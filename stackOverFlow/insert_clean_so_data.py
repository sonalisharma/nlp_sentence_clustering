from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BeautifulSoup import BeautifulSoup
import string  # for removing punctuations

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

# reading stop words
stop_word_file = "ir_dcs_gla_ac_uk_stop_words.txt"
cached_stop_words = []

with open(stop_word_file) as f:
    contents = f.readlines()
    for word in contents:
        cached_stop_words.append(word.strip())


def clean_html(value):
    soup = BeautifulSoup(value)
    for tag in soup.findAll(True):
        if tag.name in VALID_TAGS:
            tag.hidden = True
        if tag.name in INVALID_TAGS:
            tag.replaceWith('')
    return soup.renderContents()


def remove_punctuation(sentence):
    return sentence.translate(string.maketrans("",""), string.punctuation)


def remove_stop_words(sentence):
    return ' '.join([word for word in sentence.split() if word not in cached_stop_words])


def insert_data():
    from models import Questions
    for ques in session.query(Questions).order_by(Questions.ques_id):
        clean_html_answer = clean_html(ques.answer_text)
        wo_punctuation_answer = remove_punctuation(clean_html_answer)
        wo_stop_words_answer = remove_stop_words(wo_punctuation_answer)
        ques.answer_text = unicode(wo_stop_words_answer, 'utf8')
        session.commit()
        print ques.ques_id

if __name__ == "__main__":
    insert_data()
