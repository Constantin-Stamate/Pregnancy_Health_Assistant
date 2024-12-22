from flask import Flask, render_template, request, Response
import requests
import time
import json

app = Flask(__name__)

OLLAMA_API_URL = "http://localhost:11434/api/generate"

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    user_msg = request.form.get("msg", "")
    if not user_msg.strip():
        return "The message cannot be empty!" 

    return Response(generate_response(user_msg), content_type='text/plain;charset=utf-8')

if __name__ == '__main__':
    app.run(debug=True, threaded=True) 