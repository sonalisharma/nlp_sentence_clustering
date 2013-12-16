# This file is used for front end application

import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import render_template
from werkzeug import secure_filename
from flask import Flask, request, redirect, url_for
from flask import send_from_directory   
from sqlalchemy import distinct, Table
from itertools import izip
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session,sessionmaker
from processing import fetchphrases
from flask import json
import re

app = Flask(__name__)


SQLALCHEMY_DATABASE_URI='sqlite:///tutorial.db'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI



engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)


db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

db = SQLAlchemy(app)
eng = db.create_engine(SQLALCHEMY_DATABASE_URI)

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
    if query is not None:
      parent,children,grand=fetchphrases(query)
      #Parents Dict: category:freq Children dict: parent_cat:[category:freq], Grand dict : child_cat:[category:freq]
      parentcategories={}
      childcategories={}
      grandcategories={}
      categories = {}
      #Search for each category in ngrams.lemmangrams, get question ids from ngrams 
      #and question text from questions table

      for phrase,freq in parent.items():
        try:
          categories[str(phrase)]=freq
        except UnicodeEncodeError:
          categories[phrase]=freq
      return (parent,children,grand)


@app.route('/data', methods=['GET', 'POST'])
def data():
    varhtml = ""
    data = json.loads(request.form.get('data'))
    phrase_data = data['value']

    results={}
    for p in phrase_data:
      newphrase = " ".join(str(p).split("_"))
      ques_ans=[]
      ques_list=[]
      try:

        res = engine.execute("select q.ques_text,q.id,q.answer_text from ngrams n join questions\
        q on n.questionid=q.id where n.lemmangrams='{}'".format(newphrase))

        for r in res.fetchall():
          ques_id = re.sub(r"[\n\t\r]", " ",str(r['id']))
          ques_text = re.sub(r"[\n\t\r]", " ",str(r['ques_text']))
          ans_text = re.sub(r"[\n\t\r]", " ",str(r['answer_text']))
          if ques_id in ques_list:
            pass
          else:
            ques_list.append(ques_id)
            ques_ans.append([ques_id,ques_text,ans_text])
          results[str(newphrase)]=list(ques_ans)
      except UnicodeEncodeError:
        print "Caught in an exception"
        continue  
    
    for r in results.keys():
      divid = r.replace(" ","_")
      varhtml= varhtml+"<div id=\""+divid+"\" >"
      for questions in results[r]:
        varhtml=varhtml+"<div id =\""+questions[0]+"_question\" style=\"cursor:pointer;\" onclick=\"show(\'"+questions[0]+"\')\"><h4>"+questions[1]+"</h4></div>\
        <div id =\""+questions[0]+"_ans\" style=\"display:none; font-size:14px;margin-left:15px;\">"+questions[2]+"</div></div>"

    return  varhtml

@app.route('/results/<query>')
def getresults(query):
    if query is not None:
      if query=='999':
        categories=[]
      else:
        categories=getdata(query)
    return render_template('index.html',categories=categories)


if __name__ == "__main__":
    app.run()











