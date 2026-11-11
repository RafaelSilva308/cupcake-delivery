# Cupcake Delivery — PIT II (Engenharia de Software)

Aplicação web de delivery de cupcakes, desenvolvida como parte do Projeto Integrador Transdisciplinar em Engenharia de Software II (Cruzeiro do Sul Virtual). Continuação do PIT I, que definiu a IHC/UX do produto (mapas conceitual/navegacional, wireframes e mockups).

## Stack

- **Linguagem/Framework:** Python 3 + Flask
- **Padrão arquitetural:** MVC (Model: SQLAlchemy / View: Jinja2 / Controller: Blueprints do Flask)
- **Banco de dados:** SQLite (desenvolvimento) / PostgreSQL (produção no Render)
- **Testes:** pytest
- **Deploy:** Render (web service + banco Postgres gratuito, via `render.yaml`)

## Funcionalidades

- Catálogo de cupcakes disponíveis
- Carrinho de compras (sessão, sem necessidade de login)
- Checkout com dados de entrega (nome, telefone, endereço, forma de pagamento)
- Confirmação de pedido com resumo e status

## Estrutura do projeto

```
cupcake-delivery/
  app/
    models.py            # Model: Cupcake, Pedido, ItemPedido
    controllers/          # Controller: rotas (catalog, cart, orders)
    templates/             # View: páginas Jinja2
    static/                 # CSS e imagens
    seed.py                 # popula o banco com cupcakes de exemplo
  tests/                    # testes automatizados (pytest)
  docs/
    diagrama_classes.md      # diagrama de classes UML (Mermaid)
    dicionario_dados.md       # dicionário de dados das tabelas
  config.py
  run.py
```

## Como rodar localmente

```bash
# 1. Crie e ative um ambiente virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Popule o banco com cupcakes de exemplo
python -m app.seed

# 4. Rode a aplicação
python run.py
```

A aplicação sobe em `http://127.0.0.1:5000/`.

## Como rodar os testes

```bash
pip install -r requirements.txt
pytest -v
```

Os testes usam um banco SQLite em memória isolado (`TestConfig`), sem afetar o banco de desenvolvimento.

## Fluxo da aplicação

1. **Cardápio (`/`)** — lista os cupcakes disponíveis, cada um com botão de adicionar ao carrinho.
2. **Carrinho (`/carrinho/`)** — exibe itens adicionados, permite atualizar quantidade ou remover, mostra o total.
3. **Checkout (`/checkout`)** — formulário com dados de entrega; ao confirmar, cria o pedido no banco e esvazia o carrinho.
4. **Confirmação (`/pedido/<id>`)** — resumo do pedido realizado.

## Deploy no Render

O arquivo `render.yaml` na raiz do projeto já descreve toda a infraestrutura (web service + banco Postgres gratuito), no formato "Blueprint" do Render:

1. Crie uma conta em [render.com](https://render.com) (pode entrar direto com sua conta do GitHub).
2. No painel, clique em **New +** → **Blueprint**.
3. Conecte o repositório `cupcake-delivery` do GitHub.
4. O Render vai ler o `render.yaml` automaticamente e propor criar:
   - um **Web Service** (`cupcake-delivery`, plano free)
   - um **banco PostgreSQL** (`cupcake-delivery-db`, plano free)
5. Clique em **Apply** e aguarde o build/deploy (alguns minutos).
6. Ao final, o Render mostra a URL pública, algo como `https://cupcake-delivery.onrender.com` — esse é o "link da solução em funcionamento".

Detalhes já resolvidos no código:
- `config.py` lê `DATABASE_URL` do ambiente e normaliza o esquema `postgres://` → `postgresql://` (exigido pelo SQLAlchemy 2.x). Sem essa variável (ambiente local), cai no SQLite normalmente.
- O `buildCommand` roda `python -m app.seed`, que cria as tabelas e popula os cupcakes de exemplo automaticamente (só insere se o banco estiver vazio — seguro rodar a cada deploy).
- `startCommand` usa `gunicorn` (servidor de produção), já incluído no `requirements.txt`.

**Observação:** no plano gratuito, o serviço "dorme" após ~15 minutos sem acesso e demora alguns segundos para acordar na próxima visita — isso é normal, mas, diferente do SQLite puro, os pedidos continuam salvos no Postgres entre essas pausas.
