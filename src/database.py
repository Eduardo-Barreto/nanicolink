import requests
from json import dumps

from link import *

class Database():
    def __init__(self, url):
        self.url = url

    def _clear_database_(self):
        clear_request = requests.delete(f'{self.url}/links/.json')
        return clear_request.status_code

    def json_to_link(self, json: dict) -> Link:
        object_link = Link()
        object_link.load_json(json)
        return object_link

    def get_all_links(self) -> list:
        links = requests.get(f'{self.url}/links/.json')
        list_links = []
        for link in links.json():
            list_links.append(self.json_to_link({link: links.json()[link]}))

        return list_links

    def get_link_by_keyword(self, keyword: str) -> Link:
        link = requests.get(f'{self.url}/links/{keyword}/.json')
        return self.json_to_link({keyword: link.json()})

    def get_link_by_long(self, long: str) -> Link:
        links = self.get_all_links()
        for link in links:
            if link.long_url == long:
                return link

    def get_links_by_tag(self, tag: str) -> list:
        links = self.get_all_links()
        links_with_tag = []
        for link in links:
            if tag in link.tags:
                links_with_tag.append(link)
        return links_with_tag

    def create_link(self, link: Link):
        keyword = link.keyword
        link_data = link.to_dict()
        link_data = link_data.get(keyword)
        create_request = requests.put(f'{self.url}/links/{keyword}/.json', data=dumps(link_data))
        return create_request.status_code

    def save_link(self, link: Link):
        keyword = link.keyword
        link_data = link.to_dict()
        link_data = link_data.get(keyword)
        save_request = requests.patch(f'{self.url}/links/{keyword}/.json', data=dumps(link_data))
        return save_request.status_code