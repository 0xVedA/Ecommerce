from flask import Flask, render_template
import cx_Oracle
app = Flask(__name__)

try:
    con = cx_Oracle.connect('hr/hr@localhost:1521/xe')
    print(con.version)

    cursor = con.cursor()

    #cursor.execute('create table "CART"("UID" integer primary key, "NAME" varchar2(30), "ITEM" varchar2(100))')
    #cursor.execute('''insert into CART values (001, 'YT', 'TV')''')
    con.commit()
    print("Table Inserted successfully")

except cx_Oracle.DatabaseError as e:
    print("There is a problem with Oracle", e)

finally:
    if cursor:
        cursor.close()
    if con:
        con.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")
    

@app.route('/payment')
def payment():
    return render_template("paymentform.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")







if __name__ == "__main__":
    app.run()
#vedant