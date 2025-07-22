<p align="center">
  <img src="static/images/favicon.png" alt="Image Description" width="120"/>
</p>
<p align="center"><b style="font-size: 21px; font-family: 'Times New Roman', serif;">Support for You and Your Baby</b><p>

## Overview

**The Pregnancy Health Assistant** is a web application that uses a chatbot and Machine Learning prediction to provide advice based on investigative medical data (Campos, D. & Bernardes, J. (2000). UCI Machine Learning Repository. https://doi.org/10.24432/C51S4N).

It offers a supportive interface for pregnant users to receive real-time assistance and fetal health evaluations in an accessible and user-friendly way, combining advanced predictive analytics with intuitive design to ensure users feel confident and informed throughout their pregnancy journey.

<p align="center">
  <img src="static/images/assistant.png" alt="Assistant"/>
</p>

## Features

- **User Authentication**: Register and log in to access personalized features.
<p align="center">
  <img src="static/images/authentication.png"/>
</p>

- **Fetal Health Prediction**: Input medical data such as fetal heart rate, uterine contractions, etc., and receive a prediction based on the Gradient Boosting model.
<p align="center">
  <img src="static/images/prediction.png"/>
</p>

- **Prediction Results**: Review the entered health data along with a preliminary diagnosis and recommendations to highlight potential fetal risks.
<p align="center">
  <img src="static/images/summary.png"/>
</p>

- **HealthAI Chatbot**: Ask questions related to fetal and maternal health, and receive AI-based guidance and feedback using predictive medical models.
<p align="center">
  <img src="static/images/prompt.png"/>
</p>

## Installation

To install the application, follow these steps:

1. **Clone this repository:**
```bash
   git clone https://github.com/Constantin-Stamate/PregnancyHealthAssistant.git
```

2. **Navigate to the project repository:**
```bash
   cd path to directory/PregnancyHealthAssistant
```

3. **Create a virtual environment:**
```bash
   python3 -m venv venv
```

4. **Activate the virtual environment for Windows:**
```bash
   venv/Scripts/activate.bat --activate virtual env
```

5. **Activate the virtual environment for Mac:**
```bash
   source venv/bin/activate
```

6. **Install the dependecies:**
```bash
   pip install -r requirements.txt
```

7. **Additionally, you can connect to a mySQL database and create a project:**
```bash
   app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<username>:<password>@<hostname>:<port>/<database_name>'
```

8. **Replace flask key with your personal one:**
```bash
   app.secret_key = "your_secure_secret_key"
```

9. **Setup the chatBot:**
```bash
   https://ollama.com/download
```

10. **Run the following command in the terminal:**
```bash
   ollama run llama3.2
```

11. **Run the application:**
```bash
   python app.py
```

12. **Navigate to the following URL in your browser and use the app:**
```bash
   http://127.0.0.1:5000
```

## Technologies

- **Framework**: Flask  
- **Programming Language**: Python  
- **Machine Learning**: Gradient Boosting, Logistic Regression, Decision Tree, Ollama 3.2  
- **Database**: MySQL  
- **Frontend**: HTML, CSS
- **Version Control**: Git, GitHub  
- **Development Environment**: Visual Studio Code 

## Contributors

For more details about our project or any general information, feel free to reach out to us.

<a href="https://github.com/Alexandra-Paula"><img src="https://avatars.githubusercontent.com/u/144719877?v=4" title="Manea Alexandra-Paula" width="60" height="60"></a> 
<a href="https://github.com/Andrei-Chiosa"><img src="https://avatars.githubusercontent.com/u/164755219?v=4" title="Chiosa Andrei" width="60" height="60"></a>
<a href="https://github.com/Constantin-Stamate"><img src="https://avatars.githubusercontent.com/u/173792187?s=400&u=a7d867c53fbc3b0e988b72205f155a1bca7249ac&v=4" title="Stamate Constantin" width="60" height="60"></a>