# SPHERE House Parkinson's Disease Sensors Web App

University of Bristol Master's Project (Computer Science)

This is my work-in-progress master's project for analyzing Parkinson's Disease symptoms in a residential environment.

![Home Screen](https://i.imgur.com/bJiVRM3.png)

![Camera Annotation](https://i.imgur.com/sewu94n.png)

![Wearable Annotation](https://i.imgur.com/EFfJqw1.png)

# To Install:

### Make sure you have pip installed: 
```
sudo apt-get install python-pip python-dev
sudo pip install –upgrade pip
```

### Install requirements:
```
cd pdsensorvis
pip install -r requirements.txt
```

### Create new admin user
```
python3 manage.py createsuperuser
```

### Run project:
```
python3 manage.py runserver
```

Navigate browser to: http://127.0.0.1:8000/

Admin panel at: http://127.0.0.1:8000/admin/
