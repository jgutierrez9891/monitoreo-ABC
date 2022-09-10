Create venv
python3 -m venv venv  

Activate venv
<!-- on windows -->
venv/Scripts/activate
<!-- on Ubuntu -->
source venv/bin/activate

Install libraries
pip install flask
pip install flask_sqlalchemy
pip install marshmallow-sqlalchemy
pip install flask_restful
pip install boto3

pip install -r requirements.txt

To run the program
From flaskr folder
flask run