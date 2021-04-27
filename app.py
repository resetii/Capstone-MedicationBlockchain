import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from Blockchain import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

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
    return render_template("home.html")

@app.route('/dataentry', methods=['GET','POST'])
def datapage():
    errors = []
    results = {}
    print("got to data page")
    if request.method == "POST":
        # get info that the user has entered
        #try:
            meds = request.form['Mname']
            person = request.form['Pname']
            quantity = request.form['Qname']
            print("someone typed here")

            testForGenesis = db.session.query(Records.block_hash).order_by(Records.index.desc()).first()
            if testForGenesis:
                print("exists")
            else:
                print("Fail")
            # if not testForGenesis:
            #     newBlock = Block()
            #     compHash = newBlock.compute_hash()
            #
            # highestIndex = db.session.query(index).last()

        #except:
            errors.append("Invalid data entry.")
            print("except block error jump")

    return render_template('index.html', errors=errors, results=results)

@app.route('/records')
def recordspage():
    allRecords = db.session.query(Records).all()
    return render_template("records.html", allRecords=allRecords)
