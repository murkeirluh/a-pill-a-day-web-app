# A-Pill-A-Day web app
## CS 145 1718B Capstone Project
This web app allows doctors to create and update prescriptions and intake schedules for their patient/s. These prescriptions and schedules are viewable by the patient. This web app is integrated with our smart medicine box and its accompanying mobile app that alerts the patient when it is time to take their medicine for the time of day.

### Team 11 Members:
- Caparoso, Patricia
- De Guzman, Nicole Jade
- Divina, Christelle
- Lopez, Mikayla
- Robino, Gem

### Installation and setup

**Main dependencies:** Python 3.6, pip, Django 2.0, virtualenv

1. Install Python 3.6 from the Python website. pip should already come with this Python version. If it has been properly installed, running `python --version` (alternatively `python3 --version`) and `pip`  on the terminal should display the version of your Python installation, and commands and flags for pip.

2.  Install virtualenv using pip.
    
    `$ pip install virtualenv`

    Test the installation
    
    `$ virtualenv --version`

### Cloning the project
1. Create or go to the directory where you want to clone the project

2. Create your virtualenv. In this case, my virtualenv name is _apilladay_.
    
    `$ virtualenv -p python3 apilladay`

3. `cd` inside your virtualenv.
    
    `$ cd apilladay`

4. Activate the virtualenv. On Windows, the `activate` command should be inside the _Scripts_ folder. For Linux, I believe it is inside _bin_.
	
	On Windows

    `$ Scripts\activate`

    On Linux

    `$ source bin/activate`

    You should see `(APILLADAY)` (or something similar) at the beginning of your 

5. Clone the repository
    
	`$ git clone https://github.com/murkeirluh/a-pill-a-day-web-app.git`

6. Install project requirements
    
    `$ pip install -r requirements.txt`

7. `cd` into the folder project and check for the folder with the file 'manage.py'

8. Make database migrations
    
    `$ python manage.py makemigrations`

9. Migrate the database
    
    `$ python manage.py migrate`