# Quizapp
  
This is backend of quiz game app. There are hard questions. If user knows answer then can answer directly if not then try to guess some letters from the word.

  **P.S**: This website is not for a real company.

  ### Website Features:
  
  - User can register/login
  - 2 modes: multiplayer and bot-mode
  - User can start game and play with other users or with bot
    
    
  ### Technologies used in developement
   Back-end Rest Api:
   - Flask
   - Flask-Cors==3.0.8
   - Flask-Login==0.5.0
   - Flask-marshmallow==0.13.0
   - Flask-mongoengine==0.9.5
   - Flask-RESTful==0.3.8
   - Flask-SocketIO==4.3.1
  

  ### Installation
  
   In order to run the application in local environment follow instructions below:
  
  ```bash
  # clone
  git clone https://github.com/rasimatics/Quiz-game-backend.git
  
  cd Quiz-game-backend
  
  virtualenv venv
  
  source venv/bin/activate
  
  pip install -r requirements.txt
  
  python main.py
 

  ```
