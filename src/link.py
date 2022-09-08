from time import time
from string import ascii_letters, digits
from random import seed, choice


class Link:
    def __init__(
        self,
        long_url: str = '',
        keyword: str = '',
        tags: list = [],
        destroy_clicks: int = 0,
        destroy_time: int = 0,
    ):
        '''
        Construtor da classe Link

        Parâmetros
        ----------
        long_url: str
            URL longa a ser encurtada

        keyword: str
            Palavra-chave para a URL encurtada

        tags: list
            Lista de tags para a URL encurtada

        destroy_clicks: int
            Número de cliques para a URL encurtada ser destruída
            (0 para não destruir)

        destroy_time: int
            Tempo em dias para a URL encurtada ser destruída (0 para nunca)
        '''
        self.long_url = long_url
        self.keyword = keyword
        self.clicks = 0
        self.destroy_clicks = destroy_clicks
        self.tags = ['all'] + tags
        self.date_created = time()
        self.destroy_time = destroy_time
        self.validate_link()

    def load_db_json(self, json: dict) -> None:
        '''
        Carrega os valores de um dicionário (da db) para a classe

        Parâmetros
        ----------
        json: dict
            Dicionário com os valores a serem carregados
        '''
        self.keyword = list(json.keys())[0]
        json = json.get(self.keyword)
        self.long_url = json.get('long_url')
        self.clicks = json.get('clicks', 0)
        self.destroy_clicks = json.get('destroy_clicks', 0)
        self.tags = json.get('tags', ['all'])
        self.date_created = json.get('date_created', time())
        self.destroy_time = json.get('destroy_time', 0)
        self.validate_link()

    def to_dict(self) -> dict:
        '''
        Retorna um dicionário com os valores da classe

        Retorno
        -------
        dict
            Dicionário com os valores da classe
        '''
        return {
            self.keyword: {
                'long_url': self.long_url,
                'clicks': self.clicks,
                'destroy_clicks': self.destroy_clicks,
                'tags': self.tags,
                'date_created': self.date_created,
                'destroy_time': self.destroy_time,
            }
        }

    def generate_keyword(self) -> None:
        '''
        Gera uma keyword para a URL encurtada baseada na URL longa
        '''
        seed(self.long_url+str(time()))
        self.keyword = ''.join(choice(ascii_letters + digits)
                               for i in range(8))

    def validate_link(self):
        '''
        Valida as informações do link
            keyword não pode estar vazia
            destroy_time não pode ser negativo
            destroy_clicks não pode ser negativo
        '''
        if self.keyword == '':
            self.generate_keyword()

        if self.destroy_time < 0:
            self.destroy_time = 0

        if self.destroy_clicks < 0:
            self.destroy_clicks = 0
