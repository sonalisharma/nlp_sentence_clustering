from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BeautifulSoup import BeautifulSoup
import string  # for removing punctuations
from models import Base
import logging
logging.root.setLevel(logging.DEBUG)
import xml.etree.cElementTree as cElementTree


## Creating database connections
# SQLALCHEMY_DATABASE_URI = 'sqlite:///tutorial_pp2.db'
SQLALCHEMY_DATABASE_URI = 'mysql://nlp_user:nlp_user@localhost/stackoverflow'

engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True, pool_size=100, pool_recycle=7200)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(bind=engine)

## raw data files:
XML_files = ['posts.xml']

## HTML Tags to keep and remove
VALID_TAGS = ['p', 'a', 'h2', 'blockquote', 'hr', 'em', 'strong']
INVALID_TAGS = ['CODE', 'ul', 'ol', 'pre']


## stop words
stop_word_file = "ir_dcs_gla_ac_uk_stop_words.txt"
cached_stop_words = []

## populate the stop word list
with open(stop_word_file) as f:
    contents = f.readlines()
    for word in contents:
        cached_stop_words.append(word.strip())


def clean_html(value):
    """
    remove INVALID_TAGS tags and keep the data for VALID_TAGS
    """
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
    return ' '.join([word for word in sentence.split() if word.lower() not in cached_stop_words])


def clean_answers():
    """
    Cleans up answer text and
    if the questions does not have an answer, delete it
    """
    from models import Questions
    for ques in session.query(Questions).all():
        logging.debug(ques.id)
        if ques.answer_text:
            clean_html_answer = clean_html(ques.answer_text)
            wo_punctuation_answer = remove_punctuation(clean_html_answer)
            wo_stop_words_answer = remove_stop_words(wo_punctuation_answer)
            ques.answer_text = unicode(wo_punctuation_answer, 'utf8')
            ques.answer_wo_stop_words = unicode(wo_stop_words_answer, 'utf8')
        else:
            session.delete(ques)
    session.commit()


# __DEPRECATED__
def insert_data():
    from models import Questions
    #from models import Answers
    for ques in session.query(Questions).filter(Questions.ques_id <= 100):
        logging.debug(ques.id)
        if ques.answer_text:
            clean_html_answer = clean_html(ques.answer_text)
            wo_punctuation_answer = remove_punctuation(clean_html_answer)
            wo_stop_words_answer = remove_stop_words(wo_punctuation_answer)
            ques.answer_text = unicode(wo_stop_words_answer, 'utf8')
        else:
            session.delete(ques)
    session.commit()


def read_xml():
    """
    read the xml file
    add question and answers to the database
    """
    logging.debug("read_xml entered")
    from models import Questions
    from models import Answers
    logging.debug("models imported")
    for to_read_file in XML_files:
        logging.debug("reading file: to_read_file")
        i = 0
        for event, elem in cElementTree.iterparse(to_read_file):
            if elem.tag == "row":
                logging.debug("element has row")
                if int(elem.attrib['PostTypeId']) == 1:
                    try:
                        elem.attrib['AcceptedAnswerId']
                        logging.debug(elem.attrib['Id'])
                        q = Questions(ques_id=int(elem.attrib['Id']),
                                      ques_text=elem.attrib['Title'],
                                      answer_id=elem.attrib['AcceptedAnswerId'])
                        session.add(q)
                    except:
                        pass
                elif int(elem.attrib['PostTypeId']) == 2:
                    try:
                        logging.debug(elem.attrib['Id'])
                        a = Answers(ans_id=int(elem.attrib['Id']),
                                    ans_text=elem.attrib['Body'])
                        session.add(a)
                    except:
                        pass
            elem.clear()
            if i > 200:
                session.commit()
                i = 0
            else:
                i =+ 1
        session.commit()


def merge_tables():
    """
    add answers to the questions table
    """
    from models import Questions
    from models import Answers
    commit_counter = 0
    for ques in session.query(Questions).all():
        logging.debug(ques.id)
        ans = session.query(Answers).filter(Answers.id == ques.answer_id).first()
        if ans:
            ques.answer_text = ans.answer_text
            ques.answer_wo_stop_words = ans.answer_wo_stop_words
        else:
            session.delete(ques)
        if commit_counter > 200:
            session.commit()
            commit_counter = 0
        else:
            commit_counter += 1
    session.commit()


def delete_extras():
    """
    Delete the answer table after all the data has been extracted from it
    """
    from models import Answers
    session.query(Answers).delete()
    session.commit()


if __name__ == "__main__":
    read_xml()
    merge_tables()
    delete_extras()
    clean_answers()
