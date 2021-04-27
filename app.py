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
        try:
            meds = request.form['Mname']
            person = request.form['Pname']
            quantity = request.form['Qname']
            print("someone typed here")

            lastBlockHash = db.session.query(Records.block_hash).order_by(Records.index.desc()).first()

            if not lastBlockHash:
                genesis_block = Block(type="null", created_on=time.ctime(), verified_by="null", quantity="null", previous_hash="null", index=1, block_hash="null")
                gen_hash = genesis_block.compute_hash()

                newRecords = Records(
                    index= genesis_block.index,
                    type = genesis_block.type,
                    created_on = genesis_block.created_on,
                    verified_by = genesis_block.verified_by,
                    quantity = genesis_block.quantity,
                    block_hash = gen_hash,
                    previous_hash = "empty",
                )

                db.session.add(newRecords)
                db.session.commit()

                new_block_hash = Block.compute_hash(meds, person, quantity)
                newBlock = Records(
                    type=meds,
                    created_on=time.ctime(),
                    verified_by=person,
                    quantity=quantity,
                    block_hash=new_block_hash,
                    previous_hash=gen_hash,
                )

                db.session.add(newBlock)
                db.session.commit()

            else:
                new_block_hash = Block.compute_hash(meds, person, quantity)
                newBlock = Records(
                    type=meds,
                    created_on=time.ctime(),
                    verified_by=person,
                    quantity=quantity,
                    block_hash=new_block_hash,
                    previous_hash=lastBlockHash,
                )

                db.session.add(newBlock)
                db.session.commit()

        except:
            errors.append("Invalid data entry.")

    return render_template('index.html', errors=errors, results=results)

@app.route('/records')
def recordspage():
    allRecords = db.session.query(Records).all()
    return render_template("records.html", allRecords=allRecords)
