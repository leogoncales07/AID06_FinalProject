# 🦸 Comic Store - Sistema de Gestão Web para PME

Sistema de gestão web para uma loja de banda desenhada (comics), desenvolvido com **Python** e **Django**, no âmbito do projeto final da disciplina AID06.

## 📋 Funcionalidades

- **Gestão de Produtos**: CRUD completo para comics, séries e editoras
- **Filtragem e Pesquisa**: Pesquisa de produtos por nome, série ou editora
- **Vista de Detalhe**: Visualização completa de informação de cada produto
- **Autenticação**: Sistema de login/logout com proteção de rotas
- **Painel de Administração**: Gestão de dados via Django Admin
- **Interface Responsiva**: Estilizada com Bootstrap via CDN

## 🚀 Como Instalar e Executar

### 1. Clonar o Repositório

```bash
git clone https://github.com/leogoncales07/AID06_FinalProject.git
cd AID06_FinalProject
```

### 2. Criar e Ativar o Ambiente Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Aplicar as Migrações da Base de Dados

```bash
python manage.py migrate
```

### 5. Criar um Superutilizador (opcional)

```bash
python manage.py createsuperuser
```

### 6. Iniciar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

A aplicação estará disponível em: [http://127.0.0.1:8000](http://127.0.0.1:8000)

O painel de administração estará em: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## 🛠️ Tecnologias Utilizadas

- **Python 3.13**
- **Django 6.0**
- **SQLite3** (base de dados local)
- **Bootstrap 5** (via CDN)
- **HTML5 / CSS3**

## 📁 Estrutura do Projeto

```
AID06_FinalProject/
├── comic_store/          # Configurações do projeto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                # Aplicação principal
│   ├── models.py         # Modelos de dados
│   ├── views.py          # Lógica de vistas
│   ├── forms.py          # Formulários Django
│   ├── urls.py           # Rotas da aplicação
│   ├── admin.py          # Configuração do painel admin
│   └── templates/        # Templates HTML
├── templates/            # Templates base (base.html)
├── static/               # Ficheiros estáticos (CSS, JS, imagens)
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 👥 Equipa

- Projeto desenvolvido no âmbito da disciplina AID06

## 📄 Licença

Projeto académico — Todos os direitos reservados.
