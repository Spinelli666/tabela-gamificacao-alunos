from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Avg, Count
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Aluno, Atividade, Nota, HistoricoNota, Presenca, Grupo, MembroGrupo, CacaNiquel
from .forms import AlunoForm, AtividadeForm, NotaForm, PresencaForm, GrupoForm, AdicionarMembrosForm
import json
import random
from decimal import Decimal


def login_view(request):
    """View para login do usuário"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    
    return render(request, 'gamificacao/login.html')


def logout_view(request):
    """View para logout do usuário"""
    logout(request)
    messages.info(request, 'Você foi desconectado com sucesso.')
    return redirect('login')


@login_required
def dashboard(request):
    """View principal - Dashboard com ranking"""
    # Buscar todos os alunos ativos
    alunos = Aluno.objects.filter(ativo=True).order_by('nome')
    
    # Calcular ranking baseado na média das notas
    ranking_data = []
    for aluno in alunos:
        ranking_data.append({
            'aluno': aluno,
            'nota_media': aluno.nota_atual,
            'total_atividades': aluno.total_atividades,
            'pontos_presenca': aluno.pontos_presenca,
            'pontuacao_total': aluno.pontuacao_total,
            'percentual_presenca': aluno.percentual_presenca
        })
    
    # Ordenar por pontuação total (nota + presença) decrescente
    ranking_data.sort(key=lambda x: (x['pontuacao_total'], x['nota_media'], x['pontos_presenca']), reverse=True)
    
    # Adicionar posição no ranking
    for i, item in enumerate(ranking_data, 1):
        item['posicao'] = i
    
    # Estatísticas gerais
    total_alunos = len(ranking_data)
    total_atividades = Atividade.objects.filter(ativa=True).count()
    total_presencas = Presenca.objects.filter(presente=True).count()
    media_geral = sum(float(item['pontuacao_total']) for item in ranking_data) / total_alunos if total_alunos > 0 else 0
    media_presenca = sum(item['pontos_presenca'] for item in ranking_data) / total_alunos if total_alunos > 0 else 0
    
    context = {
        'ranking': ranking_data,
        'total_alunos': total_alunos,
        'total_atividades': total_atividades,
        'total_presencas': total_presencas,
        'media_geral': round(media_geral, 2),
        'media_presenca': round(media_presenca, 1),
    }
    
    return render(request, 'gamificacao/dashboard.html', context)


@login_required
def historico_notas(request):
    """View para mostrar histórico de notas por atividade"""
    atividades = Atividade.objects.filter(ativa=True).order_by('-data_criacao')
    
    historico_data = []
    for atividade in atividades:
        notas = Nota.objects.filter(atividade=atividade).select_related('aluno').order_by('-valor', 'aluno__nome')
        historico_data.append({
            'atividade': atividade,
            'notas': notas,
            'media': atividade.media_turma,
            'total_alunos': notas.count()
        })
    
    return render(request, 'gamificacao/historico.html', {'historico_data': historico_data})


@login_required
def gerenciar_alunos(request):
    """View para gerenciar alunos"""
    alunos = Aluno.objects.all().order_by('nome')
    
    # Paginação
    paginator = Paginator(alunos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'alunos': page_obj,
    }
    return render(request, 'gamificacao/gerenciar_alunos.html', context)


@login_required
def criar_aluno(request):
    """View para criar novo aluno"""
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno criado com sucesso!')
            return redirect('gerenciar_alunos')
    else:
        form = AlunoForm()
    
    return render(request, 'gamificacao/form_aluno.html', {'form': form, 'titulo': 'Criar Aluno'})


@login_required
def editar_aluno(request, pk):
    """View para editar aluno"""
    aluno = get_object_or_404(Aluno, pk=pk)
    
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso!')
            return redirect('gerenciar_alunos')
    else:
        form = AlunoForm(instance=aluno)
    
    return render(request, 'gamificacao/form_aluno.html', {'form': form, 'titulo': 'Editar Aluno', 'aluno': aluno})


@login_required
def deletar_aluno(request, pk):
    """View para deletar aluno"""
    aluno = get_object_or_404(Aluno, pk=pk)
    
    if request.method == 'POST':
        aluno.delete()
        messages.success(request, 'Aluno excluído com sucesso!')
        return redirect('gerenciar_alunos')
    
    return render(request, 'gamificacao/confirmar_delete.html', {'objeto': aluno, 'tipo': 'aluno'})


@login_required
def gerenciar_atividades(request):
    """View para gerenciar atividades"""
    atividades = Atividade.objects.all().order_by('-data_criacao')
    
    # Paginação
    paginator = Paginator(atividades, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gamificacao/gerenciar_atividades.html', {'page_obj': page_obj})


@login_required
def criar_atividade(request):
    """View para criar nova atividade"""
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade criada com sucesso!')
            return redirect('gerenciar_atividades')
    else:
        form = AtividadeForm()
    
    return render(request, 'gamificacao/form_atividade.html', {'form': form, 'titulo': 'Criar Atividade'})


@login_required
def editar_atividade(request, pk):
    """View para editar atividade"""
    atividade = get_object_or_404(Atividade, pk=pk)
    
    if request.method == 'POST':
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Atividade atualizada com sucesso!')
            return redirect('gerenciar_atividades')
    else:
        form = AtividadeForm(instance=atividade)
    
    return render(request, 'gamificacao/form_atividade.html', {'form': form, 'titulo': 'Editar Atividade', 'atividade': atividade})


@login_required
def deletar_atividade(request, pk):
    """View para deletar atividade"""
    atividade = get_object_or_404(Atividade, pk=pk)
    
    if request.method == 'POST':
        nome = atividade.nome
        print(f"Tentando excluir atividade: {nome} (ID: {pk})")
        
        try:
            # Verificar se há notas associadas
            notas_count = atividade.nota_set.count()
            print(f"Atividade tem {notas_count} notas associadas")
            
            atividade.delete()
            print(f"Atividade '{nome}' excluída com sucesso")
            messages.success(request, f'Atividade "{nome}" excluída com sucesso!')
            return redirect('gerenciar_atividades')
            
        except Exception as e:
            print(f"Erro ao excluir atividade: {str(e)}")
            messages.error(request, f'Erro ao excluir atividade: {str(e)}')
            return redirect('gerenciar_atividades')
    
    return render(request, 'gamificacao/confirmar_delete.html', {
        'objeto': atividade, 
        'tipo': 'atividade',
        'titulo': f'Excluir atividade "{atividade.nome}"',
        'mensagem': f'Tem certeza que deseja excluir a atividade "{atividade.nome}"? Todas as notas desta atividade também serão excluídas!'
    })


@login_required
def gerenciar_notas(request, atividade_id=None):
    """View para gerenciar notas de uma atividade específica"""
    if atividade_id:
        atividade = get_object_or_404(Atividade, pk=atividade_id)
        notas = Nota.objects.filter(atividade=atividade).select_related('aluno').order_by('aluno__nome')
        
        # Buscar alunos que ainda não têm nota nesta atividade
        alunos_com_nota = notas.values_list('aluno_id', flat=True)
        alunos_sem_nota = Aluno.objects.filter(ativo=True).exclude(id__in=alunos_com_nota)
        
        context = {
            'atividade': atividade,
            'notas': notas,
            'alunos_sem_nota': alunos_sem_nota,
        }
        return render(request, 'gamificacao/gerenciar_notas.html', context)
    else:
        atividades = Atividade.objects.filter(ativa=True).order_by('-data_criacao')
        return render(request, 'gamificacao/selecionar_atividade.html', {'atividades': atividades})


@login_required
def lancar_nota(request, atividade_id, aluno_id=None):
    """View para lançar nova nota"""
    atividade = get_object_or_404(Atividade, pk=atividade_id)
    
    if aluno_id:
        aluno = get_object_or_404(Aluno, pk=aluno_id)
        # Verificar se já existe nota para este aluno nesta atividade
        if Nota.objects.filter(atividade=atividade, aluno=aluno).exists():
            messages.warning(request, f'Já existe uma nota para {aluno.nome} nesta atividade. Use a função editar.')
            return redirect('gerenciar_notas_atividade', atividade_id=atividade.id)
    else:
        aluno = None
    
    if request.method == 'POST':
        form = NotaForm(request.POST, atividade=atividade)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.atividade = atividade
            nota.lancada_por = request.user
            nota.save()
            
            messages.success(request, f'Nota lançada com sucesso para {nota.aluno.nome}!')
            return redirect('gerenciar_notas_atividade', atividade_id=atividade.id)
    else:
        initial_data = {}
        if aluno:
            initial_data['aluno'] = aluno
            
        form = NotaForm(atividade=atividade, initial=initial_data)
    
    # Buscar histórico se existir
    historico = None
    
    context = {
        'form': form,
        'atividade': atividade,
        'aluno': aluno,
        'historico': historico,
        'is_edit': False
    }
    
    return render(request, 'gamificacao/form_nota.html', context)


@login_required
def lancar_nota_aluno(request, atividade_id, aluno_id):
    """View para lançar nova nota para aluno específico"""
    return lancar_nota(request, atividade_id, aluno_id)


@login_required
def editar_nota(request, atividade_id, aluno_id):
    """View para editar nota existente"""
    atividade = get_object_or_404(Atividade, pk=atividade_id)
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    nota = get_object_or_404(Nota, atividade=atividade, aluno=aluno)
    
    if request.method == 'POST':
        valor_anterior = nota.valor
        form = NotaForm(request.POST, instance=nota, atividade=atividade)
        if form.is_valid():
            nova_nota = form.save(commit=False)
            
            # Se o valor mudou, salvar histórico
            if nova_nota.valor != valor_anterior:
                HistoricoNota.objects.create(
                    nota=nota,
                    valor_anterior=valor_anterior,
                    valor_novo=nova_nota.valor,
                    motivo=request.POST.get('motivo_alteracao', 'Alteração via sistema'),
                    usuario=request.user
                )
            
            nova_nota.save()
            messages.success(request, f'Nota de {aluno.nome} atualizada com sucesso!')
            return redirect('gerenciar_notas_atividade', atividade_id=atividade.id)
    else:
        form = NotaForm(instance=nota, atividade=atividade)
    
    # Buscar histórico
    historico = HistoricoNota.objects.filter(nota=nota).order_by('-data_alteracao')
    
    context = {
        'form': form,
        'atividade': atividade,
        'aluno': aluno,
        'historico': historico,
    }
    
    return render(request, 'gamificacao/form_nota.html', context)


@login_required
def deletar_nota(request, nota_id):
    """View para deletar nota"""
    nota = get_object_or_404(Nota, pk=nota_id)
    atividade_id = nota.atividade.id
    
    if request.method == 'POST':
        # TODO: Salvar no histórico antes de deletar (temporariamente comentado)
        # HistoricoNota.objects.create(
        #     nota=nota,
        #     valor_anterior=nota.valor,
        #     valor_novo=None,
        #     motivo='Nota excluída',
        #     usuario=request.user
        # )
        
        aluno_nome = nota.aluno.nome
        nota.delete()
        messages.success(request, f'Nota de {aluno_nome} excluída com sucesso!')
        return redirect('gerenciar_notas_atividade', atividade_id=atividade_id)
    
    return render(request, 'gamificacao/confirmar_delete.html', {
        'objeto': nota, 
        'tipo': 'nota',
        'titulo': f'Excluir nota de {nota.aluno.nome}',
        'mensagem': f'Tem certeza que deseja excluir a nota {nota.valor} de {nota.aluno.nome} na atividade "{nota.atividade.nome}"?'
    })


@login_required
def gerenciar_notas_atividade(request, atividade_id):
    """View para gerenciar notas de uma atividade específica"""
    atividade = get_object_or_404(Atividade, pk=atividade_id)
    notas = Nota.objects.filter(atividade=atividade).select_related('aluno').order_by('-valor', 'aluno__nome')
    
    # Buscar alunos que ainda não têm nota nesta atividade
    alunos_com_nota = notas.values_list('aluno_id', flat=True)
    alunos_sem_nota = Aluno.objects.filter(ativo=True).exclude(id__in=alunos_com_nota).order_by('nome')
    
    context = {
        'atividade': atividade,
        'notas': notas,
        'alunos_sem_nota': alunos_sem_nota,
    }
    return render(request, 'gamificacao/gerenciar_notas.html', context)


# ===== VIEWS DE PRESENÇA =====

@login_required
def gerenciar_presencas(request):
    """View para gerenciar presenças"""
    from datetime import date, timedelta
    
    # Filtros de data
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Se não informadas, usar últimos 30 dias
    if not data_inicio:
        data_inicio = (date.today() - timedelta(days=30)).strftime('%Y-%m-%d')
    if not data_fim:
        data_fim = date.today().strftime('%Y-%m-%d')
    
    # Converter strings para objetos date
    try:
        data_inicio_obj = date.fromisoformat(data_inicio)
        data_fim_obj = date.fromisoformat(data_fim)
    except ValueError:
        data_inicio_obj = date.today() - timedelta(days=30)
        data_fim_obj = date.today()
        data_inicio = data_inicio_obj.strftime('%Y-%m-%d')
        data_fim = data_fim_obj.strftime('%Y-%m-%d')
    
    # Buscar presenças no período
    presencas = Presenca.objects.filter(
        data_presenca__range=[data_inicio_obj, data_fim_obj]
    ).select_related('aluno', 'lancada_por').order_by('-data_presenca', 'aluno__nome')
    
    # Estatísticas
    total_presencas = presencas.count()
    total_presentes = presencas.filter(presente=True).count()
    total_faltas = presencas.filter(presente=False).count()
    
    context = {
        'presencas': presencas,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_presencas': total_presencas,
        'total_presentes': total_presentes,
        'total_faltas': total_faltas,
    }
    
    return render(request, 'gamificacao/gerenciar_presencas.html', context)


@login_required
def lancar_presenca(request):
    """View para lançar nova presença"""
    if request.method == 'POST':
        form = PresencaForm(request.POST)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.lancada_por = request.user
            presenca.save()
            
            status = 'presente' if presenca.presente else 'faltou'
            messages.success(request, f'Presença de {presenca.aluno.nome} lançada com sucesso ({status})!')
            return redirect('gerenciar_presencas')
    else:
        form = PresencaForm()
    
    context = {
        'form': form,
        'titulo': 'Lançar Presença',
        'is_edit': False
    }
    
    return render(request, 'gamificacao/form_presenca.html', context)


@login_required
def editar_presenca(request, pk):
    """View para editar presença existente"""
    presenca = get_object_or_404(Presenca, pk=pk)
    
    if request.method == 'POST':
        form = PresencaForm(request.POST, instance=presenca)
        if form.is_valid():
            presenca = form.save(commit=False)
            presenca.save()
            
            status = 'presente' if presenca.presente else 'faltou'
            messages.success(request, f'Presença de {presenca.aluno.nome} atualizada com sucesso ({status})!')
            return redirect('gerenciar_presencas')
    else:
        form = PresencaForm(instance=presenca)
    
    context = {
        'form': form,
        'presenca': presenca,
        'titulo': f'Editar Presença - {presenca.aluno.nome}',
        'is_edit': True
    }
    
    return render(request, 'gamificacao/form_presenca.html', context)


@login_required
def deletar_presenca(request, pk):
    """View para deletar presença"""
    presenca = get_object_or_404(Presenca, pk=pk)
    
    if request.method == 'POST':
        aluno_nome = presenca.aluno.nome
        data_presenca = presenca.data_presenca.strftime('%d/%m/%Y')
        presenca.delete()
        messages.success(request, f'Presença de {aluno_nome} do dia {data_presenca} excluída com sucesso!')
        return redirect('gerenciar_presencas')
    
    return render(request, 'gamificacao/confirmar_delete.html', {
        'object': presenca,
        'object_type': 'presença',
        'object_name': f'{presenca.aluno.nome} - {presenca.data_presenca.strftime("%d/%m/%Y")}',
        'cancel_url': 'gerenciar_presencas'
    })


@login_required
def lancar_presenca_multipla(request):
    """View para lançar presença de vários alunos de uma vez"""
    from datetime import date
    
    if request.method == 'POST':
        data_presenca = request.POST.get('data_presenca')
        alunos_selecionados = request.POST.getlist('alunos')
        
        if not data_presenca:
            messages.error(request, 'Data da presença é obrigatória!')
            return redirect('lancar_presenca_multipla')
            
        if not alunos_selecionados:
            messages.error(request, 'Selecione pelo menos um aluno!')
            return redirect('lancar_presenca_multipla')
        
        try:
            data_obj = date.fromisoformat(data_presenca)
        except ValueError:
            messages.error(request, 'Data inválida!')
            return redirect('lancar_presenca_multipla')
        
        # Lançar presenças
        count = 0
        for aluno_id in alunos_selecionados:
            try:
                aluno = Aluno.objects.get(id=aluno_id, ativo=True)
                # Verificar se já existe presença para este aluno nesta data
                if not Presenca.objects.filter(aluno=aluno, data_presenca=data_obj).exists():
                    Presenca.objects.create(
                        aluno=aluno,
                        data_presenca=data_obj,
                        presente=True,
                        lancada_por=request.user
                    )
                    count += 1
            except Aluno.DoesNotExist:
                continue
        
        if count > 0:
            messages.success(request, f'Presença lançada para {count} aluno(s) com sucesso!')
        else:
            messages.warning(request, 'Nenhuma presença foi lançada (já existiam registros para a data selecionada).')
            
        return redirect('gerenciar_presencas')
    
    # GET - mostrar formulário
    alunos = Aluno.objects.filter(ativo=True).order_by('nome')
    data_hoje = date.today().strftime('%Y-%m-%d')
    
    context = {
        'alunos': alunos,
        'data_hoje': data_hoje,
    }
    
    return render(request, 'gamificacao/presenca_multipla.html', context)


# ==================== VIEWS DE GRUPOS ====================

@login_required
def gerenciar_grupos(request):
    """View para listar todos os grupos"""
    grupos = Grupo.objects.filter(ativo=True).order_by('nome')
    
    # Adicionar informações extras para cada grupo
    grupos_info = []
    for grupo in grupos:
        membros = grupo.membros.select_related('aluno').all()
        ranking = []
        
        for i, membro in enumerate(membros):
            aluno = membro.aluno
            ranking.append({
                'posicao': i + 1,
                'aluno': aluno,
                'pontuacao': float(aluno.pontuacao_total)
            })
        
        # Ordenar por pontuação
        ranking.sort(key=lambda x: (-x['pontuacao'], x['aluno'].nome))
        
        # Reajustar posições após ordenação
        for i, item in enumerate(ranking):
            item['posicao'] = i + 1
        
        grupos_info.append({
            'grupo': grupo,
            'ranking': ranking,
            'total_membros': len(ranking),
            'media_grupo': grupo.media_grupo
        })
    
    context = {
        'grupos_info': grupos_info,
    }
    
    return render(request, 'gamificacao/gerenciar_grupos.html', context)


@login_required
def criar_grupo(request):
    """View para criar um novo grupo"""
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.criado_por = request.user
            grupo.save()
            messages.success(request, f'Grupo "{grupo.nome}" criado com sucesso!')
            return redirect('gerenciar_grupos')
    else:
        form = GrupoForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Novo Grupo'
    }
    
    return render(request, 'gamificacao/form_grupo.html', context)


@login_required
def editar_grupo(request, grupo_id):
    """View para editar um grupo"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, f'Grupo "{grupo.nome}" atualizado com sucesso!')
            return redirect('gerenciar_grupos')
    else:
        form = GrupoForm(instance=grupo)
    
    context = {
        'form': form,
        'grupo': grupo,
        'titulo': f'Editar Grupo: {grupo.nome}'
    }
    
    return render(request, 'gamificacao/form_grupo.html', context)


@login_required
def deletar_grupo(request, grupo_id):
    """View para deletar um grupo"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    if request.method == 'POST':
        nome_grupo = grupo.nome
        grupo.delete()
        messages.success(request, f'Grupo "{nome_grupo}" deletado com sucesso!')
        return redirect('gerenciar_grupos')
    
    context = {
        'objeto': grupo,
        'tipo': 'grupo',
        'titulo': f'Deletar Grupo: {grupo.nome}',
        'url_voltar': 'gerenciar_grupos'
    }
    
    return render(request, 'gamificacao/confirmar_delete.html', context)


@login_required
def adicionar_membros(request, grupo_id):
    """View para adicionar alunos ao grupo"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    
    if request.method == 'POST':
        form = AdicionarMembrosForm(request.POST, grupo=grupo)
        # Passar grupo instance para validação
        form.grupo_instance = grupo
        
        if form.is_valid():
            alunos_selecionados = form.cleaned_data['alunos']
            lider_escolhido = form.cleaned_data.get('lider')
            adicionados = 0
            
            for aluno in alunos_selecionados:
                membro, created = MembroGrupo.objects.get_or_create(
                    grupo=grupo,
                    aluno=aluno,
                    defaults={'adicionado_por': request.user}
                )
                if created:
                    adicionados += 1
            
            # Definir líder se foi escolhido
            if lider_escolhido:
                grupo.lider = lider_escolhido
                grupo.save()
            
            if adicionados > 0:
                messages.success(request, f'{adicionados} aluno(s) adicionado(s) ao grupo "{grupo.nome}"!')
            else:
                messages.info(request, 'Nenhum aluno novo foi adicionado.')
                
            if lider_escolhido:
                messages.success(request, f'"{lider_escolhido.nome}" foi definido como líder do grupo!')
            
            return redirect('gerenciar_grupos')
    else:
        form = AdicionarMembrosForm(grupo=grupo)
    
    context = {
        'form': form,
        'grupo': grupo,
        'titulo': f'Adicionar Membros ao Grupo: {grupo.nome}'
    }
    
    return render(request, 'gamificacao/adicionar_membros.html', context)


@login_required
def remover_membro(request, grupo_id, aluno_id):
    """View para remover um aluno do grupo"""
    grupo = get_object_or_404(Grupo, id=grupo_id)
    aluno = get_object_or_404(Aluno, id=aluno_id)
    
    try:
        membro = MembroGrupo.objects.get(grupo=grupo, aluno=aluno)
        nome_aluno = aluno.nome
        membro.delete()
        messages.success(request, f'"{nome_aluno}" foi removido do grupo "{grupo.nome}"!')
    except MembroGrupo.DoesNotExist:
        messages.error(request, 'Este aluno não está no grupo.')
    
    return redirect('gerenciar_grupos')


# ============= VIEWS CAÇA-NÍQUEL =============

@login_required
def caca_niquel_interface(request):
    """Interface principal do caça-níquel"""
    context = {
        'alunos': Aluno.objects.all(),
        'recompensas_recentes': CacaNiquel.objects.select_related('aluno')[:10],
    }
    return render(request, 'gamificacao/caca_niquel.html', context)


@login_required 
@require_http_methods(["POST"])
@csrf_exempt
def jogar_caca_niquel(request):
    """Processa uma jogada do caça-níquel"""
    # Verificar se está autenticado
    if not request.user.is_authenticated:
        return JsonResponse({'erro': 'Usuário não autenticado'}, status=401)
    try:
        aluno_id = request.POST.get('aluno_id')
        
        if not aluno_id:
            return JsonResponse({'erro': 'Aluno não selecionado'}, status=400)
        
        try:
            aluno = Aluno.objects.get(id=aluno_id)
        except Aluno.DoesNotExist:
            return JsonResponse({'erro': 'Aluno não encontrado'}, status=404)
        
        # Sistema de probabilidades
        recompensas_probabilidade = [
            ('salgado', 50),      # 50% chance
            ('doce', 35),         # 35% chance  
            ('vale_trabalho', 8), # 8% chance
            ('5_reais', 5),       # 5% chance
            ('10_reais', 2),      # 2% chance
        ]
        
        # Gerar número aleatório de 1-100
        numero_sorteado = random.randint(1, 100)
        
        # Determinar recompensa baseada na probabilidade
        acumulado = 0
        recompensa_ganha = 'salgado'  # fallback
        
        for recompensa, chance in recompensas_probabilidade:
            acumulado += chance
            if numero_sorteado <= acumulado:
                recompensa_ganha = recompensa
                break
        
        # Salvar no banco de dados
        jogada = CacaNiquel.objects.create(
            aluno=aluno,
            recompensa=recompensa_ganha
        )
        
        # Retornar resultado
        recompensas_display = {
            '10_reais': {'emoji': '💰', 'texto': 'R$ 10,00', 'classe': 'premio-dourado'},
            '5_reais': {'emoji': '💵', 'texto': 'R$ 5,00', 'classe': 'premio-prata'},
            'vale_trabalho': {'emoji': '📝', 'texto': 'Vale-trabalho', 'classe': 'premio-bronze'},
            'doce': {'emoji': '🍭', 'texto': 'Doce', 'classe': 'premio-comum'},
            'salgado': {'emoji': '🥨', 'texto': 'Salgado', 'classe': 'premio-comum'},
        }
        
        resultado = recompensas_display.get(recompensa_ganha, recompensas_display['salgado'])
        
        return JsonResponse({
            'sucesso': True,
            'aluno': aluno.nome,
            'recompensa': {
                'tipo': recompensa_ganha,
                'emoji': resultado['emoji'],
                'texto': resultado['texto'],
                'classe': resultado['classe']
            },
            'numero_sorteado': numero_sorteado,
            'jogada_id': jogada.id
        })
        
    except Exception as e:
        # Log do erro para debug
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro no caça-níquel: {str(e)}", exc_info=True)
        
        return JsonResponse({
            'erro': f'Erro interno do servidor: {str(e)}'
        }, status=500)


@login_required
def historico_caca_niquel(request):
    """Página com histórico de jogadas do caça-níquel"""
    jogadas = CacaNiquel.objects.select_related('aluno').order_by('-data_jogada')
    
    # Paginação
    paginator = Paginator(jogadas, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estatísticas
    total_jogadas = CacaNiquel.objects.count()
    premios_resgatados = CacaNiquel.objects.filter(resgatado=True).count()
    premios_pendentes = CacaNiquel.objects.filter(resgatado=False).count()
    
    # Estatísticas por tipo de recompensa
    from django.db.models import Count
    stats_recompensas = (
        CacaNiquel.objects
        .values('recompensa')
        .annotate(quantidade=Count('recompensa'))
        .order_by('-quantidade')
    )
    
    context = {
        'page_obj': page_obj,
        'total_jogadas': total_jogadas,
        'premios_resgatados': premios_resgatados,
        'premios_pendentes': premios_pendentes,
        'stats_recompensas': stats_recompensas,
    }
    
    return render(request, 'gamificacao/historico_caca_niquel.html', context)


@login_required
@require_http_methods(["POST"])
def marcar_resgatado(request, jogada_id):
    """Marca uma recompensa como resgatada"""
    try:
        jogada = CacaNiquel.objects.get(id=jogada_id)
        jogada.resgatado = True
        jogada.data_resgate = timezone.now()
        jogada.resgatado_por = request.user
        jogada.save()
        
        messages.success(request, f'Recompensa de {jogada.aluno.nome} marcada como resgatada!')
        return JsonResponse({'sucesso': True})
        
    except CacaNiquel.DoesNotExist:
        return JsonResponse({'erro': 'Jogada não encontrada'}, status=404)


@login_required  
@require_http_methods(["POST"])
def excluir_premio(request, jogada_id):
    """Exclui um prêmio permanentemente"""
    try:
        jogada = CacaNiquel.objects.get(id=jogada_id, resgatado=False)
        
        # Log da exclusão para auditoria
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Prêmio excluído: ID={jogada.id}, Aluno={jogada.aluno.nome}, "
                     f"Recompensa={jogada.get_recompensa_display()}, "
                     f"Data_jogada={jogada.data_jogada}, Excluído_por={request.user.username}")
        
        # Salvar informações antes de excluir
        nome_aluno = jogada.aluno.nome
        recompensa = jogada.get_recompensa_display()
        
        # Excluir a jogada
        jogada.delete()
        
        messages.warning(request, 
                       f'⚠️ Prêmio "{recompensa}" de {nome_aluno} foi excluído permanentemente!')
        
        return JsonResponse({'sucesso': True})
        
    except CacaNiquel.DoesNotExist:
        return JsonResponse({'erro': 'Prêmio não encontrado ou já resgatado'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': f'Erro interno: {str(e)}'}, status=500)


@login_required
def premios_pendentes(request):
    """Lista de prêmios ainda não resgatados"""
    premios = CacaNiquel.objects.filter(resgatado=False).select_related('aluno').order_by('-data_jogada')
    
    # Calcular totais por tipo de prêmio
    total_10_reais = premios.filter(recompensa='10_reais').count()
    total_5_reais = premios.filter(recompensa='5_reais').count()
    total_vale_trabalho = premios.filter(recompensa='vale_trabalho').count()
    total_lanches = premios.filter(recompensa__in=['doce', 'salgado']).count()
    
    context = {
        'premios': premios,
        'total_10_reais': total_10_reais,
        'total_5_reais': total_5_reais,
        'total_vale_trabalho': total_vale_trabalho,
        'total_lanches': total_lanches,
    }
    
    return render(request, 'gamificacao/premios_pendentes.html', context)
