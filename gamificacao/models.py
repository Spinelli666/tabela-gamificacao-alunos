from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Aluno(models.Model):
    """Modelo para representar um aluno"""
    nome = models.CharField(max_length=200, verbose_name='Nome')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    matricula = models.CharField(max_length=20, unique=True, verbose_name='Matrícula')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def nota_atual(self):
        """Retorna a média das notas do aluno"""
        notas = self.nota_set.all()
        if notas:
            return round(sum(nota.valor for nota in notas) / len(notas), 2)
        return 0.0

    @property
    def total_atividades(self):
        """Retorna o total de atividades realizadas"""
        return self.nota_set.count()

    @property
    def pontos_presenca(self):
        """Retorna o total de pontos de presença do aluno (+1 por presença, -0.5 por falta)"""
        presencas = self.presenca_set.all()
        pontos = 0
        for presenca in presencas:
            if presenca.presente:
                pontos += 1  # +1 ponto por presença
            else:
                pontos -= 0.5  # -0.5 pontos por falta
        return round(pontos, 1)

    @property
    def total_presencas(self):
        """Retorna o total de presenças registradas"""
        return self.presenca_set.count()

    @property
    def percentual_presenca(self):
        """Retorna o percentual de presença do aluno"""
        total = self.total_presencas
        if total > 0:
            presentes = self.presenca_set.filter(presente=True).count()
            return round((presentes / total) * 100, 1)
        return 0.0

    @property
    def meus_grupos(self):
        """Retorna os grupos que o aluno pertence"""
        return [membro.grupo for membro in self.grupos.all()]

    @property
    def pontuacao_total(self):
        """Retorna a pontuação total (nota + presença)"""
        return round(self.nota_atual + self.pontos_presenca, 2)


class Atividade(models.Model):
    """Modelo para representar uma atividade/avaliação"""
    nome = models.CharField(max_length=200, verbose_name='Nome da Atividade')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_entrega = models.DateTimeField(blank=True, null=True, verbose_name='Data de Entrega')
    valor_maximo = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        default=10.0, 
        verbose_name='Valor Máximo'
    )
    ativa = models.BooleanField(default=True, verbose_name='Ativa')

    class Meta:
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.nome

    @property
    def media_turma(self):
        """Retorna a média da turma nesta atividade"""
        notas = self.nota_set.all()
        if notas:
            return round(sum(nota.valor for nota in notas) / len(notas), 2)
        return 0.0


class Nota(models.Model):
    """Modelo para representar uma nota de um aluno em uma atividade"""
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE, verbose_name='Atividade')
    valor = models.DecimalField(
        max_digits=4, 
        decimal_places=1,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name='Nota'
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    data_lancamento = models.DateTimeField(auto_now_add=True, verbose_name='Data de Lançamento')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    lancada_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Lançada por'
    )

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        unique_together = ('aluno', 'atividade')  # Um aluno não pode ter duas notas para a mesma atividade
        ordering = ['-data_lancamento']

    def __str__(self):
        return f'{self.aluno.nome} - {self.atividade.nome}: {self.valor}'


class HistoricoNota(models.Model):
    """Modelo para manter histórico de alterações das notas"""
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE, verbose_name='Nota')
    valor_anterior = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        verbose_name='Valor Anterior'
    )
    valor_novo = models.DecimalField(
        max_digits=4, 
        decimal_places=1, 
        verbose_name='Valor Novo'
    )
    motivo = models.CharField(max_length=500, verbose_name='Motivo da Alteração')
    usuario = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Usuário'
    )
    data_alteracao = models.DateTimeField(auto_now_add=True, verbose_name='Data da Alteração')

    class Meta:
        verbose_name = 'Histórico de Nota'
        verbose_name_plural = 'Histórico de Notas'
        ordering = ['-data_alteracao']

    def __str__(self):
        return f'{self.nota.aluno.nome} - {self.nota.atividade.nome}: {self.valor_anterior} → {self.valor_novo}'


class Presenca(models.Model):
    """Modelo para controlar a presença dos alunos"""
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    data_presenca = models.DateField(verbose_name='Data da Presença')
    presente = models.BooleanField(default=True, verbose_name='Presente')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')
    data_lancamento = models.DateTimeField(auto_now_add=True, verbose_name='Data de Lançamento')
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    lancada_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Lançada por'
    )

    class Meta:
        verbose_name = 'Presença'
        verbose_name_plural = 'Presenças'
        unique_together = ('aluno', 'data_presenca')  # Um aluno não pode ter duas presenças para o mesmo dia
        ordering = ['-data_presenca', 'aluno__nome']

    def __str__(self):
        status = 'Presente' if self.presente else 'Faltou'
        return f'{self.aluno.nome} - {self.data_presenca.strftime("%d/%m/%Y")} - {status}'

    @property
    def pontos(self):
        """Retorna os pontos ganhos pela presença (+1 se presente, -0.5 se faltou)"""
        return 1 if self.presente else -0.5


class Grupo(models.Model):
    """Modelo para representar um grupo de alunos"""
    nome = models.CharField(max_length=100, verbose_name='Nome do Grupo')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    lider = models.ForeignKey(
        'Aluno',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grupos_liderados',
        verbose_name='Líder do Grupo'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    criado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Criado por'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    @property
    def total_membros(self):
        """Retorna o total de membros do grupo"""
        return self.membros.count()

    @property
    def alunos(self):
        """Retorna os alunos do grupo"""
        from django.db import models
        return models.QuerySet(model=Aluno).filter(grupos__grupo=self)

    @property
    def media_grupo(self):
        """Retorna a média de pontos do grupo"""
        alunos_grupo = [membro.aluno for membro in self.membros.all()]
        if alunos_grupo:
            total_pontos = sum(float(aluno.pontuacao_total) for aluno in alunos_grupo)
            return round(total_pontos / len(alunos_grupo), 2)
        return 0.0

    def get_ranking_grupo(self):
        """Retorna os alunos do grupo ordenados por pontuação"""
        membros = self.membros.select_related('aluno').all()
        alunos_com_pontos = [(membro.aluno, float(membro.aluno.pontuacao_total)) for membro in membros]
        alunos_ordenados = sorted(alunos_com_pontos, key=lambda x: (-x[1], x[0].nome))
        return [aluno for aluno, _ in alunos_ordenados]


class MembroGrupo(models.Model):
    """Modelo para relacionar alunos com grupos (permite múltiplos grupos)"""
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='membros')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='grupos')
    data_adicao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Adição')
    adicionado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Adicionado por'
    )

    class Meta:
        verbose_name = 'Membro do Grupo'
        verbose_name_plural = 'Membros do Grupo'
        unique_together = ('grupo', 'aluno')  # Um aluno não pode estar no mesmo grupo duas vezes
        ordering = ['data_adicao']

    def __str__(self):
        return f'{self.aluno.nome} - {self.grupo.nome}'


class CacaNiquel(models.Model):
    """Modelo para registrar as jogadas no caça-níquel"""
    RECOMPENSAS_CHOICES = [
        ('10_reais', '💰 R$ 10,00'),
        ('5_reais', '💵 R$ 5,00'), 
        ('vale_trabalho', '📝 Vale-trabalho'),
        ('doce', '🍭 Doce'),
        ('salgado', '🥨 Salgado'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Aluno')
    recompensa = models.CharField(max_length=20, choices=RECOMPENSAS_CHOICES, verbose_name='Recompensa')
    data_jogada = models.DateTimeField(auto_now_add=True, verbose_name='Data da Jogada')
    resgatado = models.BooleanField(default=False, verbose_name='Resgatado')
    data_resgate = models.DateTimeField(null=True, blank=True, verbose_name='Data do Resgate')
    resgatado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Resgatado por'
    )

    class Meta:
        verbose_name = 'Caça-níquel'
        verbose_name_plural = 'Caça-níquel'
        ordering = ['-data_jogada']

    def __str__(self):
        status = '✅ Resgatado' if self.resgatado else '⏳ Pendente'
        return f'{self.aluno.nome} - {self.get_recompensa_display()} ({status})'

    @property
    def valor_recompensa(self):
        """Retorna o valor monetário da recompensa"""
        valores = {
            '10_reais': 10.00,
            '5_reais': 5.00,
            'vale_trabalho': 0.00,
            'doce': 2.00,  # Valor estimado
            'salgado': 3.00,  # Valor estimado
        }
        return valores.get(self.recompensa, 0.00)
