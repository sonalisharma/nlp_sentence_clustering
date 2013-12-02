from xml.dom import minidom  # read XML file
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from BeautifulSoup import BeautifulSoup
import string  # for removing punctuations
from models import Base
import logging
logging.root.setLevel(logging.DEBUG)
import xml.etree.cElementTree as cElementTree

SQLALCHEMY_DATABASE_URI = 'sqlite:///tutorial_pp2.db'
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()
Base.metadata.create_all(bind=engine)

XML_files = ['posts.xml']

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
    return ' '.join([word for word in sentence.split() if word.lower() not in cached_stop_words])


def clean_answers():
    from models import Questions
    for ques in session.query(Questions).all():
        print ques.id
        clean_html_answer = clean_html(ques.answer_text)
        wo_punctuation_answer = remove_punctuation(clean_html_answer)
        wo_stop_words_answer = remove_stop_words(wo_punctuation_answer)
        ques.answer_text = unicode(wo_punctuation_answer, 'utf8')
        ques.answer_wo_stop_words = unicode(wo_stop_words_answer, 'utf8')
    session.commit()


# __DEPRECATED__
def insert_data():
    from models import Questions
    #from models import Answers
    for ques in session.query(Questions).filter(Questions.ques_id <= 100):
        clean_html_answer = clean_html(ques.answer_text)
        wo_punctuation_answer = remove_punctuation(clean_html_answer)
        wo_stop_words_answer = remove_stop_words(wo_punctuation_answer)
        ques.answer_text = unicode(wo_stop_words_answer, 'utf8')
        session.commit()
        print ques.answer_text


def read_xml():
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
            if i > 20000:
                session.commit()
                i = 0
            else:
                i = i+1
        session.commit()

'''

        xml_doc = minidom.parse(to_read_file)
        logging.debug("xml_doc = minidom.parse(to_read_file)")
        item_list = xml_doc.getElementsByTagName('row')
        logging.debug("xml_doc.getElementsByTagName row")
        for post in item_list:
            logging.debug("for post in item_list")
            if int(post.attributes['PostTypeId'].value) == 1:  # is a questions
                try:
                    post.attributes['AcceptedAnswerId']
                    print post.attributes['Id'].value
                    q = Questions(ques_id=int(post.attributes['Id'].value),
                                  ques_text=post.attributes['Title'].value,
                                  answer_id=post.attributes['AcceptedAnswerId'].value)
                    session.add(q)
                    session.commit()
                except:  # is an answer
                    pass
            elif int(post.attributes['PostTypeId'].value) == 2:
                try:
                    print post.attributes['Id'].value
                    a = Answers(ans_id=int(post.attributes['Id'].value),
                                ans_text=post.attributes['Body'].value)
                    session.add(a)
                    session.commit()
                except:
                    pass
'''


def merge_tables():
    from models import Questions
    from models import Answers
    for ques in session.query(Questions).all():
        print ques.id
        ans = session.query(Answers).filter(Answers.id == ques.answer_id).first()
        if ans:
            ques.answer_text = ans.answer_text
            ques.answer_wo_stop_words = ans.answer_wo_stop_words
        else:
            session.delete(ques)
    session.query(Answers).all().delete()  # reduce the size of the db
    session.commit()

if __name__ == "__main__":
    read_xml()
    #merge_tables()
    #clean_answers()
