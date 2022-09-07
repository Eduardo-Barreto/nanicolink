from cgi import test
from webbrowser import get
from link import *
from database import *
from os import environ
db = Database(environ['databaseURL'])

test_links = [
    Link('https://google.com', 'google', ['search', 'google'], 0, 0),
    Link('https://youtube.com', 'youtube', ['video', 'youtube'], 0, 0),
    Link('https://github.com', 'github', ['code', 'github'], 0, 0),
    Link('https://stackoverflow.com', 'stackoverflow', ['code', 'stackoverflow'], 0, 0),
    Link('https://reddit.com', 'reddit', ['social', 'reddit'], 0, 0),
    Link('https://twitter.com', 'twitter', ['social', 'twitter'], 0, 0),
    Link('https://facebook.com', 'facebook', ['social', 'facebook'], 0, 0),
    Link('https://instagram.com', 'instagram', ['social', 'instagram'], 0, 0),
    Link('https://twitch.tv', 'twitch', ['video', 'twitch'], 0, 0),
    Link('https://netflix.com', 'netflix', ['video', 'netflix'], 0, 0),
    Link('https://amazon.com', 'amazon', ['shopping', 'amazon'], 0, 0),
    Link('https://wikipedia.org', 'wikipedia', ['search', 'wikipedia'], 0, 0)
]

for link in test_links:
    db.create_link(link)


social_tag = db.get_links_by_tag('social')

for link in social_tag:
    print(link.keyword)
