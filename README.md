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
pip install Flask-JWT
pip install Flask-JWT-Extended
pip install PyJWT

pip install -r requirements.txt

To run the program
From flaskr folder
flask run
flask run --host=0.0.0.0 --port=5001