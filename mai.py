from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'ajdvbnm_lknve#vklnejkna3'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    firstName = db.Column(db.String(length=30), nullable=False, unique=False)
    lastName = db.Column(db.String(length=30), nullable=False, unique=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    password = db.Column(db.String(length=50), nullable=False, unique=True)
    balance = db.Column(db.Integer(), default=0)

with app.app_context(): 
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        repeatedPassword = request.form.get('repeat_password')

        if not firstName or not lastName or not email or not password:
            return render_template('sign_up.html', message=True)
        
        if repeatedPassword != password:
            return render_template('sign_up.html', passErr=True)
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
             return render_template('sign_up.html', emailErr=True)

        new_user = User(firstName=firstName, lastName=lastName, email=email, password=password, balance=0)
        db.session.add(new_user)
        db.session.commit()
        return render_template('home.html', user=new_user)

    return render_template('sign_up.html')

@app.route("/log_in", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if user.email == email and user.password == password:
                return render_template('home.html', user=user)
            else:
             return render_template('log_in.html', error=True)
        else :
            return render_template('log_in.html', error=True)

    return render_template('log_in.html')

@app.route("/welcomeSir", methods=["GET", "POST"])
def welcomeSir():
    return render_template('log_in.html')

@app.route("/einzahlen/<int:id>", methods=["POST", "GET"])
def einzahlen(id):
    user = User.query.get(id)
    if request.method == "POST":
        newBalance = request.form.get('newBalance')
        if newBalance:
            user.balance += int(newBalance) 
            db.session.commit()
    return render_template('home.html', user=user)

@app.route("/auszahlen/<int:id>", methods=["POST", "GET"])
def auszahlen(id):
    user = User.query.get(id)
    if request.method == "POST":
        newBalance = request.form.get('newBalance')
        if newBalance:
            user.balance -= int(newBalance) 
            db.session.commit()
    return render_template('home.html', user=user)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8080)
