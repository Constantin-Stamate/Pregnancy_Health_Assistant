from datetime import timedelta
from flask import Flask, render_template, request, Response
from flask_sqlalchemy import SQLAlchemy
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
    app.run(debug=True, threaded=True) 