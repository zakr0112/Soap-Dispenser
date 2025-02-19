# Soap-Dispenser
Website for the tracking of a motion sensor soap dispenser device

## Prerequisites

Things you will require

* Pycharm or Visual Studio Code
* Python installed to path
* git bash installed


THE INSTALLATION IS NOT FINAL

## Getting Started
Open your editor of choice and open the terminal to clone this repository:
```
git clone https://github.com/zakr0112/Soap-Dispenser.git
cd Soap-Dispenser
```
Note: This should clone the repository into your file system and navigate to it\
If for example you are using visual studio code, make sure it's a blank window when\
cloning the repo, and after cloning the reop succesfully make sure you press\
"open folder" and select the one called "???"


## Installation

Step by step installation\
Open the terminal in the editor and run the following commands:
```
python -m venv venv
```
## Activate VENV (Windows)
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\activate
```
## Activate VENV (Mac/Linux)
```
source venv/bin/activate
```
## Continue (Universal)
```
cd SoapProject\soapdispenser
```
```
pip install -r requirements.txt
```
```
pip install django
```
```
pip install pillow
```

## Final Run
Open a new terminal via 'View > Terminal' in VS CODE and run the following commands
```
cd Soap-Dispenser/SoapProject
```
```
python manage.py runserver
```

## Additional Information

* Using Django as the web framework
* sqlite3 database
* bulma CSS
* JavaScript
