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
from flask import json

app = Flask(__name__)

#SQLALCHEMY_DATABASE_URI = 'mysql://nlp_user:nlp_user@localhost/stackoverflow'

SQLALCHEMY_DATABASE_URI='sqlite:///tutorial.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI



engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

db = SQLAlchemy(app)
eng = db.create_engine(SQLALCHEMY_DATABASE_URI)

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

def getdata(query,):
    print "here"
    if query is not None:
      parent,children,grand=fetchphrases(query)
      #Parents Dict: category:freq Children dict: parent_cat:[category:freq], Grand dict : child_cat:[category:freq]
      parentcategories={}
      childcategories={}
      grandcategories={}
      categories = {}

      for phrase,freq in parent.items():
        try:
          categories[str(phrase)]=freq
        except UnicodeEncodeError:
          categories[phrase]=freq
      #Search for each category in ngrams.lemmangrams, get question ids from ngrams 
      #and question text from questions table
      
     
      return (parent,children,grand)


@app.route('/data', methods=['GET', 'POST'])
def data():
    #print "here inside data"
    #list_name = request.args.get("isLocked")
    #print "I am here inside data"
    #print list_name

    data = json.loads(request.form.get('data'))
    phrase_data = data['value']

    results={}
    for p in phrase_data:
      print str(p)
      ques_ans=[]
      try:
        print "select q.ques_text,q.id,q.answer_text from ngrams n join questions\
        q on n.questionid=q.id where n.lemmangrams='{}'".format(str(p))

        res = engine.execute("select q.ques_text,q.id,q.answer_text from ngrams n join questions\
        q on n.questionid=q.id where n.lemmangrams='{}'".format(str(p)))
        print "After execute"
        print res
        for r in res.fetchall():
          print r
          ques_ans.append([str(r['id']),str(r['ques_text']),str(r['answer_text'])])
        results[str(p)]=ques_ans
      except UnicodeEncodeError:
        continue  
      #results[str(p)]=ques_ans
    print results
    #return str(ss)
    return  "somthing"
    #cat = getdata()
    #print "listname"
    #print list_name
    #print "/listname"
    #return render_template('index.html',categories=cat)

@app.route('/results/<query>')
def getresults(query):
    if query is not None:
      if query=='999':
        categories=[]
      else:
        categories=getdata(query)
        print "***********************************"
        print categories[0]
        print "***********************************"
    return render_template('index.html',categories=categories)


if __name__ == "__main__":
    global name
    global email
    global radio
    global colorbox
    #db.drop_all()
    #db.create_all()
    app.run()











