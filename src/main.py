from time import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi import FastAPI, HTTPException, Body
import uvicorn
from sys import path
from os import environ

path.append('./src')

import models
from database import Database
from link import Link

db = Database(environ['databaseURL'])

HOST = 'https://nanicolink.herokuapp.com'


description = 'Pílulas de nanicolina para o seu link longo!'

app = FastAPI(title='Nanicolink', description=description)


@app.get(
    '/',
    summary='Redirecionamento GitHub',
    response_class=RedirectResponse,
    response_description='Redirecionamento para o repositório no GitHub',
    description='Redireciona para o repositório do projeto no GitHub'
)
async def root():
    return RedirectResponse(
        url='https://github.com/Eduardo-Barreto/nanicolink'
    )


@app.get(
    '/{keyword}',
    summary='Redireciona para um link',
    response_class=RedirectResponse,
    response_description='Redirecionamento para o link solicitado'
)
async def redirect(keyword: str) -> RedirectResponse:
    '''
    Redireciona para o link que foi encurtado

    - **keyword**: Apelido do link
    '''
    if not db.keyword_exists(keyword):
        raise HTTPException(
            status_code=404,
            detail='Não foi possível encontrar ' +
            f'um link com a keyword {keyword}'
        )

    link = db.get_link_by_keyword(keyword)
    link.clicks += 1
    db.save_link(link)

    if link.destroy_time > 0:
        if link.date_created + link.destroy_time*3600 <= time():
            try:
                db.delete_link(link)
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail='Erro ao deletar link: ' + str(e)
                )

            raise HTTPException(status_code=410, detail='Link expirado')

    if link.destroy_clicks > 0 and link.clicks >= link.destroy_clicks:
        db.delete_link(link)

    return RedirectResponse(url=link.long_url)


@app.get(
    '/details/',
    response_model=models.ResponseLink,
    summary='Retorna detalhes de um link encurtado',
    response_description='Detalhes do link',
)
async def get_link_details(keyword: str) -> Link:
    '''
    Retorna os detalhes de um link encurtado

    - **keyword**: keyword do link
    '''
    if not db.keyword_exists(keyword):
        raise HTTPException(
            status_code=404,
            detail='Não foi possível encontrar ' +
            f'um link com a keyword {keyword}'
        )

    try:
        link = db.get_link_by_keyword(keyword)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Erro ao buscar link: ' + str(e)
        )

    return JSONResponse(status_code=200, content=jsonable_encoder(link))


@app.get(
    '/tag/{tag}',
    summary='Retorna todos os links com uma tag específica',
    response_description='Links com a tag especificada',
    response_class=JSONResponse,
    response_model=list[models.ResponseLink]
)
async def get_links_by_tag(tag: str = 'all') -> JSONResponse:
    '''
    Retorna todos os links com uma tag específica

    - **tag**: tag dos links
    '''

    try:
        links = db.get_links_by_tag(tag)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Erro ao buscar links: ' + str(e)
        )

    return JSONResponse(status_code=200, content=jsonable_encoder(links))


@app.put(
    '/create',
    summary='Cria um link encurtado',
    response_class=Response
)
async def create_link(
    link: models.RequestLink = Body(
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
) -> Response:
    '''
    Cria um link encurtado

    - **long_url**: URL que será encurtada
    - **keyword**: Apelido do link
    - **tags**: Tags do link
    - **destroy_clicks**: Número de cliques para o link ser destruído
    - **destroy_time**: Tempo em horas para o link ser destruído
    '''
    link = Link(
        link.long_url,
        link.keyword,
        link.tags,
        link.destroy_clicks,
        link.destroy_time
    )

    if db.keyword_exists(link.keyword):
        raise HTTPException(
            status_code=409,
            detail=f'A keyword {link.keyword} já existe')

    try:
        db.create_link(link)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Erro ao criar link' + str(e)
        )

    return Response(
        status_code=201,
        content=f'Link com a keyword {link.keyword} criado com sucesso: ' +
        f'{HOST}/{link.keyword}'
    )


@app.delete('/delete')
async def delete_link(
    request: models.Keyword = Body(
        examples={
            "Normal": {
                "summary": "Deleta um link pela keyword",
                "value": {
                    "keyword": "google",
                }
            }
        }
    )
) -> Response:

    keyword = request.keyword

    if not db.keyword_exists(keyword):
        raise HTTPException(
            status_code=404,
            detail='Não foi possível encontrar ' +
            f'um link com a keyword {keyword}'
        )

    link = db.get_link_by_keyword(keyword)
    try:
        db.delete_link(link)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Erro ao deletar link: ' + str(e)
        )

    return Response(
        status_code=200,
        content=f'Link com a keyword {link.keyword} deletado com sucesso.'
    )


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
