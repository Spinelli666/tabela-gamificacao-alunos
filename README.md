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

8. **Acesse o sistema:**
- **URL:** http://127.0.0.1:8000
- **Admin:** http://127.0.0.1:8000/admin

## 📁 Estrutura do Projeto

```
gamificacao_escolar/
├── gamificacao/          # App principal
│   ├── models.py        # Modelos de dados
│   ├── views.py         # Lógica das views
│   ├── forms.py         # Formulários
│   └── urls.py          # Rotas
├── static/              # Arquivos estáticos (CSS, JS, imagens)
├── templates/           # Templates HTML
├── db.sqlite3          # Banco de dados SQLite
├── manage.py           # Gerenciador Django
└── requirements.txt    # Dependências Python
```

## ⚙️ Tecnologias Utilizadas

- **Backend:** Django 5.2.6
- **Frontend:** Bootstrap 5 + CSS Cyberpunk personalizado
- **Banco de Dados:** SQLite
- **Autenticação:** Django Auth System

## 🎯 Funcionalidades Principais

### 👥 **Gestão de Usuários**
- ✅ Sistema de Login/Logout
- ✅ Autenticação de usuários
- ✅ Dashboard personalizado

### 📚 **Gestão Acadêmica**
- ✅ Cadastro e gestão de alunos
- ✅ Criação e edição de atividades
- ✅ Sistema de notas com histórico
- ✅ Controle de presença

### 🏆 **Sistema de Gamificação**
- ✅ Rankings dinâmicos
- ✅ Sistema de grupos com líderes (ícones de coroa)
- ✅ Gestão de membros de grupos
- ✅ Caça-níquel com premiações
- ✅ Sistema de prêmios pendentes

### 🎨 **Interface**
- ✅ Design cyberpunk responsivo
- ✅ Tema escuro com neon
- ✅ Dropdowns funcionais
- ✅ Modais de confirmação
- ✅ Animações suaves

## 🔧 Comandos Úteis

```bash
# Criar migrações após mudanças nos modelos
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar testes
python manage.py test

# Coletar arquivos estáticos
python manage.py collectstatic
```

## 📊 Estrutura do Banco de Dados

### Principais Modelos:
- **Aluno:** Dados dos estudantes
- **Atividade:** Tarefas e trabalhos
- **Nota:** Avaliações com histórico
- **Presenca:** Controle de frequência
- **Grupo:** Grupos de trabalho
- **MembroGrupo:** Relacionamento aluno-grupo
- **CacaNiquel:** Sistema de jogos e premiações

## 🎮 Como Usar o Sistema

1. **Faça login** na página inicial
2. **Dashboard:** Veja o ranking geral dos alunos
3. **Alunos:** Cadastre e gerencie estudantes
4. **Atividades:** Crie tarefas e trabalhos
5. **Notas:** Avalie os alunos
6. **Presença:** Controle a frequência
7. **Grupos:** Organize equipes de trabalho
8. **Caça-níquel:** Sistema de premiações gamificado

## 🎯 Próximas Funcionalidades

- [ ] Relatórios em PDF
- [ ] Sistema de badges/conquistas
- [ ] Notificações em tempo real
- [ ] API REST
- [ ] App mobile

## 📞 Suporte

Sistema desenvolvido com ❤️ para educação gamificada!

**Versão:** 1.0  
**Última atualização:** Setembro 2025