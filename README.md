# SPHERE House Parkinson's Disease Sensors Web App

University of Bristol Master's Project (Computer Science)

This is my master's project for analyzing Parkinson's Disease symptoms in a residential environment.


![Home Screen](https://i.imgur.com/bJiVRM3.png)

![Camera Annotation](https://i.imgur.com/sewu94n.png)

![Wearable Annotation](https://i.imgur.com/EFfJqw1.png)

# To Install:

1. Make sure you have python 3 installed: https://www.python.org/downloads/
2. Make sure you have pip installed: https://pip.pypa.io/en/stable/installing/
3. Clone this repository to your local drive and navigate to the folder.

### Install requirements:
```
cd pdsensorvis
pip install -r requirements.txt
```

### Start app:
(On first run must migrate database:)
```
python3 manage.py migrate
```

```
python3 manage.py runserver
```

### Create new admin superuser:
```
python3 manage.py createsuperuser
```

Navigate browser to: http://127.0.0.1:8000/

Admin panel at: http://127.0.0.1:8000/admin/

Log in with your created admin details.
