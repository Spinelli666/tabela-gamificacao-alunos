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

4. **Configure as variáveis de ambiente (opcional):**
```bash
cp .env.example .env
# Edite o arquivo .env se necessário
```

5. **Execute as migrações:**
```bash
python manage.py migrate
```

6. **Crie um superusuário:**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor:**
```bash
python manage.py runserver
```
