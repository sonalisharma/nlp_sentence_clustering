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
    options=["Bird","Face"]
    print options
    if request.method == 'POST':
        return redirect(url_for('getresults')) 
    return render_template('index.html',options=options)

def getusers():
    categories = {"cat1":10,"cat2":20,"cat3":9,"cat4":8,"cat5":2}
    #con =  eng.connect()
    #query_template = "select * from Matchglass WHERE status = active"
    #active_users = con.execute(query)
    return categories


@app.route('/results')
def getresults():
    category = getusers()
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

