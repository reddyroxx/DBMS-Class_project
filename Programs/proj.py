
from flask import Flask,render_template ,redirect, url_for , request
#import requests
import sqlite3 as sql
#import os.path
import datetime

conn=sql.connect("restaurant.db")

 
app = Flask(__name__)
@app.route('/home')
def home():
    return render_template("homepage.html")

@app.route("/branch",methods=["POST","GET"])
def branch():
    #tableName = "Girinagar"
    if request.method == 'POST':
        tableName=request.form['branch']
    conn=sql.connect("restaurant.db")
	#conn.row_factory=sql.Row
	#cur=conn.cursor()
    command="select branch_id from branch where location = '"+tableName+"';"
    #command="select branch_id from branch where location = 'Girinagar';"
    b_id = list(conn.execute(command))[0][0]
    #print(b_id)
    #conn.commit()
    #rows=cur.fetchall()
    #menu = ["Spicy Delight Veg Pizza","Country Special Veg Pizza","Farm House Veg Pizza","Mexican Green Wave Veg Pizza","5 Pepper Veg Pizza","Cheese and Barbeque Chicken Non-Veg Pizza","Chicken Fiesta Non-Veg Pizza","Spicy Chicken Non-Veg Pizza","Zesty Chicken Non-Veg Pizza","Chicken Mexicana Non-Veg Pizza"]    
    
    return render_template("branch_"+b_id+".html")

'''
@app.route("/queries",methods=["POST","GET"])
def queries():
    return render_template("queries.html")
'''


@app.route("/check_user",methods=["POST","GET"])
def check_user():
    if request.method == 'POST':
        contact=request.form['contact_no']
    conn=sql.connect("restaurant.db")
    command = "select * from customer where contact_no ='"+contact+"';"    
    user = list(conn.execute(command))
    rows = [contact]
    if len(user)==0:
        return render_template("registration.html",rows=rows)
    else:
        return render_template("prajwal.html",rows=rows)
    
@app.route("/user_created",methods=["POST","GET"])
def user_created():
    if request.method=='POST':
        name = request.form['name']
        contact_no = request.form['contact_no']
        email = request.form['email']
    
        
    conn = sql.connect("restaurant.db")
    command = "select count(*) from customer;"
    n = int(list(conn.execute(command))[0][0])
    
    insert_command = "INSERT INTO customer (customer_id,name,contact_no,email_id) values\
                        ('"+"c"+str(n+1)+"',"+"'"+name+"','"+contact_no+"','"+email+"');"
    conn.execute(insert_command)
    conn.commit()    
    return render_template("homepage.html")
    #return redirect(url_for('home'))
    


@app.route("/transaction_success",methods=["POST","GET"])
def transaction_success():
    
    
    
    if request.method == 'POST':
        item=request.form.getlist('pizza')
        quantity = request.form.getlist('quantity')
        contact_no = request.form['contact_no']
        branch = request.form['branch']
    #conn=sql.connect("restaurant.db")
    
    #print(item)
    #print(quantity)
    
    item = list(item)
    rows = []
    rows.append(item)
    rows.append(quantity)
    rows.append(contact_no)
    rows.append(branch)
    
    
    conn=sql.connect("restaurant.db")
    order_command = "select count(*) from orders;"
    order_number = int(list(conn.execute(order_command))[0][0])+1
    #bill_number = order_number
    date = datetime.datetime.today()
    today_date = str(date.year)+"/"+str(date.month)+"/"+str(date.day)
    rows.append(order_number)
    #rows.append(bill_number)
    rows.append(today_date)
    base_prices = []
    final_prices = []
    for i in range(len(rows[0])):
        command = "select price from menu where dish_name = '"+rows[0][i]+"'"
        l = list(conn.execute(command))[0][0]
        base_prices.append(str(l))
        final_prices.append(str(int(l)*int(rows[1][i])))
    
    rows.append(base_prices)
    rows.append(final_prices)
    bill_total = sum([int(i) for i in final_prices])
    rows.append(bill_total)
    
    c_name = list(conn.execute("select name from customer where contact_no='"+rows[2]+"'"))[0][0]
    rows.append(c_name)
    print(rows)
    
    branch_id = list(conn.execute("select branch_id from branch where location='"+rows[3]+"'"))[0][0]
    c_id = list(conn.execute("select customer_id from customer where contact_no='"+rows[2]+"'"))[0][0]
    x = list(conn.execute("select visit_count from visits where branch_id='"+branch_id+"' and customer_id='"+c_id+"' and visit_date='"+rows[5]+"'"))
    
    #visits table insertion
    if(len(x)>0):
        visit_count = int(x[0][0])
        command = "update visits set visit_count='"+str(visit_count+1)+"' where "+"branch_id='"+branch_id+"' and customer_id='"+c_id+"' and visit_date='"+rows[5]+"'"
        conn.execute(command)
        conn.commit()
    else:
        visit_count = 0
        visits_command = "insert into visits (branch_id,customer_id,visit_date,visit_count) values('"+branch_id+"','"+c_id+"','"+rows[5]+"','"+str(visit_count+1)+"')"    
        conn.execute(visits_command)
        conn.commit()
    
    
    
    
    
    #orders table insertion
    orders_command = "insert into orders (order_id,customer_name,customer_id,branch_id,order_date) values('or"+str(rows[4])+"','"+c_name+"','"+c_id+"','"+branch_id+"','"+rows[5]+"')"
    conn.execute(orders_command)
    conn.commit()
    
    #bill table insertion
    bill_command = "insert into bill (bill_id,bill_date,price,order_id) values ('bi"+str(rows[4])+"','"+rows[5]+"','"+str(rows[8])+"','or"+str(rows[4])+"')"
    conn.execute(bill_command)
    conn.commit()
    
    #order_items_command
    for j in range(len(rows[0])):
        dish_id = list(conn.execute("select dish_id from menu where dish_name='"+rows[0][j]+"'"))[0][0]
        order_items_command = "insert into order_items (order_id,quantity,dish_id) values ('or"+str(rows[4])+"','"+str(rows[1][j])+"','"+dish_id+"')"
        conn.execute(order_items_command)
        conn.commit()
    
    return render_template("transaction_success.html",rows=rows)
    



if __name__ == '__main__':
    app.run(debug=True)
    
