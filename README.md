# SPHERE House Parkinson's Disease Sensors Web App

University of Bristol Master's Project (Computer Science)

This is my work-in-progress master's project for analyzing Parkinson's Disease symptoms in a residential environment.

![Home Screen](https://i.imgur.com/bJiVRM3.png)

![Camera Annotation](https://i.imgur.com/sewu94n.png)

![Wearable Annotation](https://i.imgur.com/EFfJqw1.png)

# To Install:

1. Make sure you have pip installed: https://pip.pypa.io/en/stable/installing/
2. Make sure you have python 3 installed: https://www.python.org/downloads/
3. Clone this repository to your local drive and navigate to the folder.

### Install requirements:
```
cd pdsensorvis
pip install -r requirements.txt
```

### Create new superadmin user:
```
python3 manage.py createsuperuser
```

### Start app:
```
python3 manage.py runserver
```

Navigate browser to: http://127.0.0.1:8000/

Admin panel at: http://127.0.0.1:8000/admin/
