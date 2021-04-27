import os, logging, sys
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

def error_handling():
    return 'Error: {}. {}, line: {}'.format(sys.exc_info()[0],
                                         sys.exc_info()[1],
                                         sys.exc_info()[2].tb_lineno)

def compute_hash(type, verified_by, quantity):
    # Generates hash of contents of block, applied sha256
    data_Dict = {
        "type": type,
        "verifed_by": verified_by,
        "quantity": quantity}

    # Dumps bit data from the json format to prep it for sha256 hash
    block_str = json.dumps(data_Dict, sort_keys=True)
    return sha256(block_str.encode()).hexdigest()

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
        try:
            meds = request.form['Mname']
            person = request.form['Pname']
            quantity = request.form['Qname']
            print("someone typed here")
            print(time.ctime())

            lastBlockHash = db.session.query(Records.block_hash).order_by(Records.index.desc()).first()
            print("found last block hash")

            if not lastBlockHash:
                print("entered if not lasthash")

                gen_block_hash = compute_hash("empty", "empty", "empty")
                newRecords = Records(
                    type="meds",
                    created_on=time.ctime(),
                    verified_by="person",
                    quantity="quantity",
                    block_hash=gen_block_hash,
                    previous_hash="gen_hash")


                print("created new record")

                db.session.add(newRecords)
                db.session.commit()
                print("commit gen hash")

                new_block_hash = compute_hash(meds, person, quantity)
                newBlock = Records(
                    type=meds,
                    created_on=time.ctime(),
                    verified_by=person,
                    quantity=quantity,
                    block_hash=new_block_hash,
                    previous_hash=gen_block_hash)
                print("created new block")

                db.session.add(newBlock)
                db.session.commit()
                print("commit new block")


            else:
                print(" else statement")
                new_block_hash = compute_hash(meds, person, quantity)
                print("computed else new hash")
                newBlock = Records(
                    type=meds,
                    created_on=time.ctime(),
                    verified_by=person,
                    quantity=quantity,
                    block_hash=new_block_hash,
                    previous_hash=lastBlockHash)
                print("created else new block")

                db.session.add(newBlock)
                db.session.commit()
                print("commit after else statement")

        except:
            logging.error(error_handling())
            errors.append("Invalid data entry.")
            print("fall through try block")
            print(logging)

    return render_template('index.html', errors=errors, results=results)

@app.route('/records')
def recordspage():
    allRecords = db.session.query(Records).all()
    return render_template("records.html", allRecords=allRecords)


