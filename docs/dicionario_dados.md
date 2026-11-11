# Dicionário de Dados — App de Delivery de Cupcakes

SGBD utilizado: **SQLite** (desenvolvimento/entrega acadêmica) — SGBD popular e de fácil manutenção, compatível com migração futura para PostgreSQL/MySQL via o mesmo ORM (SQLAlchemy).

## Tabela `cupcake`

| Campo       | Tipo          | Nulo? | Chave | Descrição                                   |
|-------------|---------------|-------|-------|----------------------------------------------|
| id          | INTEGER       | Não   | PK    | Identificador único do cupcake                |
| nome        | VARCHAR(80)   | Não   |       | Nome do produto exibido no cardápio           |
| descricao   | VARCHAR(255)  | Não   |       | Descrição curta do sabor/ingredientes         |
| preco       | DECIMAL(10,2) | Não   |       | Preço unitário de venda                       |
| imagem_url  | VARCHAR(255)  | Não   |       | Caminho/URL da imagem do produto              |
| disponivel  | BOOLEAN       | Não   |       | Se o produto aparece no cardápio (true/false) |

## Tabela `pedido`

| Campo            | Tipo          | Nulo? | Chave | Descrição                                                        |
|------------------|---------------|-------|-------|-------------------------------------------------------------------|
| id               | INTEGER       | Não   | PK    | Identificador único do pedido                                     |
| nome_cliente     | VARCHAR(120)  | Não   |       | Nome informado pelo cliente no checkout                           |
| telefone         | VARCHAR(20)   | Não   |       | Telefone de contato para a entrega                                 |
| endereco         | VARCHAR(255)  | Não   |       | Endereço completo de entrega                                       |
| forma_pagamento  | VARCHAR(30)   | Não   |       | `dinheiro`, `cartao` ou `pix`                                       |
| status           | VARCHAR(30)   | Não   |       | Estado atual do pedido (padrão: `recebido`)                        |
| data_criacao     | DATETIME      | Não   |       | Data/hora em que o pedido foi realizado                            |
| total            | DECIMAL(10,2) | Não   |       | Soma dos subtotais de todos os itens do pedido                     |

## Tabela `item_pedido`

| Campo          | Tipo          | Nulo? | Chave | Descrição                                                   |
|----------------|---------------|-------|-------|---------------------------------------------------------------|
| id             | INTEGER       | Não   | PK    | Identificador único do item                                   |
| pedido_id      | INTEGER       | Não   | FK → pedido.id   | Pedido ao qual este item pertence                  |
| cupcake_id     | INTEGER       | Não   | FK → cupcake.id  | Cupcake comprado                                    |
| quantidade     | INTEGER       | Não   |       | Quantidade do cupcake neste pedido                              |
| preco_unitario | DECIMAL(10,2) | Não   |       | Preço do cupcake no momento da compra (snapshot, não é FK de preço) |

## Integridade referencial

- `item_pedido.pedido_id` → `pedido.id`: exclusão em cascata (`ON DELETE CASCADE` via `cascade="all, delete-orphan"` no ORM) — ao remover um pedido, seus itens são removidos junto.
- `item_pedido.cupcake_id` → `cupcake.id`: sem cascata — um cupcake não pode ser excluído fisicamente se já existir em itens de pedido antigos (preservação de histórico). Na prática, a remoção de um produto do cardápio deve ser feita via `disponivel = false`, não exclusão.
