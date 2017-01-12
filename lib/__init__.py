# -*- coding: utf-8 -*-
from pyramid.config import Configurator


from pyramid.session import SignedCookieSessionFactory
from sqlalchemy import inspect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Deny
from pyramid.security import Authenticated
from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from models import *

my_session_factory = SignedCookieSessionFactory('itsaseekreet')

class MyFactory(object):
	def __init__(self, request):
		self.__acl__ = [(Allow, Authenticated, "add")]

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    Base.metadata.create_all()
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'lib')

    config = Configurator(root_factory=MyFactory, settings=settings, session_factory=my_session_factory)
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static')



    config.add_route("index","/")
    config.add_route("logOut","logOut")
    config.add_route("registerUser","/registerUser")
    config.add_route("registerLib","/registerLib")

    config.add_route("indexLib","/indexLib")
    config.add_route("indexUser","/indexUser")

    config.add_route("addBook", "addBook")
    config.add_route("editBook", "editBook/{id}")
    config.add_route("deleteBook", "deleteBook/{id}")


    #авторизация и аутентификация
    authn_policy = AuthTktAuthenticationPolicy('sosecret', hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    config.scan()

    return config.make_wsgi_app()
