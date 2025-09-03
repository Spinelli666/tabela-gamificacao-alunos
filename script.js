// Lista de alunos e notas
const alunos = [
    { nome: 'Ana Clara Sousa De Moura', nota: 0.0 },
    { nome: 'Ana Luiza Ramos De Jesus Pinto', nota: 0.0 },
    { nome: 'Bryan Marcello Da Silva De Sá', nota: 0.0 },
    { nome: 'Crislayne Yasmim Gomes De Paula Leite', nota: 0.0 },
    { nome: 'Cristiano Henrique Costa Maia', nota: 0.0 },
    { nome: 'Danyel Nicollas Alves De Assis', nota: 0.0 },
    { nome: 'Kerolaine Cristini Oliveira Da Silva', nota: 0.0 },
    { nome: 'Manuela Palhano Jesus', nota: 0.0 },
    { nome: 'Maria Luiza Pinheiro Orgelio', nota: 0.0 },
    { nome: 'Matheus Christiano De Assunção Marotta', nota: 0.0 },
    { nome: 'Matheus Vitoria Mendes', nota: 0.0 },
    { nome: 'Miguel Mucury Dos Santos', nota: 0.0 },
    { nome: 'Nicolas Guilherme Gomes Nicácio Cardos', nota: 0.0 },
    { nome: 'Rubia Melyssa Carvalho Dos Santos', nota: 0.0 },
    { nome: 'Tailane Lime De Souza Barreto', nota: 0.0 },
    { nome: 'Thaisa Vitoria Da Silva Santos', nota: 0.0 },
    { nome: 'Thauana Abraão Da Silva Medeiros', nota: 0.0 },
    { nome: 'Thiago Dos Santos Gonçalves Rocha', nota: 0.0 }
];

// Temas disponíveis
const temas = {
    hotline: {
        nome: 'Hotline Miami',
        cores: {
            primary: '#ff006e',
            secondary: '#00f5ff', 
            accent: '#ffff00',
            bg: '#0a0a0a'
        }
    },
    cyberpunk: {
        nome: 'Cyberpunk 2077',
        cores: {
            primary: '#00ff41',
            secondary: '#ff0080',
            accent: '#ffff00',
            bg: '#0d0208'
        }
    },
    synthwave: {
        nome: 'Synthwave',
        cores: {
            primary: '#ff00ff',
            secondary: '#00ffff',
            accent: '#ff6600',
            bg: '#1a0033'
        }
    }
};

let temaAtual = 'hotline';

function renderTabela() {
    const tbody = document.querySelector('#tabela-alunos tbody');
    tbody.innerHTML = '';
    
    // Atualiza data atual e contador
    atualizarDataEContador();
    
    // Ordena alunos por nota decrescente
    const alunosOrdenados = [...alunos].sort((a, b) => b.nota - a.nota);
    // Calcula colocações (empate para notas iguais)
    let colocacao = 1;
    let ultimaNota = null;
    let posicaoReal = 1;
    const colocacoes = [];
    alunosOrdenados.forEach((aluno, idx) => {
        if (aluno.nota !== ultimaNota) {
            colocacao = posicaoReal;
        }
        colocacoes.push({ ...aluno, colocacao });
        ultimaNota = aluno.nota;
        posicaoReal++;
    });
    // Exibe na ordem de notas decrescente
    const alunosComColocacao = alunosOrdenados.map(aluno => {
        const encontrado = colocacoes.find(a => a.nome === aluno.nome && a.nota === aluno.nota);
        if (encontrado) {
            colocacoes.splice(colocacoes.indexOf(encontrado), 1);
            return { ...aluno, colocacao: encontrado.colocacao };
        }
        return aluno;
    });
    // Adiciona todos os alunos com o mesmo estilo
    alunosComColocacao.forEach(aluno => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${aluno.colocacao}º</td>
            <td>${aluno.nome}</td>
            <td>${aluno.nota}</td>
        `;
        tbody.appendChild(tr);
    });
    // Gamificação: média das notas
    const notas = alunos.map(a => a.nota);
    const media = (notas.reduce((acc, n) => acc + n, 0) / notas.length).toFixed(2);
    document.getElementById('gamificacao').innerHTML =
        `<strong>SCORE MÉDIO:</strong> <span style='color:var(--cor-primary); font-size:1.4em; text-shadow:0 0 15px var(--cor-primary); font-weight:900;'>${media}</span>`;
}

function atualizarDataEContador() {
    const agora = new Date();
    const dataAlvo = new Date(2025, 10, 24); // 24 de novembro de 2025 (mês 10 = novembro)
    
    // Formatar data atual
    const dataAtual = agora.toLocaleDateString('pt-BR', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    
    // Calcular diferença
    const diferenca = dataAlvo - agora;
    
    if (diferenca > 0) {
        const dias = Math.floor(diferenca / (1000 * 60 * 60 * 24));
        const horas = Math.floor((diferenca % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutos = Math.floor((diferenca % (1000 * 60 * 60)) / (1000 * 60));
        const segundos = Math.floor((diferenca % (1000 * 60)) / 1000);
        
        document.getElementById('data-atual').innerHTML = 
            `<strong>DATA ATUAL:</strong> ${dataAtual.toUpperCase()}`;
            
        document.getElementById('contador').innerHTML = 
            `<strong>TEMPO RESTANTE:</strong><br>
             <span style='color:var(--cor-accent); font-size:1.3em; text-shadow:0 0 15px var(--cor-accent); font-weight:900;'>
                ${dias}D ${horas}H ${minutos}M ${segundos}S
             </span>`;
    } else {
        document.getElementById('data-atual').innerHTML = 
            `<strong>DATA ATUAL:</strong> ${dataAtual.toUpperCase()}`;
            
        document.getElementById('contador').innerHTML = 
            `<strong style='color:var(--cor-primary);'>PRAZO ACABOU!</strong>`;
    }
}

// Atualizar contador a cada segundo
setInterval(atualizarDataEContador, 1000);

// Função para alternar tema
function alternarTema() {
    const temaKeys = Object.keys(temas);
    const currentIndex = temaKeys.indexOf(temaAtual);
    const nextIndex = (currentIndex + 1) % temaKeys.length;
    temaAtual = temaKeys[nextIndex];
    
    aplicarTema(temaAtual);
    
    // Feedback visual
    const btn = document.getElementById('btn-tema');
    btn.textContent = `🎨 TEMA: ${temas[temaAtual].nome.toUpperCase()}`;
    setTimeout(() => {
        btn.textContent = '🎨 ALTERNAR TEMA';
    }, 2000);
}

// Função para aplicar tema
function aplicarTema(tema) {
    // Remove classes de tema anteriores
    document.body.classList.remove('tema-cyberpunk', 'tema-synthwave');
    
    // Aplica nova classe de tema
    if (tema === 'cyberpunk') {
        document.body.classList.add('tema-cyberpunk');
    } else if (tema === 'synthwave') {
        document.body.classList.add('tema-synthwave');
    }
    // tema 'hotline' usa as variáveis CSS padrão do :root
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Botão tema
    document.getElementById('btn-tema').addEventListener('click', alternarTema);
    
    // Aplicar tema inicial
    aplicarTema(temaAtual);
});

renderTabela();
