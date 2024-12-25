# Pregnancy Health Assistant  

This is a project to implement AI features and workflow practices, to create a web app, that takes important steps in solving a real world problem.

## Setup Guide

1. **Clone the repository**
Clone the project repository to your local machine using the following command:
```bash
    git clone https://github.com/Constantin-Stamate/Pregnancy_Health_Assistant.git
```

2. **Navigate to the project repository**
```bash
    cd path to directory/Pregnancy_Health_Assistant
```

3. **Create a virtual environment**
```bash
    python3 -m venv venv
```

4. **Activate the virtual environment**
For Windows
```bash 
    venv/Scripts/activate.bat --activate virtual env
```
For Mac
```bash
    source venv/bin/activate
```

5. **Install the dependecies**
```bash
    pip install -r requirements.txt
```

6. **Additionally, you can connect to a mySQL database and create a project**
Open the file app.py and change the configuration of the database with your personal data.
```bash
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@<hostname>:<port>/<database_name>'
```

7. **Replace flask key with your personal one**
```bash
    app.secret_key = "your_secure_secret_key"
```

8. **Setup the chatBot**
Download the ollama local AI model. 
```bash
    https://ollama.com/download
```
Run the following command in the terminal
```bash
    ollama run llama3.2
```


9. **Run the application**
Run the app.py file. 
```bash
python app.py
```

10. **Navigate to the following URL in your browser and use the app**
```bash
http://127.0.0.1:5000
```

11. **Additionally, you can run tox checks**
Run the source code from the tests folder. 



## About the Project

This project is a web app that uses a chatbot and Machine Learning Prediction, to give advice to people, using investigative medicinal data (Campos, D. & Bernardes, J. (2000). Cardiotocography [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C51S4N.). The data is analysed using an AI model. To test some of the functionalities you can interact with the chatbot, after running the app. The main functionality of the project, is the prediction, made using a ML model and input data. 