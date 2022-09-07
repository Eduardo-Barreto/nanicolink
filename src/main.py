from cgi import test
from webbrowser import get
from link import *
from database import *
from os import environ
db = Database(environ['databaseURL'])

print(db.create_link(Link('https://google.com', 'google', ['all'], 0, 0)))
print(db.get_link_by_keyword('google').long_url)
