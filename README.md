# API de Gerenciamento de Usuários e Refeições

Esta é uma aplicação FastAPI para gerenciar usuários e suas refeições.

## Funcionalidades

- **Listar Usuários**: Recupera todos os usuários.
- **Registrar Usuário**: Adiciona um novo usuário.
- **Adicionar Refeição**: Adiciona uma refeição para um usuário.
- **Listar Refeições por Usuário**: Mostra todas as refeições de um usuário.
- **Atualizar Refeição**: Atualiza os dados de uma refeição.
- **Deletar Refeição**: Remove uma refeição.

## Endpoints

## 📖 Endpoints da API

### Listar Usuários

**GET** `/users`

---

### Registrar Usuário

**POST** `/users`

**Parâmetros:**
- `name`: Nome do usuário
- `age`: Idade do usuário
- `gender`: Gênero do usuário

---

### Adicionar Refeição

**POST** `/meals`

**Parâmetros:**
- `user_id`: ID do usuário
- `meal_type`: Tipo de refeição (ex: café da manhã, almoço, jantar)
- `food_items`: Lista de itens alimentares
- `calories`: Quantidade de calorias
- `date`: Data da refeição

---

### Listar Refeições por Usuário

**GET** `/meals/{user_id}`

---

### Atualizar Refeição

**PUT** `/meals/{meal_id}`

---

### Deletar Refeição

**DELETE** `/meals/{meal_id}`

---

## 🔧 Como Executar a Aplicação

### 1. Instale as dependências:

pip install fastapi uvicorn

### 2. Execute a aplicação:

uvicorn main:app --reload

### 3. Acesse a documentação da API em:

http://127.0.0.1:8000/docs
