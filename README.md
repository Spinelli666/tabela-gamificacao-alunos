# 🎮 Sistema de Gamificação Escolar

Um sistema completo de gamificação educacional com ranking de alunos, gestão de atividades, sistema de grupos, caça-níquel e premiações.

## 🚀 Deploy no Render.com (GRATUITO)

### Passo 1: Preparar o Repositório

1. **Push para o GitHub:**
```bash
git add .
git commit -m "Preparando para deploy no Render"
git push origin main
```

### Passo 2: Configurar no Render.com

1. **Acesse:** https://render.com
2. **Crie uma conta** (pode usar GitHub)
3. **Clique em "New +"** → **"Web Service"**
4. **Conecte seu repositório GitHub**
5. **Configure:**
   - **Name:** `gamificacao-escolar`
   - **Environment:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn gamificacao_escolar.wsgi:application`
   - **Plan:** `Free` (gratuito)

### Passo 3: Variáveis de Ambiente

No Render, adicione essas variáveis:

```
DEBUG = False
PYTHON_VERSION = 3.12.3
SECRET_KEY = [será gerado automaticamente]
```

### Passo 4: Banco de Dados

1. **Crie um PostgreSQL Database** (também gratuito)
2. **Nome:** `gamificacao-db`
3. **O Render conectará automaticamente**

### Passo 5: Deploy

1. **Clique em "Create Web Service"**
2. **Aguarde o build** (pode demorar alguns minutos)
3. **Seu site estará disponível em:** `https://gamificacao-escolar.onrender.com`

## 🛠️ Desenvolvimento Local

```bash
# Clonar repositório
git clone [seu-repositorio]
cd tabela-gamificacao-alunos

# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

## ⚙️ Tecnologias

- **Backend:** Django 5.2.6
- **Frontend:** Bootstrap 5 + CSS Cyberpunk
- **Banco de Dados:** SQLite (dev) / PostgreSQL (prod)
- **Deploy:** Render.com

## 🎯 Funcionalidades

- ✅ Sistema de Login/Autenticação
- ✅ Dashboard com Rankings
- ✅ Gestão de Alunos
- ✅ Gestão de Atividades
- ✅ Sistema de Notas
- ✅ Controle de Presença
- ✅ Gestão de Grupos com Líderes
- ✅ Caça-Níquel com Premiações
- ✅ Sistema de Prêmios Pendentes
- ✅ Interface Cyberpunk Responsiva

## 📞 Suporte

Desenvolvido com ❤️ para educação gamificada!