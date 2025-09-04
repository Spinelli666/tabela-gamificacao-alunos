# 🎮 Sistema de Gamificação Escolar

Um sistema completo de gamificação educacional com ranking de alunos, gestão de atividades, sistema de grupos, caça-níquel e premiações.

## �️ Como Executar Localmente

### Pré-requisitos
- Python 3.8+
- Git

### Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/Spinelli666/tabela-gamificacao-alunos.git
cd tabela-gamificacao-alunos
```

2. **Crie e ative o ambiente virtual:**
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações:**
```bash
python manage.py migrate
```

5. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

6. **Execute o servidor:**
```bash
python manage.py runserver
```

7. **Acesse o sistema:**
- **URL:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin
