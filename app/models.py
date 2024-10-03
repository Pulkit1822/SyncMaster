# Import the necessary SQLAlchemy modules
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create a Base class that will be used to define the structure of our database tables
Base = declarative_base()

# Define a class to represent the users table
class User(Base):
    # Specify the name of the table
    __tablename__ = 'users'
    
    # Define the columns of the table
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    
    # Define a relationship between the User class and the Post class
    posts = relationship('Post', back_populates='author')

# Define a class to represent the posts table
class Post(Base):
    # Specify the name of the table
    __tablename__ = 'posts'
    
    # Define the columns of the table
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Define a relationship between the Post class and the User class
    author = relationship('User', back_populates='posts')

# Example of creating an SQLite database and tables
if __name__ == "__main__":
    # Create an engine that will be used to create the database
    engine = create_engine('sqlite:///example.db')
    
    # Create all the tables in the database
    Base.metadata.create_all(engine)
