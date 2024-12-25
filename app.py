from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, redirect, render_template, request, Response, session, url_for
import joblib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import pytz
import requests
import time
import json
import pandas as pd

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

model_ros = joblib.load('models/gradient_boosting.pkl')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "Costea+11" 

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class PregnancyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    baseline_value = db.Column(db.String(120), nullable=False)
    accelerations = db.Column(db.String(120), nullable=False)
    fetal_movement = db.Column(db.String(120), nullable=False)
    uterine_contractions = db.Column(db.String(120), nullable=False)
    light_decelerations = db.Column(db.String(120), nullable=False)
    severe_decelerations = db.Column(db.String(120), nullable=False)
    prolonged_decelerations = db.Column(db.String(120), nullable=False)
    abnormal_variability = db.Column(db.String(120), nullable=False)
    short_variability = db.Column(db.String(120), nullable=False)
    percentage_of_variability = db.Column(db.String(120), nullable=False)
    long_variability = db.Column(db.String(120), nullable=False)
    histogram_width = db.Column(db.String(120), nullable=False)
    histogram_min = db.Column(db.String(120), nullable=False)
    histogram_max = db.Column(db.String(120), nullable=False)
    histogram_of_peaks = db.Column(db.String(120), nullable=False)
    histogram_of_zeroes = db.Column(db.String(120), nullable=False)
    histogram_mode = db.Column(db.String(120), nullable=False)
    histogram_mean = db.Column(db.String(120), nullable=False)
    histogram_median = db.Column(db.String(120), nullable=False)
    histogram_variance = db.Column(db.String(120), nullable=False)
    histogram_tendency = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<PregnancyData {self.id}>"

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

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route("/predict")
@login_required
def predict_page():
    return render_template('predict.html')

@app.route("/result", methods=["GET"])
@login_required
def result():
    data = session.get('form_data', {})

    if data:
        features_dict = {
            'baseline value': data.get('baseline_value'),
            'accelerations': data.get('accelerations'),
            'fetal_movement': data.get('fetal_movement'),
            'uterine_contractions': data.get('uterine_contractions'),
            'light_decelerations': data.get('light_decelerations'),
            'severe_decelerations': data.get('severe_decelerations'),
            'prolongued_decelerations': data.get('prolonged_decelerations'),
            'abnormal_short_term_variability': data.get('abnormal_variability'),
            'mean_value_of_short_term_variability': data.get('short_variability'),
            'percentage_of_time_with_abnormal_long_term_variability': data.get('percentage_of_variability'),
            'mean_value_of_long_term_variability': data.get('long_variability'),
            'histogram_width': data.get('histogram_width'),
            'histogram_min': data.get('histogram_min'),
            'histogram_max': data.get('histogram_max'),
            'histogram_number_of_peaks': data.get('histogram_of_peaks'),
            'histogram_number_of_zeroes': data.get('histogram_of_zeroes'),
            'histogram_mode': data.get('histogram_mode'),
            'histogram_mean': data.get('histogram_mean'),
            'histogram_median': data.get('histogram_median'),
            'histogram_variance': data.get('histogram_variance'),
            'histogram_tendency': data.get('histogram_tendency')
        }

        input_data = pd.DataFrame([features_dict])

        prediction = model_ros.predict(input_data)[0]
        return render_template('result.html', data=data, prediction=prediction)

    return render_template('result.html', data=data, prediction=None)

@app.route("/chat")
@login_required
def chat_page():
    return render_template('chat.html')

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
            else:
                return render_template('login.html')  
        else:
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

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form.get("msg", "")
    if not user_msg.strip():
        return "The message cannot be empty!" 

    bot_response = generate_response(user_msg)
    save_message_to_db(user_msg, bot_response) 
    return Response(bot_response, content_type='text/plain;charset=utf-8')

@app.route("/submit", methods=["POST"])
@login_required
def submit_form():
    if request.method == "POST":
        baseline_value = request.form['baseline_value']
        accelerations = request.form['accelerations']
        fetal_movement = request.form['fetal_movement']
        uterine_contractions = request.form['uterine_contractions']
        light_decelerations = request.form['light_decelerations']
        severe_decelerations = request.form['severe_decelerations']
        prolonged_decelerations = request.form['prolonged_decelerations']
        abnormal_variability = request.form['abnormal_variability']
        short_variability = request.form['short_variability']
        percentage_of_variability = request.form['percentage_of_variability']
        long_variability = request.form['long_variability']
        histogram_width = request.form['histogram_width']
        histogram_min = request.form['histogram_min']
        histogram_max = request.form['histogram_max']
        histogram_of_peaks = request.form['histogram_of_peaks']
        histogram_of_zeroes = request.form['histogram_of_zeroes']
        histogram_mode = request.form['histogram_mode']
        histogram_mean = request.form['histogram_mean']
        histogram_median = request.form['histogram_median']
        histogram_variance = request.form['histogram_variance']
        histogram_tendency = request.form['histogram_tendency']

        data = {
            'baseline_value': baseline_value,
            'accelerations': accelerations,
            'fetal_movement': fetal_movement,
            'uterine_contractions': uterine_contractions,
            'light_decelerations': light_decelerations,
            'severe_decelerations': severe_decelerations,
            'prolonged_decelerations': prolonged_decelerations,
            'abnormal_variability': abnormal_variability,
            'short_variability': short_variability,
            'percentage_of_variability': percentage_of_variability,
            'long_variability': long_variability,
            'histogram_width': histogram_width,
            'histogram_min': histogram_min,
            'histogram_max': histogram_max,
            'histogram_of_peaks': histogram_of_peaks,
            'histogram_of_zeroes': histogram_of_zeroes,
            'histogram_mode': histogram_mode,
            'histogram_mean': histogram_mean,
            'histogram_median': histogram_median,
            'histogram_variance': histogram_variance,
            'histogram_tendency': histogram_tendency
        }

        user_id = session.get('user_id')

        new_data = PregnancyData(
            user_id=user_id,  
            baseline_value=baseline_value,
            accelerations=accelerations,
            fetal_movement=fetal_movement,
            uterine_contractions=uterine_contractions,
            light_decelerations=light_decelerations,
            severe_decelerations=severe_decelerations,
            prolonged_decelerations=prolonged_decelerations,
            abnormal_variability=abnormal_variability,
            short_variability=short_variability,
            percentage_of_variability=percentage_of_variability,
            long_variability=long_variability,
            histogram_width=histogram_width,
            histogram_min=histogram_min,
            histogram_max=histogram_max,
            histogram_of_peaks=histogram_of_peaks,
            histogram_of_zeroes=histogram_of_zeroes,
            histogram_mode=histogram_mode,
            histogram_mean=histogram_mean,
            histogram_median=histogram_median,
            histogram_variance=histogram_variance,
            histogram_tendency=histogram_tendency
        )

        db.session.add(new_data)
        db.session.commit()

        session['form_data'] = data

        return redirect(url_for('predict_page'))

def save_message_to_db(user_msg, bot_response):
    try:
        message = Message(user_message=user_msg, bot_response=bot_response)
        db.session.add(message)
        db.session.commit()
    except Exception as e:
        print(f"Error saving message: {e}")

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
                            time.sleep(0.00001)  
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