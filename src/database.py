from webbrowser import get
import requests
import json

from link import *

class Database():
    def __init__(self, url):
        self.url = url
        _connection = requests.get(self.url)

    def json_to_link(self, json: dict) -> Link:
        object_link = Link()
        object_link.load_json(json)
        return object_link

    def get_all_links(self) -> dict:
        links = requests.get(f'{self.url}/links.json')
        return links.json()

    def get_link_by_keyword(self, keyword: str) -> Link:
        link = requests.get(f'{self.url}/links/{keyword}.json')
        return self.json_to_link({keyword: link.json()})

    def get_link_by_long(self, long: str) -> Link:
        links = self.get_all_links()
        for link in links:
            if links[link]["long_url"] == long:
                return self.json_to_link({link: links[link]})

    def create_link(self, link: Link):
        link_data = link.to_dict()
        keyword = list(link_data)[0]
        link_data = link_data.get(keyword)
        print(link_data)
        create_request = requests.put(f'{self.url}/links/{keyword}/.json', data=json.dumps(link_data))
        return create_request.status_code