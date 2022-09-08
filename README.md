# nanicolink
Pílulas de nanicolina (Chapolin) para o seu link longo!

tasks
https://eduardo-barreto.notion.site/8cc5b41333464993864d1144c0d503a8?v=fbeeaf16fde243a2a26b73762c3474f2

# Requisições

## Criar um link
- url: `host/create`
- método: `POST`

Ao criar um link, você pode personalizar os seguintes itens:
- keyword: a palavra-chave que será usada para acessar o link (ex: host/keyword)
- url: o link que será encurtado
- tags: tags para o link
- destroy_clicks: a quantidade de cliques que o link pode receber antes de ser destruído (0 para infinito)
- destroy_time: o tempo em horas que o link pode ficar ativo antes de ser destruído (0 para infinito)
```json
{
    "long_url": "https://google.com",
    "keyword": "google",
    "tags": ["search", "google"],
    "destroy_clicks": 0,
    "destroy_time": 0
}
```

Você também pode optar por usar as configurações padrão, para isso basta passar somente o link no request
```json
{
    "long_url": "https://google.com",
}
```

## Deletar um link
- url: `host/delete`
- método: `POST`

Para deletar um link, você precisa passar a keyword dele
```json
{
    "keyword": "google"
}
```

## Acessar um link
- url: `host/[keyword]`
- método: `GET`
Ao acessar um link, você é redirecionado.

## Listar links por tag
- url: `host/tag/[tag]`
- método: `GET`

# Acessar detalhes de um link
- url: `host/[keyword]/details`
- método: `GET`