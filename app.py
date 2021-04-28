import logging
import os
import sys

from Blockchain import *
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Call to sqlalchemy library
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

# initialize database 'db'
db = SQLAlchemy(app)

# database model (named Records):
#   INDEX || TYPE || CREATED_ON || VERIFIED_BY || QUANTITY || BLOCK_HASH || PREVIOUS_HASH
class Records(db.Model):
    # Primary key is index, auto increments
    index = db.Column(db.Integer, primary_key=True)
    # Banning null values can act as secondary input validation if null makes it through the catch statement
    type = db.Column(db.String(200), nullable=False)
    created_on = db.Column(db.String(200), nullable=False)
    verified_by = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.String(200), nullable=False)
    block_hash = db.Column(db.String(200), nullable=False)
    previous_hash = db.Column(db.String(200), nullable=False)

    # return when new item added
    def __repr__(self):
        return '<block_hash>' % self.index

# Error handling for troubleshooting, puts out formatting and sql errors into heroku CLI logging files
def error_handling():
    return 'Error: {}. {}, line: {}'.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)

# Compute hash model from blockchain app
def compute_hash(type, verified_by, quantity):
    # Generates hash of contents of block, applied sha256
    data_Dict = {
        "type": type,
        "verifed_by": verified_by,
        "quantity": quantity}
    # Dumps bit data from the json format to prep it for sha256 hash
    block_str = json.dumps(data_Dict, sort_keys=True)
    return sha256(block_str.encode()).hexdigest()

# https://medicine-blockchain-2021.herokuapp.com/
@app.route('/')
def index():
    # Default route renders home page
    return render_template("home.html")

# https://medicine-blockchain-2021.herokuapp.com/dataentry
@app.route('/dataentry', methods=['GET','POST'])
def datapage():
    errors = []
    results = {}
    if request.method == "POST":
        # get info that the user has entered within Try-Catch statement
        try:
            # Pull user input from HTML Form
            meds = request.form['Mname']
            person = request.form['Pname']
            quantity = request.form['Qname']

            # SQL query for hash of most recent block ordered by index
            lastBlockHash = db.session.query(Records.block_hash).order_by(Records.index.desc()).first()
            # If no previous entries exist, create genesis block first
            if not lastBlockHash:
                gen_block_hash = compute_hash("empty", "empty", "empty")
                newRecords = Records(
                    type="genesis_block",
                    created_on=time.ctime(),
                    verified_by="genesis_block",
                    quantity="genesis_block",
                    block_hash=gen_block_hash,
                    previous_hash="genesis_block")
                db.session.add(newRecords)
                db.session.commit()

                # Append new entry following table defined format for Records
                new_block_hash = compute_hash(meds, person, quantity)
                newBlock = Records(
                    type=meds,
                    created_on=time.ctime(),
                    verified_by=person,
                    quantity=quantity,
                    block_hash=new_block_hash,
                    previous_hash=gen_block_hash)

                db.session.add(newBlock)
                db.session.commit()

            else:
                # Append new entry following table defined format for Records
                new_block_hash = compute_hash(meds, person, quantity)
                newBlock = Records(
                    type=meds,
                    created_on=time.ctime(),
                    verified_by=person,
                    quantity=quantity,
                    block_hash=new_block_hash,
                    previous_hash=lastBlockHash[0])
                db.session.add(newBlock)
                db.session.commit()

        except:
            # Error logging printed to heroku CLI error logs for inspection
            logging.error(error_handling())
            errors.append("Invalid data entry.")
            print(logging)

    return render_template('index.html', errors=errors, results=results)

# https://medicine-blockchain-2021.herokuapp.com/records
@app.route('/records')
def recordspage():
    allRecords = db.session.query(Records).all()
    return render_template("records.html", allRecords=allRecords)

'''
# Search function is incomplete
# https://medicine-blockchain-2021.herokuapp.com/search
@app.route('/search', methods=['GET','POST'])
def searchFunction():
    errors = []
    if request.method == "POST":
        # get info that the user has entered
        try:
            searchHash = request.form['query']
            result = db.session.query(index).filter(block_hash.key=={searchHash})

        except:
            logging.error(error_handling())
            errors.append("Invalid data entry.")

    return render_template("search.html", result=allRecords)

'''
