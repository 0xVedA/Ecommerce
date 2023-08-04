from flask import Flask, render_template, request, jsonify
import cx_Oracle
from cryptography.fernet import Fernet
app = Flask(__name__)
import bcrypt

def get_connection():
    return cx_Oracle.connect('hr/hr@localhost:1521/xe')





@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        entered_password = request.form.get('password')

        try:
            # Establish the database connection
            conn = get_connection()
            cursor = conn.cursor()

            # Fetch the user data based on the entered email
            sql = "SELECT email, USER_PASSWORD FROM SIGNUP WHERE email = :1"
            cursor.execute(sql, (email,))
            user_data = cursor.fetchone()

            if user_data:
                stored_email, stored_password = user_data

                # Verify the entered password against the stored hashed password
                if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password.encode('utf-8')):
                    # Successful login: Store user information in the session

                    return jsonify({'message': 'Login successful!'})
                else:
                    return jsonify({'error': 'Invalid email or password'})
            else:
                return jsonify({'error': 'Invalid email or password'})

        except Exception as e:
            return jsonify({'error': str(e)})

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                print("connection closed")

    # If the request is a GET request, render the login page
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
        password = request.form.get('pwd')

        # Generate a new random salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        try:
            con = get_connection()
            cursor = con.cursor()

            sql = "INSERT INTO SIGNUP (UNAME, MOBILE, EMAIL, USER_PASSWORD) VALUES (:1, :2, :3, :4)"
            cursor.execute(sql, (name, mobile, email, hashed_password.decode('utf-8')))  # Note the decode here
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
