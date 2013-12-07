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

#SQLALCHEMY_DATABASE_URI = 'mysql://nlp_user:nlp_user@localhost/stackoverflow'

SQLALCHEMY_DATABASE_URI='sqlite:///tutorial.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


#SQLALCHEMY_DATABASE_URI = 'mysql://nlp_user:nlp_user@localhost/stackoverflow'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutorial.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
#engine = create_engine(SQLALCHEMY_DATABASE_URI,
#                       convert_unicode=True,
#                       pool_recycle=7200,
#                       paramstyle='format')

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
      
      results={}
      for k,v in categories.items():
        ques_ans=[]
        try:
          res = engine.execute("select q.ques_text,q.answer_id from ngrams n join questions\
          q on n.questionid=q.id where n.lemmangrams='{}'".format(k))
          for r in res:
            ans_id=str(r['answer_id'])
            ans_text=engine.execute("select answer_text from answers where id='{}'".format(ans_id))
            ques_ans.append([str(r['ques_text'])],ans_text)
        except UnicodeEncodeError:
          continue  
        results[k]=(ques_ans,v)
      return (parent,children,grand),results


@app.route('/data', methods=['GET', 'POST'])
def data():
    #print "here inside data"
    list_name = request.args.get("input_value")
    cat = getdata()
    #print "listname"
    #print list_name
    #print "/listname"
    return render_template('index.html',categories=cat)

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

