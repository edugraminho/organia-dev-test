# 📊 API de Análise de Sentimentos

Esta API permite a **classificação automática de sentimentos** em avaliações de clientes sobre produtos, serviços ou suporte. A análise é feita com um modelo de IA que classifica os sentimentos como **positivo, negativo ou neutro** e gera uma análise das avaliações.



## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI** - Framework para criação da API REST
- **PostgreSQL** - Banco de dados relacional
- **SQLAlchemy** - ORM para manipulação do banco de dados
- **Docker & Docker Compose** - Para execução do ambiente isolado
- **Maritaca AI (sabia-3)** - Modelo LLM para análise de sentimentos
- **Pydantic** - Validação de dados
- **Pytest** - Testes Unitários

### 📌 A API utiliza o modelo de linguagem Maritaca AI (sabia-3) para análise de sentimentos.
**Essa escolha foi feita porque:**

✔️ É um modelo nativo em português, garantindo melhor entendimento de expressões e contexto.

✔️ Evita problemas de tradução, comuns em modelos treinados em inglês.


O prompt utilizado na API foi baseado no artigo:
[**🔗 Análise de Sentimentos com LLM**](https://www.aprendizartificial.com/analise-de-sentimentos-com-llm/)

---

## 📌 Instalação e Configuração

### **1️⃣ Clonar o repositório**

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### **2️⃣ Configurar as variáveis de ambiente**

Copie o arquivo `.env.example` com o nome `.env` na raiz do projeto.

```bash
cp .env.example .env
```

```ini
MARITACA_API_KEY=sua-chave-aqui (me chama que forneço a key para testes)
```

### **3️⃣ Criar e ativar um ambiente virtual (opcional)**

```bash
python3 -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate      # Windows
```

### **4️⃣ Instalar as dependências**

```bash
pip install -r requirements.txt
```

---

## 💻 Executando o projeto com Docker

```bash
docker-compose up --build db app
```

Isso inicializará a API e o banco de dados PostgreSQL dentro de containers.

A API estará disponível em http://localhost:8000.

---

# 📌 Acessando a documentação da API

A API possui documentação interativa pelo Swagger UI e ReDoc:

### 📌 Swagger UI: http://localhost:8000/docs

### 📌 ReDoc UI: http://localhost:8000/redoc

---

# 📌 Endpoints da API

Método Rota Descrição
POST /reviews/ Cria uma nova avaliação e realiza a análise de sentimento
GET /reviews/ Retorna todas as avaliações cadastradas
GET /reviews/{id} Busca uma avaliação específica pelo ID
GET /reviews/report Retorna um relatório de avaliações no período informado

| Método | Rota            | Descrição                                                 |
| :----- | :-------------- | :-------------------------------------------------------- |
| POST   | /reviews/       | Cria uma nova avaliação e realiza a análise de sentimento |
| GET    | /reviews/       | Retorna todas as avaliações cadastradas                   |
| GET    | /reviews/{id}   | Busca uma avaliação específica pelo ID                    |
| GET    | /reviews/report | Retorna um relatório de avaliações no período informado   |

## 📌 Exemplo de requisição
> OBS: Anexo com os Reviews está no arquivo reviews.json na raiz do projeto

---

1️⃣ **Criando uma nova avaliação** (`POST /reviews/`)

```json
{
  "customer_name": "Eduardo",
  "review_text": "O suporte foi incrível, muito rápido!",
  "sentiment": "positiva",
  "review_date": "2024-06-10"
}
```

**📌 Resposta JSON:**

```json
{
  "status": "OK",
  "review": {
    "id": 1,
    "customer_name": "Eduardo",
    "review_text": "O suporte foi incrível, muito rápido!",
    "sentiment": "positiva",
    "review_date": "2024-06-10"
  }
}
```

---

---

2️⃣ **Obter todos as avaliações** (`GET /reviews/`)

**📌 Resposta JSON:**

```json
{
	"reviews_list": [
		{
			"id": 1,
			"customer_name": "Ana Silva",
			"review_text": "O suporte foi incrível, muito rápido!",
			"sentiment": "neutra",
			"review_date": "2024/08/07"
		},
		{
			"id": 2,
			"customer_name": "Eduardo ",
			"review_text":"O suporte foi incrível, muito rápido!",
			"sentiment": "neutra",
			"review_date": "2024/08/07"
		},
	]
}
```

---
---

3️⃣ **Obter todos as avaliações por ID** (`GET /reviews/{id}`)


**📌 Resposta JSON:**

```json
{
  "review": {
    "id": 1,
    "customer_name": "Eduardo",
    "review_text": "O suporte foi incrível, muito rápido!",
    "sentiment": "positiva",
    "review_date": "2024-06-10"
  }
}
```

---
---

4️⃣ **Gerando um relatório** (`GET /reviews/report`)

📌 Requisição:

`GET /reviews/report?start_date=2024-06-01&end_date=2024-06-30`


**📌 Resposta JSON:**

```json
{
  "total_reviews": 10,
  "positive": 7,
  "negative": 2,
  "neutral": 1,
  "reviews": [
    {
      "id": 1,
      "customer_name": "Eduardo",
      "review_text": "O suporte foi incrível, muito rápido!",
      "sentiment": "positiva",
      "score": 0.9,
      "keywords": ["suporte", "rápido", "incrível"],
      "explanation": "A análise identificou um sentimento positivo."
    },
    ...
  ]
}
```

---
---

# 📌 Testes Automatizados

O projeto inclui testes unitários usando pytest. Para rodar os testes:
```bash
docker-compose up test
```

# 📌 Executando os Linters (PEP8)
Para validar automaticamente a conformidade com o **PEP8** execute o seguinte comando:
```bash
docker-compose up lint
```

Isso executará:

- Flake8 → Verifica erros de estilo PEP8.
- Black → Verifica se o código está formatado corretamente.
- Isort → Verifica se os imports estão ordenados corretamente.