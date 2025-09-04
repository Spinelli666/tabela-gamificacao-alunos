from django import forms
from .models import Aluno, Atividade, Nota, Presenca, Grupo, MembroGrupo


class AlunoForm(forms.ModelForm):
    """Formulário para criação e edição de alunos"""
    
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do aluno'
            }),
            'matricula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Matrícula única'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@exemplo.com'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nome': 'Nome Completo',
            'matricula': 'Matrícula',
            'email': 'E-mail',
            'ativo': 'Aluno Ativo'
        }


class AtividadeForm(forms.ModelForm):
    """Formulário para criação e edição de atividades"""
    
    class Meta:
        model = Atividade
        fields = ['nome', 'descricao', 'data_entrega', 'valor_maximo', 'ativa']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da atividade'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da atividade (opcional)'
            }),
            'data_entrega': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'valor_maximo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'step': '0.1'
            }),
            'ativa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nome': 'Nome da Atividade',
            'descricao': 'Descrição',
            'data_entrega': 'Data de Entrega',
            'valor_maximo': 'Valor Máximo',
            'ativa': 'Atividade Ativa'
        }


class NotaForm(forms.ModelForm):
    """Formulário para lançamento e edição de notas"""
    motivo_alteracao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Motivo da alteração (opcional)'
        }),
        label='Motivo da Alteração',
        help_text='Apenas necessário quando estiver editando uma nota existente'
    )
    
    class Meta:
        model = Nota
        fields = ['aluno', 'valor', 'observacoes']
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'form-select'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '10',
                'step': '0.1'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre a nota (opcional)'
            })
        }
        labels = {
            'aluno': 'Aluno',
            'valor': 'Nota',
            'observacoes': 'Observações'
        }
    
    def __init__(self, *args, **kwargs):
        self.atividade = kwargs.pop('atividade', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar apenas alunos ativos
        self.fields['aluno'].queryset = Aluno.objects.filter(ativo=True).order_by('nome')
        
        # Se a atividade foi passada, ajustar o valor máximo
        if self.atividade:
            self.fields['valor'].widget.attrs['max'] = str(float(self.atividade.valor_maximo))
            self.fields['valor'].help_text = f'Valor máximo: {self.atividade.valor_maximo}'
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if self.atividade and valor and valor > self.atividade.valor_maximo:
            raise forms.ValidationError(
                f'A nota não pode ser maior que o valor máximo da atividade ({self.atividade.valor_maximo})'
            )
        return valor


class FiltroNotasForm(forms.Form):
    """Formulário para filtrar notas no histórico"""
    atividade = forms.ModelChoiceField(
        queryset=Atividade.objects.filter(ativa=True).order_by('-data_criacao'),
        required=False,
        empty_label='Todas as atividades',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    aluno = forms.ModelChoiceField(
        queryset=Aluno.objects.filter(ativo=True).order_by('nome'),
        required=False,
        empty_label='Todos os alunos',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Data Início'
    )
    
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        label='Data Fim'
    )


class PresencaForm(forms.ModelForm):
    """Formulário para lançamento e edição de presenças"""
    
    class Meta:
        model = Presenca
        fields = ['aluno', 'data_presenca', 'presente', 'observacoes']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar widgets e estilos
        self.fields['aluno'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['data_presenca'].widget.attrs.update({
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['presente'].widget.attrs.update({
            'class': 'form-check-input'
        })
        self.fields['observacoes'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Observações opcionais...'
        })
        
        # Labels
        self.fields['aluno'].label = 'Aluno'
        self.fields['data_presenca'].label = 'Data da Presença'
        self.fields['presente'].label = 'Presente'
        self.fields['observacoes'].label = 'Observações'
        
    def clean_data_presenca(self):
        """Validação da data de presença"""
        data_presenca = self.cleaned_data.get('data_presenca')
        
        if data_presenca:
            from datetime import date
            if data_presenca > date.today():
                raise forms.ValidationError('A data de presença não pode ser no futuro.')
                
        return data_presenca


class GrupoForm(forms.ModelForm):
    """Formulário para criação e edição de grupos"""
    
    class Meta:
        model = Grupo
        fields = ['nome', 'descricao', 'ativo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do grupo'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do grupo (opcional)'
            }),
            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'nome': 'Nome do Grupo',
            'descricao': 'Descrição',
            'ativo': 'Grupo Ativo'
        }


class AdicionarMembrosForm(forms.Form):
    """Formulário para adicionar múltiplos alunos a um grupo"""
    alunos = forms.ModelMultipleChoiceField(
        queryset=Aluno.objects.filter(ativo=True),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        label='Selecionar Alunos',
        required=True
    )
    
    lider = forms.ModelChoiceField(
        queryset=Aluno.objects.filter(ativo=True),
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        }),
        label='Escolher Líder do Grupo',
        required=False,
        empty_label='Nenhum líder'
    )
    
    def __init__(self, *args, **kwargs):
        grupo = kwargs.pop('grupo', None)
        super().__init__(*args, **kwargs)
        
        if grupo:
            # Excluir alunos que já estão no grupo
            alunos_no_grupo = [membro.aluno.id for membro in grupo.membros.all()]
            alunos_disponiveis = Aluno.objects.filter(
                ativo=True
            ).exclude(id__in=alunos_no_grupo)
            
            self.fields['alunos'].queryset = alunos_disponiveis
            
            # Para o campo líder, incluir alunos já no grupo + novos alunos
            alunos_grupo_existentes = [membro.aluno for membro in grupo.membros.all()]
            todos_alunos_opcoes = list(alunos_grupo_existentes) + list(alunos_disponiveis)
            
            # Ordenar por nome
            todos_alunos_opcoes.sort(key=lambda x: x.nome)
            
            # Criar queryset personalizado
            ids_todos_alunos = [aluno.id for aluno in todos_alunos_opcoes]
            self.fields['lider'].queryset = Aluno.objects.filter(id__in=ids_todos_alunos).order_by('nome')
            
            # Definir valor inicial se já há líder
            if grupo.lider:
                self.fields['lider'].initial = grupo.lider

    def clean(self):
        cleaned_data = super().clean()
        lider = cleaned_data.get('lider')
        alunos = cleaned_data.get('alunos', [])
        
        # Se um líder foi escolhido, verificar se ele está na lista de alunos selecionados ou já no grupo
        if lider and hasattr(self, 'grupo_instance'):
            grupo = self.grupo_instance
            alunos_no_grupo = [membro.aluno for membro in grupo.membros.all()]
            
            if lider not in alunos and lider not in alunos_no_grupo:
                raise forms.ValidationError(
                    'O líder escolhido deve estar entre os membros do grupo.'
                )
        
        return cleaned_data
