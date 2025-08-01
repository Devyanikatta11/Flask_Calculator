from flask import Flask, request, jsonify,render_template
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager, create_access_token,jwt_required,get_jwt,get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from Project.utils import Calculator
import proj_config



CalObj = Calculator()


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "secre-key"
jwt = JWTManager(app)

# MySQL config
app.config['MYSQL_HOST'] = proj_config.HOST
app.config['MYSQL_USER'] = proj_config.USER
app.config['MYSQL_PASSWORD'] = proj_config.PASSWORD
app.config['MYSQL_DB'] = proj_config.DB

mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/forgot-password-page')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/reset-password-page')
def reset_password_page():
    return render_template('reset_password.html')

@app.route('/calculator-page')
def calculator_page():
    return render_template('calculator.html')




# ------------------ REGISTER ------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    mobile = data.get('mobile')
    dob = data.get('dob')
    password = data.get('password')

    if not all([name, username, email, mobile, dob, password]):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        cur = mysql.connection.cursor()
        # Check for existing username/email
        cur.execute("SELECT id FROM users_details WHERE username = %s OR email = %s", (username, email))
        if cur.fetchone():
            return jsonify({'error': 'Username or email already exists'}), 409

        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users_details (name, username, email, mobile, dob, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, username, email, mobile, dob, password_hash))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------ LOGIN ------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.form
    identifier = data.get('identifier')  # username or email
    password = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username, password_hash FROM users_details WHERE username = %s OR email = %s", (identifier, identifier))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[1], password):
            access_token = create_access_token(identity=user[0],expires_delta=datetime.timedelta(minutes=20))
            return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------ FORGOT PASSWORD ------------------
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.form
    identifier = data.get('identifier')
    dob = data.get('dob')

    if not identifier or not dob:
        return jsonify({'error': 'Missing identifier or DOB'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users_details WHERE (username = %s OR email = %s) AND dob = %s", (identifier, identifier, dob))
        user = cur.fetchone()
        cur.close()

        if user:
            access_token = create_access_token(identity=user[0])
            return jsonify({'message': 'User verified. You can now reset your password.', 'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid information provided'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    data = request.form
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'New password is required'}), 400

    try:
        username = get_jwt_identity()
        password_hash = generate_password_hash(new_password)
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users_details SET password_hash = %s WHERE username = %s", (password_hash, username))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Password reset successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

# ------------------ APIs TESTING ------------------

# @app.route("/Addition", methods=["POST"])
# def addition():
#     data = request.form
#     try:
#         a = float(data.get("a", None))
#         b = float(data.get("b", None))
#     except (TypeError, ValueError):
#         return jsonify({"Message": "Invalid input. Please provide numeric values for 'a' and 'b'."}), 400

#     result = CalObj.addition(a, b)
#     return jsonify({"Message": "successful", "Result": result})

# @app.route("/Multiplication", methods=["POST"])
# def multiply():
#     data = request.form
#     a = float(data.get("a",""))
#     b = float(data.get("b",""))
#     result = CalObj.multiplication(a,b)
#     return jsonify({"Message":"successful","Result":result})

# @app.route("/Substraction", methods=["POST"])
# def substract():
#     data = request.form
#     a = float(data.get("a",""))
#     b = float(data.get("b",""))
#     result = CalObj.substraction(a,b)
#     return jsonify({"Message":"successful","Result":result})

# @app.route("/Division", methods=["POST"])
# def division():
#     data = request.get_json()
#     a = float(data.get("a",""))
#     b = float(data.get("b",""))
#     result = CalObj.division(a,b)
#     return jsonify({"Message":"successful","Result":result})

# @app.route("/Power", methods=["POST"])
# def power():
#     data = request.form
#     a = float(data.get("a",""))
#     b = float(data.get("b",""))
#     result = CalObj.power(a,b)
#     return jsonify({"Message":"successful","Result":result})

# ------------------ CALCULATOR OPERATION ------------------

@app.route("/Calculator",methods= ["POST"])
@jwt_required()
def calculator():
    data = request.form
    try:
        a = float(data.get("a", ""))
        b = float(data.get("b", ""))
        operation = data["operation"]
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid input"}), 400

    if operation == "addition":
        result = CalObj.addition(a, b)
    elif operation == "substraction":
        result = CalObj.substraction(a, b)
    elif operation == "division":
        result = CalObj.division(a, b)
    elif operation == "multiplication":
        result = CalObj.multiplication(a, b)
    elif operation == "power":
        result = CalObj.power(a, b)
    else:
        return jsonify({"error": "Invalid operation"}), 400

    return jsonify({"status": "successful", "Result": result}), 200


blacklist = set()

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist


if __name__ == '__main__':
    app.run(host= "0.0.0.0",port=5008, debug=True)
