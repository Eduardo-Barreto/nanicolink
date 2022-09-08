from os import environ
import uvicorn
from fastapi import FastAPI, HTTPException, Body, Request
from starlette.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from time import time
from typing import Optional
from pydantic import BaseModel

from link import Link
from database import Database

db = Database(environ['databaseURL'])


def set_response(status_code, message):
    return {'status_code': status_code, 'message': message}


class LinkModel(BaseModel):
    long_url: str
    keyword: Optional[str] = ''
    tags: Optional[list] = []
    destroy_clicks: Optional[int] = 0
    destroy_time: Optional[int] = 0


app = FastAPI()


@app.get('/')
async def root():
    return set_response(200, 'Bem vindo! Página inicial')


@app.get('/{keyword}')
async def redirect(keyword: str):
    if not db.keyword_exists(keyword):
        raise HTTPException(
            404,
            f'Não foi possível encontrar um link com a keyword {keyword}'
        )

    link = db.get_link_by_keyword(keyword)
    link.clicks += 1
    db.save_link(link)

    if link.destroy_time > 0:
        if link.date_created + link.destroy_time*3600 <= time():
            try:
                db.delete_link(link)
            except Exception as e:
                raise HTTPException(500, 'Erro ao deletar link: ' + str(e))

            raise HTTPException(410, 'Link expirado')

    if link.destroy_clicks > 0 and link.clicks >= link.destroy_clicks:
        db.delete_link(link)

    return RedirectResponse(url=link.long_url)


@app.get('/{keyword}/details')
async def get_link_details(keyword: str):
    if not db.keyword_exists(keyword):
        raise HTTPException(
            404,
            f'Não foi possível encontrar um link com a keyword {keyword}'
        )

    try:
        link = db.get_link_by_keyword(keyword)
    except Exception as e:
        raise HTTPException(500, 'Erro ao buscar link: ' + str(e))

    return set_response(200, link)


@app.get('/tag/{tag}')
async def get_links_by_tag(tag: str):
    try:
        links = db.get_links_by_tag(tag)
    except Exception as e:
        raise HTTPException(500, 'Erro ao buscar links: ' + str(e))

    return set_response(200, links)


@app.put('/create')
async def create_link(
    link: LinkModel = Body(
        examples={
            "Normal": {
                "summary": "Cria um link padrão, sem personalização",
                "value": {
                    "long_url": "https://google.com",
                }
            },
            "totalmente personalizado": {
                "summary": "Cria um link totalmente personalizado",
                "value": {
                    "long_url": "https://google.com",
                    "keyword": "google",
                    "tags": ["search", "google"],
                    "destroy_clicks": 0,
                    "destroy_time": 0
                }
            }
        }
    )
):
    if db.keyword_exists(link.keyword):
        raise HTTPException(409, f'A keyword {link.keyword} já existe')

    link = Link(
        link.long_url,
        link.keyword,
        link.tags,
        link.destroy_clicks,
        link.destroy_time
    )
    try:
        db.create_link(link)
    except Exception as e:
        raise HTTPException(500, 'Erro ao criar link' + str(e))

    return set_response(201, 'Link criado com sucesso')


@app.delete('/delete')
async def delete_link(request: Request):
    keyword = await request.json()
    keyword = keyword.get('keyword')

    if not db.keyword_exists(keyword):
        raise HTTPException(
            404,
            f'Não foi possível encontrar um link com a keyword {keyword}'
        )

    link = db.get_link_by_keyword(keyword)
    try:
        db.delete_link(link)
    except Exception as e:
        raise HTTPException(500, 'Erro ao deletar link: ' + str(e))

    return set_response(200, 'Link deletado com sucesso')


def main():
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    uvicorn.run(app)


if __name__ == '__main__':
    main()
