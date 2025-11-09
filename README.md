# 📄 Currículo IA

Aplicação web inteligente que otimiza currículos automaticamente usando Inteligência Artificial (Gemini + Perplexity).

## 🎯 Funcionalidades

- **Análise Inteligente**: Extrai palavras-chave e informações essenciais da descrição da vaga
- **Pesquisa de Cultura**: Investiga a cultura e valores da empresa usando Perplexity AI
- **Otimização Personalizada**: Gera um currículo otimizado alinhado com a vaga e cultura da empresa
- **Interface Moderna**: Design profissional com tema dark e experiência de usuário fluida
- **Retry Automático**: Lógica inteligente de retry para lidar com limites de taxa das APIs

## 🏗️ Arquitetura

```
curriculo-ia/
├── app.py                 # Backend Flask + Pipeline de IA
├── templates/
│   └── index.html         # Interface do usuário
├── static/
│   ├── styles.css         # Estilos (tema dark)
│   └── script.js          # Lógica frontend
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Chave de API do Google Gemini
- Chave de API do Perplexity AI

### Passo 1: Clone o Repositório

```bash
git clone <url-do-repositorio>
cd pipeline-resu
```

### Passo 2: Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instale as Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configure as Chaves de API

1. Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

2. Edite o arquivo `.env` e adicione suas chaves:
```
GEMINI_API_KEY=sua_chave_gemini_aqui
PERPLEXITY_API_KEY=sua_chave_perplexity_aqui
```

#### Como Obter as Chaves de API

**Google Gemini:**
1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login com sua conta Google
3. Clique em "Create API Key"
4. Copie a chave gerada

**Perplexity AI:**
1. Acesse: https://www.perplexity.ai/settings/api
2. Crie uma conta ou faça login
3. Gere uma nova API key
4. Copie a chave gerada

## 💻 Uso

### Iniciar o Servidor

```bash
python app.py
```

O servidor estará disponível em: **http://localhost:5000**

### Usando a Aplicação

1. Abra seu navegador e acesse `http://localhost:5000`
2. Cole a **descrição completa da vaga** no primeiro campo
3. Cole seu **currículo base** no segundo campo
4. Clique em **"Otimizar Currículo Agora"**
5. Aguarde o processamento (pode levar alguns minutos)
6. Visualize e copie seu currículo otimizado

## 🔄 Pipeline de Processamento

A aplicação executa 3 etapas sequenciais:

### Etapa 1: Análise da Vaga (Gemini)
- Extrai o nome da empresa
- Identifica palavras-chave e habilidades importantes
- Retorno em formato JSON estruturado
- **Retry automático** em caso de rate limit (60s de espera)

### Etapa 2: Pesquisa de Cultura (Perplexity)
- Pesquisa informações sobre a empresa
- Identifica cultura organizacional e valores
- Fornece contexto para personalização

### Etapa 3: Síntese Final (Gemini)
- Combina todos os dados coletados
- Gera currículo otimizado e personalizado
- Mantém informações verdadeiras do currículo original
- **Retry automático** em caso de rate limit (60s de espera)

## 🛡️ Segurança

- As chaves de API são carregadas de variáveis de ambiente
- O arquivo `.env` está no `.gitignore` para evitar vazamento de credenciais
- Dados não são armazenados no servidor
- Comunicação segura entre frontend e backend

## 🎨 Tecnologias Utilizadas

**Backend:**
- Flask (framework web)
- Google Generative AI (Gemini)
- OpenAI SDK (Perplexity)
- python-dotenv (variáveis de ambiente)

**Frontend:**
- HTML5
- CSS3 (design responsivo + tema dark)
- JavaScript Vanilla (sem frameworks)

## 📝 Notas Importantes

- **Custos**: Ambas as APIs (Gemini e Perplexity) têm limites gratuitos, mas podem gerar custos dependendo do uso
- **Rate Limits**: A aplicação implementa retry automático, mas respeite os limites das APIs
- **Privacidade**: Seus dados são enviados para as APIs de terceiros (Gemini e Perplexity)
- **Tempo de Processamento**: O pipeline completo pode levar de 30 segundos a alguns minutos

## 🐛 Troubleshooting

### Erro: "As chaves de API devem estar configuradas"
- Verifique se o arquivo `.env` existe e contém as chaves corretas

### Erro: Rate Limit
- A aplicação tentará novamente automaticamente após 60 segundos
- Se persistir, aguarde alguns minutos antes de tentar novamente

### Erro de Conexão
- Verifique sua conexão com a internet
- Confirme se as chaves de API são válidas

## 📄 Licença

Este projeto é fornecido como está, para fins educacionais e de demonstração.

## 👨‍💻 Desenvolvido por

Engenheiro de Software Sênior Full-Stack

---

**Nota**: Nunca compartilhe suas chaves de API publicamente. Mantenha o arquivo `.env` sempre no `.gitignore`.
