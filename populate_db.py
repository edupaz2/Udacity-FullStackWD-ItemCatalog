from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Drill, User, Base

engine = create_engine('sqlite:///drills.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Populate DB with categories
def populateCategory(n):
    if len(session.query(Category).filter_by(name=n).all()) == 0:
        category_item = Category(name=n)
        session.add(category_item)
        session.commit()


def populateDB():
    populateCategory('Offensive')
    populateCategory('Defensive')
    populateCategory('Forward')
    populateCategory('Defenseman')
    populateCategory('Goalie')
    populateCategory('Warm-up')
    populateCategory('Shooting')
    populateCategory('Passing')
    populateCategory('Power Play')
    populateCategory('Penalty Killing')
    populateCategory('Fun games')
    populateCategory('Conditioning')

if __name__ == '__main__':
    populateDB()