# nanicolink
Pílulas de nanicolina (Chapolin) para o seu link longo!

# Requisições
Todas as requisições devem ser feitas para o endereço `https://nanicolink.herokuapp.com/`.

## Criar um link
- url: `https://nanicolink.herokuapp.com/create`
- método: `PUT`

Ao criar um link, você pode personalizar os seguintes itens:
- keyword: a palavra-chave que será usada para acessar o link (ex: https://nanicolink.herokuapp.com/keyword)
- url: o link que será encurtado
- tags: tags para o link
- destroy_clicks: a quantidade de cliques que o link pode receber antes de ser destruído (0 para infinito)
- destroy_time: o tempo em horas que o link pode ficar ativo antes de ser destruído (0 para infinito)
```json
{
    "long_url": "https://google.com",
    "keyword": "google",
    "tags": [
        "search",
        "google"
    ],
    "destroy_clicks": 0,
    "destroy_time": 0
}
```

Você também pode optar por usar as configurações padrão, para isso basta passar somente o link no request
```json
{
    "long_url": "https://google.com"
}
```

## Deletar um link
- url: `https://nanicolink.herokuapp.com/delete`
- método: `DELETE`

Para deletar um link, você precisa passar a keyword dele
```json
{
    "keyword": "google"
}
```

## Acessar um link
- url: `https://nanicolink.herokuapp.com/[keyword]`
- método: `GET`
Ao acessar um link, você é redirecionado.

## Listar links por tag
- url: `https://nanicolink.herokuapp.com/tag/[tag]`
- método: `GET`

# Acessar detalhes de um link
- url: `https://nanicolink.herokuapp.com/details/?keyword=[keyword]`
- método: `GET`