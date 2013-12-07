import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for
from flask import send_from_directory   
from pybtex.database.input import bibtex
from sqlalchemy import distinct, Table
from itertools import izip
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session,sessionmaker
from processing import fetchphrases


app = Flask(__name__)
SQLALCHEMY_DATBASE_URI='sqlite:///tutorial.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATBASE_URI
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

engine = create_engine(SQLALCHEMY_DATBASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))

db = SQLAlchemy(app)

#db.drop_all()
#db.create_all()
app.debug = True
metadata = MetaData(bind=engine)

@app.route("/", methods=['GET', 'POST'])
def getuser():
    if request.method == 'POST' and request.form is not None:
        try:
          query=str(request.form["txt_query"])
          return redirect(url_for('getresults',query=query)) 
        except:
          print "Exception while handling user query"
          return redirect(url_for('getresults',query="999"))
    return render_template('index.html')

def getdata(query):
    print "here"
    if query is not None:
      parents,children=fetchphrases(query)
      #Parents Dict: category:freq Children dict: parent_cat:[category:freq]
      categories={}
      for phrase,freq in parents.items():
        try:
          categories[str(phrase)]=([],freq)
        except UnicodeEncodeError:
          categories[phrase]=([],freq)
      #Search for each category in ngrams.lemmangrams, get question ids from ngrams 
      #and question text from questions table
      results={}
      for k,v in categories.items():
        ques=[]
        try:
          res = engine.execute("select q.ques_text,q.answer_id from ngrams n join questions\
          q on n.questionid=q.id where n.lemmangrams='{}'".format(k))
          for r in res:
            ans_id=str(r['answer_id'])
            ans_text=engine.execute("select answer_text from answers where id='{}'".format(ans_id))
            ques.append(str(r['ques_text']))
        except UnicodeEncodeError:
          continue  
        results[k]=(list(set(ques)),v[1]) 
      
      return results

@app.route('/data', methods=['GET', 'POST'])
def data():
    print "here inside data"
    list_name = request.args.get("input_value")
    cat = getdata()
    print "listname"
    print list_name
    print "/listname"
    return render_template('index.html',categories=cat)

@app.route('/results/<query>')
def getresults(query):
    if query is not None:
      if query=='999':
        categories=[]
      else:
        categories=getdata(query)
    return render_template('index.html',categories=categories)

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

