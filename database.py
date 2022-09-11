import requests
from json import dumps

from link import Link


class Database:
    def __init__(self, url):
        '''
        Construtor da classe Database

        Parâmetros
        ----------
        url: str
            URL do banco de dados
        '''
        self.url = url

    def _clear_database_(self) -> int:
        '''
        Limpa o banco de dados

        Retorno
        -------
        status_code: int
            Código de status da requisição
        '''
        clear_request = requests.delete(f'{self.url}/links/.json')
        return clear_request.status_code

    def json_to_link(self, json: dict) -> Link:
        '''
        Converte um dicionário para um objeto Link

        Parâmetros
        ----------
        json: dict
            Dicionário a ser convertido

        Retorno
        -------
        link: Link
            Objeto Link convertido
        '''
        object_link = Link()
        object_link.load_db_json(json)
        return object_link

    def get_all_links(self) -> list:
        '''
        Retorna uma lista com todos os links do banco de dados

        Retorno
        -------
        links: list
            Lista com todos os links do banco de dados
        '''
        links = requests.get(f'{self.url}/links/.json')
        list_links = []
        for link in links.json():
            list_links.append(self.json_to_link({link: links.json()[link]}))

        return list_links

    def get_link_by_keyword(self, keyword: str) -> Link:
        '''
        Retorna um link relacionado a uma keyword

        Parâmetros
        ----------
        keyword: str
            Keyword do link

        Retorno
        -------
        link: Link
            Link relacionado a keyword
        '''
        link = requests.get(f'{self.url}/links/{keyword}/.json')
        return self.json_to_link({keyword: link.json()})

    def get_link_by_long(self, long_url: str) -> Link:
        '''
        Retorna um link relacionado a uma URL longa

        Parâmetros
        ----------
        long: str
            URL longa do link

        Retorno
        -------
        link: Link
            Link relacionado a URL longa
        '''
        links = self.get_all_links()
        for link in links:
            if link.long_url == long_url:
                return link

    def get_links_by_tag(self, tag: str) -> list:
        '''
        Retorna uma lista com todos os links relacionados a uma tag

        Parâmetros
        ----------
        tag: str
            Tag a ser procurada

        Retorno
        -------
        links: list
            Lista com todos os links relacionados a tag
        '''
        links = self.get_all_links()
        links_with_tag = []
        for link in links:
            if tag in link.tags:
                links_with_tag.append(link)
        return links_with_tag

    def keyword_exists(self, keyword: str) -> bool:
        '''
        Verifica se uma keyword já existe no banco de dados

        Parâmetros
        ----------
        keyword: str
            Keyword a ser verificada

        Retorno
        -------
        exists: bool
            True se a keyword já existe, False caso contrário
        '''
        link = requests.get(f'{self.url}/links/{keyword}/.json')
        return link.status_code == 200 and link.json() is not None

    def create_link(self, link: Link) -> int:
        '''
        Cria um link no banco de dados

        Parâmetros
        ----------
        link: Link
            Link a ser criado

        Retorno
        -------
        status_code: int
            Código de status da requisição
        '''
        keyword = link.keyword
        link_data = link.to_dict()
        link_data = link_data.get(keyword)
        create_request = requests.put(
            f'{self.url}/links/{keyword}/.json', data=dumps(link_data)
        )
        return create_request.status_code

    def save_link(self, link: Link) -> int:
        '''
        Salva (atualiza) um link no banco de dados

        Parâmetros
        ----------
        link: Link
            Link a ser salvo

        Retorno
        -------
        status_code: int
            Código de status da requisição
        '''
        keyword = link.keyword
        link_data = link.to_dict()
        link_data = link_data.get(keyword)
        save_request = requests.patch(
            f'{self.url}/links/{keyword}/.json', data=dumps(link_data)
        )
        return save_request.status_code

    def delete_link(self, link: Link) -> int:
        '''
        Deleta um link no banco de dados

        Parâmetros
        ----------
        link: Link
            Link a ser deletado

        Retorno
        -------
        status_code: int
            Código de status da requisição
        '''

        keyword = link.keyword
        save_request = requests.delete(f'{self.url}/links/{keyword}/.json')
        return save_request.status_code
