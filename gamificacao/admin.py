from django.contrib import admin
from django.db import models
from .models import Aluno, Atividade, Nota, HistoricoNota, CacaNiquel


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'email', 'nota_atual', 'total_atividades', 'ativo', 'data_criacao')
    list_filter = ('ativo', 'data_criacao')
    search_fields = ('nome', 'matricula', 'email')
    list_editable = ('ativo',)
    readonly_fields = ('data_criacao', 'nota_atual', 'total_atividades')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'matricula', 'email')
        }),
        ('Status', {
            'fields': ('ativo',)
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'nota_atual', 'total_atividades'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'valor_maximo', 'media_turma', 'data_entrega', 'ativa', 'data_criacao')
    list_filter = ('ativa', 'data_criacao', 'data_entrega')
    search_fields = ('nome', 'descricao')
    list_editable = ('ativa',)
    readonly_fields = ('data_criacao', 'media_turma')
    date_hierarchy = 'data_entrega'
    
    fieldsets = (
        ('Informações da Atividade', {
            'fields': ('nome', 'descricao', 'valor_maximo')
        }),
        ('Datas', {
            'fields': ('data_entrega',)
        }),
        ('Status', {
            'fields': ('ativa',)
        }),
        ('Estatísticas', {
            'fields': ('media_turma',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'atividade', 'valor', 'data_lancamento', 'lancada_por')
    list_filter = ('atividade', 'data_lancamento', 'lancada_por')
    search_fields = ('aluno__nome', 'atividade__nome')
    readonly_fields = ('data_lancamento', 'data_atualizacao')
    autocomplete_fields = ('aluno', 'atividade')
    
    fieldsets = (
        ('Nota', {
            'fields': ('aluno', 'atividade', 'valor')
        }),
        ('Detalhes', {
            'fields': ('observacoes', 'lancada_por')
        }),
        ('Datas', {
            'fields': ('data_lancamento', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Se é uma nova nota
            obj.lancada_por = request.user
        else:  # Se está editando uma nota existente
            # Criar histórico da alteração
            if 'valor' in form.changed_data:
                HistoricoNota.objects.create(
                    nota=obj,
                    valor_anterior=form.initial.get('valor', 0),
                    valor_novo=obj.valor,
                    motivo='Alteração via admin',
                    usuario=request.user
                )
        super().save_model(request, obj, form, change)


@admin.register(HistoricoNota)
class HistoricoNotaAdmin(admin.ModelAdmin):
    list_display = ('nota', 'valor_anterior', 'valor_novo', 'usuario', 'data_alteracao')
    list_filter = ('data_alteracao', 'usuario')
    search_fields = ('nota__aluno__nome', 'nota__atividade__nome', 'motivo')
    readonly_fields = ('data_alteracao',)
    
    def has_add_permission(self, request):
        return False  # Não permite adicionar histórico manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # Não permite editar histórico


@admin.register(CacaNiquel)
class CacaNiquelAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'get_recompensa_display', 'data_jogada', 'resgatado', 'data_resgate', 'resgatado_por')
    list_filter = ('recompensa', 'resgatado', 'data_jogada')
    search_fields = ('aluno__nome', 'aluno__matricula')
    list_editable = ('resgatado',)
    readonly_fields = ('data_jogada', 'valor_recompensa')
    date_hierarchy = 'data_jogada'
    
    fieldsets = (
        ('Informações da Jogada', {
            'fields': ('aluno', 'recompensa', 'data_jogada', 'valor_recompensa')
        }),
        ('Status do Resgate', {
            'fields': ('resgatado', 'data_resgate', 'resgatado_por')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Se está marcando como resgatado e não tinha sido resgatado antes
        if change and obj.resgatado and not obj.data_resgate:
            from django.utils import timezone
            obj.data_resgate = timezone.now()
            obj.resgatado_por = request.user
        super().save_model(request, obj, form, change)
    
    # Estatísticas no admin
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        from django.db.models import Count
        
        stats = CacaNiquel.objects.aggregate(
            total_jogadas=Count('id'),
            resgatados=Count('id', filter=models.Q(resgatado=True)),
            pendentes=Count('id', filter=models.Q(resgatado=False))
        )
        
        recompensas_stats = (
            CacaNiquel.objects
            .values('recompensa')
            .annotate(quantidade=Count('recompensa'))
            .order_by('-quantidade')
        )
        
        extra_context['stats'] = stats
        extra_context['recompensas_stats'] = recompensas_stats
        
        return super().changelist_view(request, extra_context)


# Configurações adicionais do admin
admin.site.site_header = 'Sistema de Gamificação Escolar'
admin.site.site_title = 'Gamificação'
admin.site.index_title = 'Painel de Administração'
