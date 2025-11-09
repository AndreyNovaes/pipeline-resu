"""
Currículo IA - Backend Flask
Aplicação para otimização de currículos usando IA (Gemini + Perplexity)
"""

from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from openai import OpenAI
import os
import time
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurar APIs
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

if not GEMINI_API_KEY or not PERPLEXITY_API_KEY:
    raise ValueError("As chaves de API devem estar configuradas no arquivo .env")

genai.configure(api_key=GEMINI_API_KEY)

# Configurar cliente Perplexity
perplexity_client = OpenAI(
    api_key=PERPLEXITY_API_KEY,
    base_url="https://api.perplexity.ai"
)


def call_gemini_with_retry(prompt, max_retries=2):
    """
    Chama a API Gemini com lógica de retry para lidar com rate limits.

    Args:
        prompt (str): O prompt a ser enviado para o Gemini
        max_retries (int): Número máximo de tentativas adicionais (padrão: 2)

    Returns:
        str: Resposta do modelo Gemini

    Raises:
        Exception: Se todas as tentativas falharem
    """
    # Usar modelo atualizado do Gemini (gemini-1.5-flash é mais rápido e econômico)
    model = genai.GenerativeModel('gemini-1.5-flash')
    attempts = 0

    while attempts <= max_retries:
        try:
            # Configuração de geração para respostas mais previsíveis
            generation_config = {
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 8192,
            }

            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Verificar se a resposta tem conteúdo
            if not response.text:
                raise Exception("Resposta vazia do Gemini")

            return response.text

        except Exception as e:
            error_message = str(e).lower()
            print(f"Erro na tentativa {attempts + 1}: {error_message}")

            # Verificar se é um erro de rate limit ou quota
            if 'rate' in error_message or 'quota' in error_message or 'limit' in error_message or 'resource' in error_message:
                attempts += 1
                if attempts <= max_retries:
                    print(f"Rate limit/quota atingido. Aguardando 60 segundos antes da tentativa {attempts + 1}/{max_retries + 1}...")
                    time.sleep(60)
                else:
                    raise Exception(f"Falha após {max_retries + 1} tentativas devido a rate limit/quota")
            else:
                # Se não for rate limit, lançar o erro imediatamente
                raise Exception(f"Erro ao chamar Gemini: {str(e)}")

    raise Exception("Número máximo de tentativas excedido")


def call_perplexity(prompt):
    """
    Chama a API Perplexity para pesquisa de cultura empresarial.

    Args:
        prompt (str): O prompt de pesquisa

    Returns:
        str: Resposta do modelo Perplexity

    Raises:
        Exception: Se a chamada falhar
    """
    try:
        messages = [
            {
                "role": "system",
                "content": "Você é um assistente de pesquisa especializado em cultura organizacional e empresas."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = perplexity_client.chat.completions.create(
            model="llama-3.1-sonar-small-128k-online",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        raise Exception(f"Erro ao chamar Perplexity: {str(e)}")


@app.route('/')
def index():
    """Renderiza a página principal"""
    return render_template('index.html')


@app.route('/processar-curriculo', methods=['POST'])
def processar_curriculo():
    """
    Endpoint principal que processa o currículo através do pipeline de 3 etapas:
    1. Gemini: Extrai informações da vaga (company_name, keywords)
    2. Perplexity: Pesquisa cultura da empresa
    3. Gemini: Gera currículo otimizado final
    """
    try:
        # Receber dados do frontend
        data = request.get_json()
        job_description = data.get('job_description', '').strip()
        base_cv = data.get('base_cv', '').strip()

        # Validar entrada
        if not job_description or not base_cv:
            return jsonify({'error': 'Descrição da vaga e currículo base são obrigatórios'}), 400

        print("=== INICIANDO PIPELINE ===")

        # ============================================================
        # PASSO 1: GEMINI - Análise Inicial da Vaga
        # ============================================================
        print("Passo 1/3: Analisando descrição da vaga com Gemini...")

        prompt_1 = f"""Analise a seguinte descrição de vaga e extraia as informações em formato JSON:

DESCRIÇÃO DA VAGA:
{job_description}

Por favor, retorne APENAS um objeto JSON válido com esta estrutura exata:
{{
  "company_name": "nome da empresa (ou 'Empresa não identificada' se não estiver clara)",
  "keywords": ["lista", "de", "palavras-chave", "e", "habilidades", "importantes"]
}}

Não inclua nenhum texto adicional, apenas o JSON."""

        try:
            response_1 = call_gemini_with_retry(prompt_1)

            # Extrair JSON da resposta
            # Remover possíveis marcadores de código markdown
            response_1_clean = response_1.strip()
            if response_1_clean.startswith('```'):
                # Remover blocos de código markdown
                lines = response_1_clean.split('\n')
                response_1_clean = '\n'.join([l for l in lines if not l.startswith('```')])
                response_1_clean = response_1_clean.strip()

            analysis_data = json.loads(response_1_clean)
            company_name = analysis_data.get('company_name', 'Empresa não identificada')
            keywords = analysis_data.get('keywords', [])

            print(f"  ✓ Empresa identificada: {company_name}")
            print(f"  ✓ Keywords extraídas: {len(keywords)} palavras-chave")

        except json.JSONDecodeError as e:
            return jsonify({'error': f'Erro ao processar resposta do Gemini (Passo 1). Resposta inválida: {str(e)}'}), 500
        except Exception as e:
            return jsonify({'error': f'Erro no Passo 1 (Análise Inicial): {str(e)}'}), 500

        # ============================================================
        # PASSO 2: PERPLEXITY - Pesquisa de Cultura Empresarial
        # ============================================================
        print("Passo 2/3: Pesquisando cultura da empresa com Perplexity...")

        prompt_2 = f"""Pesquise e forneça informações detalhadas sobre a cultura, valores e ambiente de trabalho da empresa "{company_name}".

Inclua:
- Missão e valores da empresa
- Cultura organizacional
- Ambiente de trabalho
- Benefícios típicos
- Estilo de gestão
- Qualquer informação relevante para um candidato

Se a empresa não for conhecida ou você não encontrar informações suficientes, indique isso claramente."""

        try:
            culture_report = call_perplexity(prompt_2)
            print(f"  ✓ Relatório de cultura obtido ({len(culture_report)} caracteres)")

        except Exception as e:
            return jsonify({'error': f'Erro no Passo 2 (Pesquisa de Cultura): {str(e)}'}), 500

        # ============================================================
        # PASSO 3: GEMINI - Síntese Final do Currículo Otimizado
        # ============================================================
        print("Passo 3/3: Gerando currículo otimizado com Gemini...")

        prompt_3 = f"""Você é um especialista em otimização de currículos. Com base nas informações fornecidas, crie uma versão otimizada do currículo que se alinhe perfeitamente com a vaga.

DESCRIÇÃO DA VAGA:
{job_description}

CURRÍCULO BASE DO CANDIDATO:
{base_cv}

INFORMAÇÕES SOBRE A CULTURA DA EMPRESA:
{culture_report}

INSTRUÇÕES:
1. Mantenha todas as informações verdadeiras do currículo original
2. Reorganize e reformule as experiências para destacar as habilidades mais relevantes para esta vaga
3. Use palavras-chave da descrição da vaga de forma natural
4. Adapte o tom e estilo para se alinhar com a cultura da empresa
5. Destaque conquistas quantificáveis quando possível
6. Mantenha um formato profissional e fácil de ler
7. NÃO invente experiências ou habilidades que não existam no currículo original

Por favor, retorne o currículo otimizado completo em texto formatado."""

        try:
            optimized_cv = call_gemini_with_retry(prompt_3)
            print("  ✓ Currículo otimizado gerado com sucesso!")

        except Exception as e:
            return jsonify({'error': f'Erro no Passo 3 (Síntese Final): {str(e)}'}), 500

        print("=== PIPELINE CONCLUÍDO COM SUCESSO ===")

        # Retornar resultado
        return jsonify({
            'optimized_cv': optimized_cv,
            'company_name': company_name,
            'keywords_count': len(keywords)
        }), 200

    except Exception as e:
        print(f"Erro geral: {str(e)}")
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500


if __name__ == '__main__':
    # Executar em modo debug apenas em desenvolvimento
    app.run(debug=True, host='0.0.0.0', port=5000)
