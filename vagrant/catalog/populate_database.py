from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Genre, Movie

## Note: some of the comments below are verbatim from lesson 3 of the Full Stack Foundations course by Udacity
## They were too good not to leave in

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Populate our comedies
Genre1 = Genre(name="Comedy")

session.add(Genre1)
session.commit()

Comedy1 = Movie(name="Dumb and Dumber", genre=Genre1)

session.add(Comedy1)
session.commit()

Comedy2 = Movie(name="Earnest Goes to Camp", genre=Genre1)

session.add(Comedy2)
session.commit()

Comedy3 = Movie(name="Police Academy", genre=Genre1)

session.add(Comedy3)
session.commit()

# Populate our dramas
Genre2 = Genre(name="Drama")

session.add(Genre2)
session.commit()

Drama1 = Movie(name="The Verdict", genre=Genre2)

session.add(Drama1)
session.commit()

Drama2 = Movie(name="The Godfather", genre=Genre2)

session.add(Drama2)
session.commit()

Drama3 = Movie(name="The Deer Hunter", genre=Genre2)

session.add(Drama3)
session.commit()


print "added movies to catalog!"
