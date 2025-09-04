from django.urls import path
from . import views

urlpatterns = [
    # Autenticação
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard principal
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Histórico de notas
    path('historico/', views.historico_notas, name='historico_notas'),
    
    # Gerenciamento de alunos
    path('alunos/', views.gerenciar_alunos, name='gerenciar_alunos'),
    path('alunos/criar/', views.criar_aluno, name='criar_aluno'),
    path('alunos/<int:pk>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:pk>/deletar/', views.deletar_aluno, name='deletar_aluno'),
    
    # Gerenciamento de atividades
    path('atividades/', views.gerenciar_atividades, name='gerenciar_atividades'),
    path('atividades/criar/', views.criar_atividade, name='criar_atividade'),
    path('atividades/<int:pk>/editar/', views.editar_atividade, name='editar_atividade'),
    path('atividades/<int:pk>/deletar/', views.deletar_atividade, name='deletar_atividade'),
    
    # Gerenciamento de notas
    path('notas/', views.gerenciar_notas, name='gerenciar_notas'),
    path('notas/atividade/<int:atividade_id>/', views.gerenciar_notas_atividade, name='gerenciar_notas_atividade'),
    path('notas/atividade/<int:atividade_id>/lancar/', views.lancar_nota, name='lancar_nota'),
    path('notas/atividade/<int:atividade_id>/aluno/<int:aluno_id>/lancar/', views.lancar_nota_aluno, name='lancar_nota_aluno'),
    path('notas/atividade/<int:atividade_id>/aluno/<int:aluno_id>/editar/', views.editar_nota, name='editar_nota'),
    path('notas/delete/<int:nota_id>/', views.deletar_nota, name='deletar_nota'),
    
    # Gerenciamento de presenças
    path('presencas/', views.gerenciar_presencas, name='gerenciar_presencas'),
    path('presencas/lancar/', views.lancar_presenca, name='lancar_presenca'),
    path('presencas/lancar-multipla/', views.lancar_presenca_multipla, name='lancar_presenca_multipla'),
    path('presencas/<int:pk>/editar/', views.editar_presenca, name='editar_presenca'),
    path('presencas/<int:pk>/deletar/', views.deletar_presenca, name='deletar_presenca'),
    
    # Gerenciamento de grupos
    path('grupos/', views.gerenciar_grupos, name='gerenciar_grupos'),
    path('grupos/criar/', views.criar_grupo, name='criar_grupo'),
    path('grupos/<int:grupo_id>/editar/', views.editar_grupo, name='editar_grupo'),
    path('grupos/<int:grupo_id>/deletar/', views.deletar_grupo, name='deletar_grupo'),
    path('grupos/<int:grupo_id>/adicionar-membros/', views.adicionar_membros, name='adicionar_membros'),
    path('grupos/<int:grupo_id>/remover-membro/<int:aluno_id>/', views.remover_membro, name='remover_membro'),
    
    # Caça-níquel
    path('caca-niquel/', views.caca_niquel_interface, name='caca_niquel'),
    path('caca-niquel/jogar/', views.jogar_caca_niquel, name='jogar_caca_niquel'),
    path('caca-niquel/historico/', views.historico_caca_niquel, name='historico_caca_niquel'),
    path('caca-niquel/premios-pendentes/', views.premios_pendentes, name='premios_pendentes'),
    path('caca-niquel/marcar-resgatado/<int:jogada_id>/', views.marcar_resgatado, name='marcar_resgatado'),
    path('caca-niquel/excluir-premio/<int:jogada_id>/', views.excluir_premio, name='excluir_premio'),
]
