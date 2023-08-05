from flask import Flask, render_template, request, jsonify
import cx_Oracle
app = Flask(__name__)
import argon2
argon2_hasher = argon2.PasswordHasher()

def get_connection():
    return cx_Oracle.connect('hr/hr@localhost:1521/xe')

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

                # Verify the entered password against the stored hashed password using Argon2
                try:
                    argon2_hasher.verify(stored_password, entered_password)
                    # Successful login: Store user information in the session
                    return jsonify({'message': 'Login successful!'})

                except argon2.exceptions.VerifyMismatchError:
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



@app.route('/')
def index():
    return render_template("index.html")





@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Get the form data submitted by the user
        name = request.form.get('name')
        gender = request.form.get('gender')
        address = request.form.get('address')
        email = request.form.get('email')
        pincode = request.form.get('pincode')

        # Get the selected product name from the query parameter
        product_name = request.args.get('product_name')

        try:
            con = get_connection()
            cursor = con.cursor()

            sql = "INSERT INTO PAYMENT (NAME, GENDER, ADDRESS, EMAIL, PINCODE, PRODUCT_NAME) VALUES (:1, :2, :3, :4, :5, :6)"
            cursor.execute(sql, (name, gender, address, email, pincode, product_name))
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
        return jsonify({'message': 'Payment details saved successfully!'})

    # Get the product ID from the query parameter and pass it to the payment form
    product_name = request.args.get('product_name')
    return render_template("paymentform.html", product_name=product_name)

if __name__ == "__main__":
    app.run(debug=True)
