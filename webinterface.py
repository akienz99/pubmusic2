import cherrypy

class webInterface:
   
   def __init__(self):
      cherrypy.quickstart(webContent())

class webContent(object):
   def index(self):
      return "Hello World!"
   
