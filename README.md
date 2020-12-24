# wellness_app

The first thing to do is to clone the repository:

$git clone https://github.com/EronzG/CPPApp.git

Create a virtual environment to install dependencies in and activate it. A Venv virtual environment can be created by running the command:

$python -m venv env

change directory to the new env folder

$cd env

run the command to activate the virtual environment

$scripts\activate

change directory to the project root folder

$cd ..

Then install the dependencies:

(env)$ pip install -r requirements.txt

Note the (env) in front of the prompt. This indicates that this terminal session operates in a virtual environment activated.

Once pip has finished downloading the dependencies, access the 'settings.py' file in the wellness folder and modify Allowed_Hosts to permit '127.0.0.1'

In the projects root folder, run the command below to start the server

(env)$ python manage.py runserver

And navigate to http://127.0.0.1:8000/

