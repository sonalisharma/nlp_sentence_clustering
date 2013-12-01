from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from nltk.stem import WordNetLemmatizer as WNL
from models import LemmaTemp, Base


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models_p
    Base.metadata.create_all(bind=engine)
    print Base.metadata.tables.keys()
    print Base.metadata.reflect(engine)

def insert_db():
    entries=[('dogs',1),('cats',2),('jumping',3),('happened',4),('best',5),('worst',6)]
    wnl=WNL()
    for e in entries:
        original=e[0]
        lemma=wnl.lemmatize(original)
        wordid=e[1]
        l=LemmaTemp(lemma,original,wordid)
        db_session.add(l)
	db_session.commit()

if __name__=='__main__':
    SQLALCHEMY_DATBASE_URI='sqlite:///tutorial.db'
    engine = create_engine(SQLALCHEMY_DATBASE_URI, convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    Base.query = db_session.query_property()
    init_db()
    insert_db()