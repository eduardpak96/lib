from sqlalchemy import create_engine,Table,Column,MetaData,Integer,String,ForeignKey,Date,Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship
import os

#if os.path.exists("lib.db"):
    #os.remove("lib.db")

engine = create_engine('sqlite:///lib.db')
Session = sessionmaker()
Base = declarative_base(bind=engine)

class User(Base):
     __tablename__ = "Users"
     Login = Column(String, nullable = False,primary_key = True)
     Password = Column(String, nullable = False)
     FirstName = Column(String, nullable = False)
     SecondName = Column(String, nullable = False)
     def __init__(self, Login, Password, FirstName, SecondName):
          self.Login = Login
          self.Password = Password
          self.FirstName = FirstName
          self.SecondName = SecondName

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.FirstName + " " +self.SecondName 

class Lib(Base):
     __tablename__ = "Lib"
     id = Column(Integer, nullable = False, primary_key = True)
     Login = Column(String, nullable = False)
     Password = Column(String, nullable = False)
     Name = Column(String, nullable = False)
     Address = Column(String, nullable = False)
     def __init__(self, Login, Password, Name, Address):
          self.Login = Login
          self.Password = Password
          self.Name = Name
          self.Address = Address

     def __repr__(self):
          return self.Login + " " + self.Password + " " + self.Name + " " +self.Address 

class Book(Base):
     __tablename__= "Books"
     id = Column(Integer, nullable = False, primary_key = True)
     Name = Column(String, nullable = False)
     Autor = Column(String, nullable = False)
     Lib = Column(String, nullable = False)
     Picture = Column(String, nullable = False)
     Publishing_house = Column(String, nullable = False)
     Publishing_year = Column(String, nullable = False)
     def __init__(self, Name, Autor, Lib, Picture,  Publishing_house, Publishing_year):
          self.Name = Name
          self.Autor = Autor
          self.Lib = Lib
          self.Picture = Picture
          self.Publishing_house = Publishing_house
          self.Publishing_year = Publishing_year
          
     def __repr__(self):
          return self.Name + " " + self.Autor + " " + self.Lib
