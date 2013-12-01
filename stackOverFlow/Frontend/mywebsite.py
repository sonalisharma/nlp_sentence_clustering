import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for
from flask import send_from_directory   
from pybtex.database.input import bibtex
from sqlalchemy import distinct
from itertools import izip
from sqlalchemy import create_engine, MetaData, Table


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial.db'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
eng = db.create_engine("sqlite:///tutorial.db")
#db.drop_all()
#db.create_all()
app.debug = True
metadata = MetaData(bind=eng)

@app.route("/", methods=['GET', 'POST'])
def getuser():
    if request.method == 'POST':
        return redirect(url_for('getresults')) 
    return render_template('index.html')

def getdata():
    categories = {"cat1":{"sent":["This is the first cat1 sentence",
                                   "This is the second cat1 sentence",
                                   "This is the third cat1 sentence",
                                   "This is the fourth cat1 sentence"],"freq":20},
                  "cat2":{"sent":["This is the first cat2 sentence",
                                   "This is the second cat2 sentence",
                                   "This is the third cat2 sentence",
                                   "This is the fourth cat2 sentence"],"freq":15},
                  "cat3":{"sent":["This is the first cat3 sentence",
                                   "This is the second cat3 sentence",
                                   "This is the third cat3 sentence",
                                   "This is the fourth cat3 sentence"],"freq":14},
                  "cat4":{"sent":["This is the first cat4 sentence",
                                   "This is the second cat4 sentence",
                                   "This is the third cat4 sentence",
                                   "This is the fourth cat4 sentence"],"freq":12},
                  "cat5":{"sent":["This is the first cat5 sentence",
                                   "This is the second cat5 sentence",
                                   "This is the third cat5 sentence",
                                   "This is the fourth cat5 sentence"],"freq":10}}
    #con =  eng.connect()
    #query_template = "select * from Matchglass WHERE status = active"
    #active_users = con.execute(query)
    return categories

@app.route('/data', methods=['GET', 'POST'])
def data():
    print "here inside data"
    list_name = request.args.get("input_value")
    cat = getdata()
    print "listname"
    print list_name
    print "/listname"
    #print cat[list_name]
    #print list_name
    return render_template('index.html',categories=cat)

@app.route('/results')
def getresults():
    category = getdata()
    return render_template('index.html',categories=category)

@app.route('/user/<name>')
def thanks(name):
    message = "Thanks! Collect your glass and prepare to find your match."
    return render_template('thankyou.html',status = message)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print "I am in upload"  
    try:
        data = [] 
        data.append(name)
        data.append("active")
        data.append(radio)
        data.append(colorbox)
        data.append("follow")
        data.append("matchpin")
        data.append("expinterest")
        data.append(email)
        print data
        matchdata = Matchglass(str(data[0]),str(data[1]),str(data[2]),str(data[3]),str(data[4]),str(data[5]),str(data[6]),str(data[7]))
        db.session.add(matchdata)
        db.session.commit()
    except Exception,e:
        flag = "failure"
        print e
    
    return redirect(url_for('thanks',name="dummy"))
if __name__ == "__main__":
    global name
    global email
    global radio
    global colorbox
    #db.drop_all()
    #db.create_all()
    app.run()

