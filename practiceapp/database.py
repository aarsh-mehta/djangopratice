from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+mysqlconnector://root:abcdpwd@localhost/practice')
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
