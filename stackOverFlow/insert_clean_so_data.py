from sqlalchemy import create_engine, MetaData, update, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BeautifulSoup import BeautifulSoup

SQLALCHEMY_DATABASE_URI = 'sqlite:///tutorial.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

Base.metadata.create_all(bind=engine)

VALID_TAGS = ['p', 'a', 'h2', 'blockquote', 'hr', 'em', 'strong']
INVALID_TAGS = ['CODE', 'ul', 'ol', 'pre']
"""
unhandled tags:

"""


def clean_html(value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        if tag.name in VALID_TAGS:
            tag.hidden = True
        if tag.name in INVALID_TAGS:
            tag.replaceWith('')
    return soup.renderContents()


def insert_data():
    from models import Questions
    for ques in session.query(Questions).order_by(Questions.ques_id):
        clean_answer = clean_html(ques.answer_text)
        #print clean_answer
        ques.answer_text = unicode(clean_answer, 'utf8')
        session.commit()
        #update(Questions).where(Questions.c.ques_id == ques.ques_id).values(answer_text=clean_answer)
        #db_session.commit()
        print ques.ques_id

if __name__ == "__main__":
    insert_data()
