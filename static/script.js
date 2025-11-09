/**
 * CURRÍCULO IA - Script Frontend
 * Gerencia a interação do usuário e comunicação com o backend
 */

// ============================================================
// Elementos do DOM
// ============================================================
const form = document.getElementById('curriculo-form');
const submitBtn = document.getElementById('submit-btn');
const jobDescriptionInput = document.getElementById('job-description');
const baseCvInput = document.getElementById('base-cv');

const loadingContainer = document.getElementById('loading');
const resultContainer = document.getElementById('result-container');
const errorContainer = document.getElementById('error-container');

const resultText = document.getElementById('result-text');
const errorMessage = document.getElementById('error-message');

const copyBtn = document.getElementById('copy-btn');
const retryBtn = document.getElementById('retry-btn');

// ============================================================
// Event Listeners
// ============================================================

/**
 * Evento de submissão do formulário
 */
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    await processarCurriculo();
});

/**
 * Evento para copiar resultado para área de transferência
 */
copyBtn.addEventListener('click', () => {
    const text = resultText.textContent;

    navigator.clipboard.writeText(text).then(() => {
        // Feedback visual
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copiado!';
        copyBtn.style.background = 'var(--accent-success)';

        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    }).catch(err => {
        alert('Erro ao copiar texto: ' + err);
    });
});

/**
 * Evento para tentar novamente após erro
 */
retryBtn.addEventListener('click', () => {
    esconderMensagens();
    // Scroll suave para o topo do formulário
    form.scrollIntoView({ behavior: 'smooth', block: 'start' });
});

// ============================================================
// Funções Principais
// ============================================================

/**
 * Processa o currículo enviando dados para o backend
 */
async function processarCurriculo() {
    // Obter valores dos campos
    const jobDescription = jobDescriptionInput.value.trim();
    const baseCv = baseCvInput.value.trim();

    // Validação básica
    if (!jobDescription || !baseCv) {
        mostrarErro('Por favor, preencha todos os campos obrigatórios.');
        return;
    }

    // Preparar UI para processamento
    esconderMensagens();
    mostrarLoading();
    desabilitarFormulario();

    try {
        // Fazer requisição POST para o backend
        const response = await fetch('/processar-curriculo', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                job_description: jobDescription,
                base_cv: baseCv
            })
        });

        // Processar resposta
        const data = await response.json();

        if (response.ok) {
            // Sucesso - mostrar currículo otimizado
            mostrarResultado(data.optimized_cv);
        } else {
            // Erro retornado pelo backend
            mostrarErro(data.error || 'Erro desconhecido ao processar o currículo.');
        }

    } catch (error) {
        // Erro de rede ou outro erro do cliente
        console.error('Erro na requisição:', error);
        mostrarErro(
            'Erro de conexão com o servidor. Verifique sua conexão com a internet e tente novamente.'
        );
    } finally {
        // Sempre ocultar loading e reabilitar formulário
        esconderLoading();
        habilitarFormulario();
    }
}

// ============================================================
// Funções de UI/UX
// ============================================================

/**
 * Mostra o indicador de loading
 */
function mostrarLoading() {
    loadingContainer.classList.remove('hidden');
}

/**
 * Esconde o indicador de loading
 */
function esconderLoading() {
    loadingContainer.classList.add('hidden');
}

/**
 * Mostra o resultado do currículo otimizado
 * @param {string} curriculo - Texto do currículo otimizado
 */
function mostrarResultado(curriculo) {
    resultText.textContent = curriculo;
    resultContainer.classList.remove('hidden');

    // Scroll suave para o resultado
    setTimeout(() => {
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Mostra uma mensagem de erro
 * @param {string} mensagem - Mensagem de erro a ser exibida
 */
function mostrarErro(mensagem) {
    errorMessage.textContent = mensagem;
    errorContainer.classList.remove('hidden');

    // Scroll suave para o erro
    setTimeout(() => {
        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

/**
 * Esconde todas as mensagens (resultado e erro)
 */
function esconderMensagens() {
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');
}

/**
 * Desabilita o formulário durante o processamento
 */
function desabilitarFormulario() {
    submitBtn.disabled = true;
    jobDescriptionInput.disabled = true;
    baseCvInput.disabled = true;
    submitBtn.style.opacity = '0.6';
    submitBtn.style.cursor = 'not-allowed';
}

/**
 * Reabilita o formulário após o processamento
 */
function habilitarFormulario() {
    submitBtn.disabled = false;
    jobDescriptionInput.disabled = false;
    baseCvInput.disabled = false;
    submitBtn.style.opacity = '';
    submitBtn.style.cursor = '';
}

// ============================================================
// Inicialização
// ============================================================

/**
 * Função executada quando a página carrega
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Currículo IA - Aplicação carregada com sucesso!');

    // Focar no primeiro campo
    jobDescriptionInput.focus();

    // Adicionar auto-resize nos textareas (opcional)
    autoResizeTextarea(jobDescriptionInput);
    autoResizeTextarea(baseCvInput);
});

/**
 * Ajusta automaticamente a altura do textarea conforme o usuário digita
 * @param {HTMLTextAreaElement} textarea - Elemento textarea
 */
function autoResizeTextarea(textarea) {
    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    });
}
