from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    verified = db.Column(db.Boolean, default=False)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return jsonify({'message': 'Logged in successfully'})
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already exists'}), 400
    new_user = User(email=email, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.json['email']
    user = User.query.filter_by(email=email).first()
    if user:
        # Send password reset email here
        msg = Message('Password Reset', sender='your-email@gmail.com', recipients=[email])
        msg.body = 'Click this link to reset your password: http://example.com/reset-password'
        mail.send(msg)
        return jsonify({'message': 'Password reset email sent'})
    else:
        return jsonify({'error': 'Email not found'}), 404

@app.route('/verify-email', methods=['POST'])
def verify_email():
    email = request.json['email']
    user = User.query.filter_by(email=email).first()
    if user:
        user.verified = True
        db.session.commit()
        return jsonify({'message': 'Email verified'})
    else:
        return jsonify({'error': 'Email not found'}), 404
