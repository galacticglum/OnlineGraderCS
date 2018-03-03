from flask import Flask
from wtforms import Form
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:glumpanda@localhost/online_grader_cs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/register')
def register():
    pass

if __name__ == '__main__':
    app.run()