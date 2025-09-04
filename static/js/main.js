// Sistema de temas
const temas = {
    hotline: 'Hotline Miami',
    cyberpunk: 'Cyberpunk 2077', 
    synthwave: 'Synthwave'
};

let temaAtual = localStorage.getItem('tema') || 'hotline';

function aplicarTema(tema) {
    // Remove classes de tema anteriores
    document.body.classList.remove('tema-cyberpunk', 'tema-synthwave');
    
    // Aplica nova classe de tema
    if (tema === 'cyberpunk') {
        document.body.classList.add('tema-cyberpunk');
    } else if (tema === 'synthwave') {
        document.body.classList.add('tema-synthwave');
    }
    
    // Salva no localStorage
    localStorage.setItem('tema', tema);
    temaAtual = tema;
    
    // Atualiza botões do theme switcher se existirem
    const themeBtns = document.querySelectorAll('.theme-btn');
    themeBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.theme === tema);
        if (btn.dataset.theme === tema) {
            btn.innerHTML = '<i class="fas fa-check-circle me-2" style="color: var(--cor-success);"></i>' + btn.textContent.replace('✓ ', '');
        } else {
            btn.innerHTML = btn.innerHTML.replace('<i class="fas fa-check-circle me-2" style="color: var(--cor-success);"></i>', '');
        }
    });
    
    console.log(`🎨 Tema alterado para: ${temas[tema]}`);
}

function configurarSeletorTemas() {
    // Configurar botões de tema na navbar
    const themeBtns = document.querySelectorAll('.theme-btn');
    
    themeBtns.forEach(btn => {
        // Marcar tema ativo
        if (btn.dataset.theme === temaAtual) {
            btn.classList.add('active');
        }
        
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            aplicarTema(btn.dataset.theme);
            
            // Fechar dropdown após seleção
            const dropdown = bootstrap.Dropdown.getInstance(document.getElementById('themeDropdown'));
            if (dropdown) {
                dropdown.hide();
            }
        });
    });
}

// Remover função criarThemeSwitcher - não usaremos mais

// Funções utilitárias
function formatarNota(nota) {
    return parseFloat(nota).toFixed(1);
}

function formatarData(dataString) {
    const data = new Date(dataString);
    return data.toLocaleDateString('pt-BR');
}

function confirmarAcao(mensagem) {
    return confirm(mensagem);
}

// Efeitos visuais
function adicionarEfeitoHover() {
    // Adiciona efeito de hover em elementos específicos
    const elementos = document.querySelectorAll('.cyber-card, .cyber-table tbody tr');
    
    elementos.forEach(elemento => {
        elemento.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        elemento.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Animações de entrada
function animarElementos() {
    const elementos = document.querySelectorAll('.cyber-card, .stats-card');
    
    elementos.forEach((elemento, index) => {
        elemento.style.opacity = '0';
        elemento.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            elemento.style.transition = 'all 0.5s ease';
            elemento.style.opacity = '1';
            elemento.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Contador em tempo real
function iniciarContador() {
    const contadorElement = document.getElementById('contador-tempo');
    if (!contadorElement) return;
    
    function atualizarContador() {
        const agora = new Date();
        const dataAlvo = new Date('2025-11-24T23:59:59'); // 24 de novembro de 2025
        
        const diferenca = dataAlvo - agora;
        
        if (diferenca > 0) {
            const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
            const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
            const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);
            
            contadorElement.innerHTML = `
                <strong>TEMPO RESTANTE:</strong><br>
                <span style='color:var(--cor-accent); font-size:1.3em; text-shadow:0 0 15px var(--cor-accent); font-weight:900;'>
                    ${dias}D ${horas}H ${minutos}M ${segundos}S
                </span>`;
        } else {
            contadorElement.innerHTML = `<strong style='color:var(--cor-primary);'>PRAZO ACABOU!</strong>`;
        }
    }
    
    // Atualizar a cada segundo
    atualizarContador();
    setInterval(atualizarContador, 1000);
}

// Filtros e busca
function configurarFiltros() {
    const inputBusca = document.getElementById('busca-tabela');
    if (inputBusca) {
        inputBusca.addEventListener('input', function() {
            const termo = this.value.toLowerCase();
            const linhas = document.querySelectorAll('.cyber-table tbody tr');
            
            linhas.forEach(linha => {
                const texto = linha.textContent.toLowerCase();
                linha.style.display = texto.includes(termo) ? '' : 'none';
            });
        });
    }
}

// Tooltips dinâmicos
function configurarTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Confirmação para exclusões
function configurarConfirmacoes() {
    const botoesDeletar = document.querySelectorAll('a[href*="deletar"], button[name="deletar"]');
    
    botoesDeletar.forEach(botao => {
        botao.addEventListener('click', function(e) {
            const confirmacao = confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.');
            if (!confirmacao) {
                e.preventDefault();
            }
        });
    });
}

// Auto-hide para mensagens
function configurarAutoHideAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                alert.style.transition = 'all 0.5s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000); // 5 segundos
    });
}

// Loading states
function mostrarLoading(elemento) {
    elemento.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Carregando...';
    elemento.disabled = true;
}

function esconderLoading(elemento, textoOriginal) {
    elemento.innerHTML = textoOriginal;
    elemento.disabled = false;
}

// Formatação de campos numéricos
function configurarCamposNumericos() {
    const camposNota = document.querySelectorAll('input[type="number"][name*="nota"], input[type="number"][name*="valor"]');
    
    camposNota.forEach(campo => {
        campo.addEventListener('input', function() {
            let valor = parseFloat(this.value);
            const max = parseFloat(this.max) || 10;
            
            if (valor > max) {
                this.value = max;
            }
            if (valor < 0) {
                this.value = 0;
            }
        });
    });
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎮 Sistema de Gamificação Escolar carregado!');
    
    // Aplicar tema salvo
    aplicarTema(temaAtual);
    
    // Configurar seletor de temas na navbar
    configurarSeletorTemas();
    
    // Configurar funcionalidades
    adicionarEfeitoHover();
    animarElementos();
    iniciarContador();
    configurarFiltros();
    configurarTooltips();
    configurarConfirmacoes();
    configurarAutoHideAlerts();
    configurarCamposNumericos();
    
    // Log do tema atual
    console.log(`🎨 Tema ativo: ${temas[temaAtual]}`);
});

// Funções globais para usar nos templates
window.GameSystem = {
    formatarNota,
    formatarData,
    confirmarAcao,
    aplicarTema,
    mostrarLoading,
    esconderLoading
};
