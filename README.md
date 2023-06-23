# Task-Manager
This is a Task-Manager inspired by JIRA
Curr version: 1.0. Project in progress. Project has a register and login form with html and css templates.

v.2.0: added registration and authorization functions, connected to sqlite using SQLALCHEMY

v.3.0: add task function implemented, view tasks.

if you need to share this project on your computer, follow this instructions:
git clone https://github.com/Simongolovinskiy/Task-Manager.git
pip install -r requirments.txt

v.4.0: This is final mvp product for some users. New functions and updates will come soon :)


Docker - If you need to start it from container: 
1) cd to your project
2) enter in cmd prompt: docker build -t task_manager . That creates docker-img for start
3) Just run it with command: docker run --rm --name Simon_Prod -p 8080:8080 task_manager
Num 3: that is container, which automatically removes himself after turning off. If you need to save it - remove '--rm' from the command above.
I didn't include volumes, so you cannot download reports if you are running that in the docker.

if you need to run it on your computer - just change app.run(debug=False, port=8080, host='0.0.0.0') in run.py to the app.run(debug=True, port=5000)
