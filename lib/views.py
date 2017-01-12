# -*- coding: utf-8 -*-
'''from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('lib')
'''

from pyramid.view import view_config
from pyramid.response import Response
from models import *
import re

import uuid
import shutil

from pyramid.security import (
remember,
forget,
)

from pyramid.httpexceptions import (
HTTPFound,
HTTPNotFound,
)

@view_config(route_name='indexUser', renderer='templates/indexUser.jinja2', permission = 'add')
def indexUser(request):
	session = Session(bind = engine)
	if(request.method == "POST"):
		name = request.params['name']
		autor = request.params['autor']
		publishing_house = request.params['publishing_house']
		publishing_year = request.params['publishing_year']
		lib = request.params['lib']
		books = session.query(Book)
		if(name != ""):
			books = books.filter(Book.Name.like('%'+name+'%'))
		if(autor != ""):
			books = books.filter(Book.Autor.like('%' + autor + '%'))
		if(publishing_house != ""):
			books = books.filter(Book.Publishing_house.like('%' + publishing_house + '%'))
		if(publishing_year != ""):
			books = books.filter(Book.Publishing_year.like('%' + publishing_year + '%'))
		if(lib != "-1"):
			lib_name = session.query(Lib).filter_by(id = lib).first().Name
			books = books.filter_by(Lib = lib_name)
		return { 'username': request.authenticated_userid , 
				 'books' : books.all(),
				 'name' : name,
				 'autor' : autor,
				 'publishing_house' : publishing_house,
				 'publishing_year' : publishing_year,
				 'libs' : session.query(Lib).all()}
	else:
		return { 'username': request.authenticated_userid , 
				 'books' : session.query(Book).all(),
				 'libs' : session.query(Lib).all()}
	



@view_config(route_name='editBook', renderer='templates/editBook.jinja2', permission = 'add')
def editBook(request):
	id = request.matchdict['id']
	session = Session(bind = engine)
	book = session.query(Book).filter_by(id = id).first()
	if request.method == "GET":
		return { 'username': request.authenticated_userid , 'book' : book}
	else:
		book.Name = request.params['name']
		book.Autor = request.params["autor"]
		book.Publishing_house = request.params['publishing_house']
		book.Publishing_year = request.params['publishing_year']
		session.commit()
		return HTTPFound(location = request.route_url("indexLib", _query = {"username" : request.authenticated_userid}))

@view_config(route_name='deleteBook', permission = 'add')
def deleteBook(request):
	session = Session(bind = engine)
	book = session.query(Book).filter_by(id  = request.matchdict['id']).first()
	session.delete(book)
	session.commit()
	return HTTPFound(location = request.route_url("indexLib", _query = {"username" : request.authenticated_userid}))

@view_config(route_name='addBook', renderer='templates/addBook.jinja2', permission = 'add')
def addBook(request):
	if request.method == "GET":
		return { 'username': request.authenticated_userid }
	else:
		session = Session(bind = engine)
		if(request.POST['picture']) != "":
			filename = request.POST['picture'].filename
			input_file = request.POST["picture"].file
			file_path = os.path.join( 'lib/static/images/uploads', filename)
			with open(file_path, 'wb') as output_file:
				shutil.copyfileobj(input_file, output_file)
			file_path = re.split(r'[/]', file_path, maxsplit = 1)[1]
		else:
			file_path = u"static/images/none.jpg"
		new_book = Book(Name = request.params["name"],
						Autor = request.params['autor'],
						Lib = session.query(Lib).filter_by(Login = request.authenticated_userid).first().Name,
						Picture = file_path,
						Publishing_house = request.params['publishing_house'],
						Publishing_year = request.params['publishing_year'])
		session.add(new_book)
		session.commit()
		return HTTPFound(location = request.route_url("indexLib", _query = {"username" : request.authenticated_userid}))

@view_config(route_name='indexLib', renderer='templates/indexLib.jinja2', permission = 'add')
def indexLib(request):
	session = Session(bind = engine)
	return { 'username': request.authenticated_userid , 'books' : session.query(Book).
				filter_by(Lib = session.query(Lib).filter_by(Login = request.authenticated_userid).first().Name).all()}

@view_config(route_name='logOut')
def logOut(request):
	headers = forget(request)
	return HTTPFound(location = '/', headers = headers)

@view_config(route_name='index', renderer='templates/index.jinja2')
def index(request):
	if request.method == "GET":
		if('good' in request.params):
			return { 'username': request.authenticated_userid, 'good' : request.params['good']}
		else:
			return { 'username': request.authenticated_userid }
	else:
		session = Session(bind = engine)
		login = request.params['login']
		password = request.params['password']
		user = session.query(User).filter_by(Login = login).first()
		lib = session.query(Lib).filter_by(Login = login).first()
		if user != None and user.Password == password:
			headers = remember(request, user.Login)			
			return HTTPFound(location = request.route_url('indexUser', _query = {"username" : request.authenticated_userid}), headers = headers)
		if lib != None and lib.Password == password:
			headers = remember(request, lib.Login)			
			return HTTPFound(location = request.route_url('indexLib', _query = {"username": request.authenticated_userid}), headers = headers)
		return { 'username': request.authenticated_userid, "error" : u"Введены не корректные данные" }

@view_config(route_name='registerUser', renderer='templates/registerUser.jinja2')
def registerUser(request):
	if request.method == 'POST':
		session = Session(bind=engine)
		errors = []
		if(len(request.params['firstName']) < 6):
			errors.append(u"Введите имя")
		if(len(request.params['secondName']) < 6):
			errors.append(u"Введите имя")
		if(len(request.params['login']) < 6):
			errors.append(u"Введите логин")
		if(len(request.params['login']) > 20):
			errors.append(u"Слишком длинный логин")
		if(len(request.params['password']) < 6):
			errors.append(u"Введите пароль")
		if(len(request.params['confirm']) < 6):
			errors.append(u"Введите подтверждение пароля")
		if(request.params['password']!= request.params['confirm']):
			errors.append(u'Пароли не совпадают')
		if(session.query(User).filter_by(Login=request.params['login']).count() != 0):
			errors.append(u'Такой логин уже существует')
		if(session.query(Lib).filter_by(Login=request.params['login']).count() != 0):
			errors.append(u'Такой логин уже существует')
		if(len(errors) != 0):
			return { 'errors' : errors ,
					 'firstName' : request.params['firstName'],
					 'secondName' : request.params['secondName'],
					 'login' : request.params['login'],
					 'username': request.authenticated_userid }
		else:
			new_user = User(Login = request.params['login'],
							Password = request.params['password'],
							FirstName = request.params['firstName'],
							SecondName = request.params['secondName'])
			session.add(new_user)
			session.commit()
			return HTTPFound(location = request.route_url('index', _query={'username': request.authenticated_userid,
																			'good' : "Вы успешно зарегестрировались"}))
	else:
		return { 'username': request.authenticated_userid }

@view_config(route_name='registerLib', renderer='templates/registerLib.jinja2')
def registerLib(request):
	if request.method == 'POST':
		session = Session(bind=engine)
		errors = []
		if(len(request.params['name']) < 6):
			errors.append(u"Введите название")
		if(len(request.params['address']) < 6):
			errors.append(u"Введите адресс")
		if(len(request.params['login']) < 6):
			errors.append(u"Введите логин")
		if(len(request.params['login']) > 20):
			errors.append(u"Слишком длинный логин")
		if(len(request.params['password']) < 6):
			errors.append(u"Введите пароль")
		if(len(request.params['confirm']) < 6):
			errors.append(u"Введите подтверждение пароля")
		if(request.params['password']!= request.params['confirm']):
			errors.append(u'Пароли не совпадают')
		if(session.query(User).filter_by(Login=request.params['login']).count() != 0):
			errors.append(u'Такой логин уже существует')
		if(session.query(Lib).filter_by(Login=request.params['login']).count() != 0):
			errors.append(u'Такой логин уже существует')
		if(session.query(Lib).filter_by(Name=request.params['name']).count() != 0):
			errors.append(u'Библиотека с таким названием уже существует')
		if(len(errors) != 0):
			return { 'errors' : errors ,
					 'name' : request.params['name'],
					 'address' : request.params['address'],
					 'login' : request.params['login'],
					 'username': request.authenticated_userid }
		else:
			new_user = Lib(Login = request.params['login'],
							Password = request.params['password'],
							Name = request.params['name'],
							Address = request.params['address'])
			session.add(new_user)
			session.commit()
			return HTTPFound(location = request.route_url('index', _query={'username': request.authenticated_userid,
																			'good' : "Вы успешно зарегестрировались"}))
	else:
		return { 'username': request.authenticated_userid }
