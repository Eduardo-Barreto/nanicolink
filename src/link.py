from time import time

class Link():
    def __init__(self, _long_url: str = '', _keyword: str = '', _tags: list = [], _destroy_clicks: int = 0, _destroy_time: int = 0):
        self.long_url = _long_url
        self.keyword = _keyword
        self.clicks = 0
        self.destroy_clicks = _destroy_clicks
        self.tags = ['all'] + _tags
        self.date_created = time()
        self.destroy_time = _destroy_time*60*60*24

    def load_json(self, json: dict):
        self.keyword = list(json.keys())[0]
        json = json.get(self.keyword)
        self.long_url = json['long_url']
        self.clicks = json['clicks']
        self.destroy_clicks = json['destroy_clicks']
        self.tags = json['tags']
        self.date_created = json['date_created']
        self.destroy_time = json['destroy_time']

    def to_dict(self):
        return {
            self.keyword: {
                'long_url': self.long_url,
                'clicks': self.clicks,
                'destroy_clicks': self.destroy_clicks,
                'tags': self.tags,
                'date_created': self.date_created,
                'destroy_time': self.destroy_time
            }
        }