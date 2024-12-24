from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, redirect, render_template, request, Response, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pytz
import requests
import time
import json

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Costea+11" 

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  
            return redirect(url_for('login_page')) 

        session_expiry = session.get('session_expiry', None)
        if session_expiry is None or datetime.now(pytz.UTC) > session_expiry:  
            session.clear()  
            return redirect(url_for('login_page'))  
        
        session['session_expiry'] = datetime.now(pytz.UTC) + timedelta(minutes=5)

        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if 'user_id' in session:  
        session['session_expiry'] = datetime.now(pytz.UTC) + timedelta(minutes=5)  
        return redirect(url_for('home_page'))  

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
                session.permanent = True  
                session['session_expiry'] = datetime.now(pytz.UTC) + timedelta(minutes=5)  
                return redirect(url_for('home_page'))  
        return redirect(url_for('register_page')) 

    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if 'user_id' in session:
        return redirect(url_for('home_page'))

    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if len(password) > 128:
            return "Password is too long! Please use a maximum of 128 characters."

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "The email is already in use! Please login."

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_page'))
    return render_template('register.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_page'))

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form.get("msg", "")
    if not user_msg.strip():
        return "The message cannot be empty!" 

    return Response(generate_response(user_msg), content_type='text/plain;charset=utf-8')

def generate_response(user_input):

    payload = {
        "model": "llama3.2",
        "prompt": user_input,
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if "response" in data:
                            yield data["response"]
                            time.sleep(0.05)  
                    except json.JSONDecodeError:
                        yield "Error parsing API response!"
        else:
            yield "Error querying Ollama!"
    except Exception as e:
        yield f"Connection error: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True, threaded=True)