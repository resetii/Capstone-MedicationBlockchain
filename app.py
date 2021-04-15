from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Blockchain import *

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///records.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///records'

# initialize db
db = SQLAlchemy(app)

# database model
class Records(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), nullable=False)
    #     created_on = db.Column(db.Datetime, default=datetime.utcnow)
    created_on = db.Column(db.String(200), nullable=False)
    verified_by = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(200), nullable=False)
    block_hash = db.Column(db.String(200), nullable=False)
    previous_hash = db.Column(db.String(200), nullable=False)

    # return when new item added
    def __repr__(self):
        return '<block_hash>' % self.index

@app.route('/')
def index():
    return "Medical Records"

@app.route('/dataentry')
def datapage():
    return render_template("index.html")
