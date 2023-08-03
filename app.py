from flask import Flask, render_template, request, jsonify
import cx_Oracle
app = Flask(__name__)

def get_connection():
    return cx_Oracle.connect('hr/hr@localhost:1521/xe')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")
    

@app.route('/payment')
def payment():
    return render_template("paymentform.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get the form data submitted by the user
        name = request.form.get('Uname')
        mobile = request.form.get('Mobnum')
        email = request.form.get('Email')
        user_password = request.form.get('pwd')

        try:
            con = get_connection()
            cursor = con.cursor()

            sql = "INSERT INTO SIGNUP (UNAME, mobile, email, USER_PASSWORD) VALUES (:1, :2, :3, :4)"
            cursor.execute(sql, (name, mobile, email, user_password))
            con.commit()
            print("values inserted")

        except Exception as e:
            return jsonify({'error': str(e)})

        finally:
            if cursor:
                cursor.close()
            if con:
                con.close()
                print("connection closed")

        # Return a response to the user after the form data is processed
        return jsonify({'message': 'User registered successfully!'})

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
