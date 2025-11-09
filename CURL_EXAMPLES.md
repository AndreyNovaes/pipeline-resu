# Exemplos de Requisições cURL para Currículo IA

## 1. Teste Simples (Vaga e Currículo Curtos)

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Vaga: Desenvolvedor Python Sênior na TechCorp. Requisitos: Python, Flask, APIs REST, 5+ anos de experiência. Conhecimento em cloud (AWS/GCP).",
    "base_cv": "João Silva - Desenvolvedor Python com 6 anos de experiência. Especializado em Flask, Django, FastAPI. Experiência com AWS, Docker, PostgreSQL. Projetos em e-commerce e fintech."
  }'
```

## 2. Teste Completo (Vaga e Currículo Reais)

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Desenvolvedor Full-Stack Sênior - Google\n\nRequisitos:\n- 5+ anos de experiência em desenvolvimento web\n- Expertise em Python, JavaScript/TypeScript\n- Experiência com frameworks modernos (React, Vue, Angular)\n- Conhecimento em arquitetura de microsserviços\n- Experiência com cloud (GCP preferencial)\n- Inglês fluente\n\nResponsabilidades:\n- Desenvolver e manter aplicações web escaláveis\n- Colaborar com equipes multidisciplinares\n- Code review e mentoria de desenvolvedores júnior\n- Implementar melhores práticas de desenvolvimento",
    "base_cv": "JOÃO SILVA\nDesenvolvedor Full-Stack\n\nEXPERIÊNCIA:\n\nEmpresa XYZ (2020-2025)\n- Desenvolvedor Sênior Python/JavaScript\n- Criação de APIs REST com Flask e FastAPI\n- Frontend com React e TypeScript\n- Deploy em AWS com Docker e Kubernetes\n- Liderança técnica de equipe de 5 desenvolvedores\n\nEmpresa ABC (2017-2020)\n- Desenvolvedor Python Pleno\n- Desenvolvimento de sistemas web com Django\n- Integração com bancos de dados PostgreSQL e MongoDB\n- Testes automatizados com Pytest\n\nFORMAÇÃO:\nBacharelado em Ciência da Computação - USP (2017)\n\nHABILIDADES:\nPython, JavaScript, TypeScript, React, Flask, Django, FastAPI, PostgreSQL, MongoDB, Docker, Kubernetes, AWS, Git"
  }'
```

## 3. Teste com Arquivo JSON

Crie um arquivo `test-request.json`:

```json
{
  "job_description": "Vaga: Desenvolvedor Backend Python na Nubank\n\nResponsabilidades:\n- Desenvolver e manter microsserviços em Python\n- Trabalhar com Kafka, Redis e PostgreSQL\n- Implementar testes automatizados\n- Participar de code reviews\n\nRequisitos:\n- 3+ anos com Python\n- Experiência com arquitetura de microsserviços\n- Conhecimento em filas de mensagens\n- Familiaridade com práticas DevOps",
  "base_cv": "Maria Santos\nEngenheira de Software Backend\n\nExperiência:\n- 4 anos com Python (Flask, Django, FastAPI)\n- Arquitetura de microsserviços\n- Message brokers: RabbitMQ, Kafka\n- Bancos: PostgreSQL, Redis, MongoDB\n- CI/CD: Jenkins, GitLab CI\n- Cloud: AWS (EC2, S3, Lambda)\n\nProjetos recentes:\n- Sistema de pagamentos distribuído\n- API de alta performance (1M+ req/dia)\n- Pipeline de dados em tempo real"
}
```

Depois execute:

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d @test-request.json
```

## 4. Teste com Verbose (Ver Headers e Status)

```bash
curl -v -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Cientista de Dados - Meta. Requisitos: Python, ML, TensorFlow, PyTorch. Experiência com NLP e Computer Vision.",
    "base_cv": "Ana Costa - Data Scientist. 5 anos de experiência. Python, scikit-learn, TensorFlow, PyTorch. Projetos em NLP (chatbots, sentiment analysis) e CV (object detection)."
  }'
```

## 5. Teste Salvando Resultado em Arquivo

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "DevOps Engineer - Amazon. Kubernetes, Terraform, AWS, CI/CD pipelines.",
    "base_cv": "Carlos Lima - DevOps. 3 anos. Docker, Kubernetes, Terraform, AWS (ECS, EKS, Lambda). Jenkins, GitHub Actions."
  }' \
  -o resultado.json

# Ver resultado formatado
cat resultado.json | python3 -m json.tool
```

## 6. Teste de Erro (Campos Vazios)

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "",
    "base_cv": ""
  }'
```

Resposta esperada:
```json
{
  "error": "Descrição da vaga e currículo base são obrigatórios"
}
```

## 7. Teste GET na Rota Principal

```bash
curl http://localhost:5000/
```

Deve retornar o HTML da página.

## 8. Teste com Timeout (Para Requisições Longas)

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  --max-time 300 \
  -d @test-request.json
```

## 9. Teste com Proxy (Se Necessário)

```bash
curl -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -x http://seu-proxy:porta \
  -d @test-request.json
```

## 10. Script de Teste Bash Completo

Crie um arquivo `test.sh`:

```bash
#!/bin/bash

echo "===================================="
echo "Testando API Currículo IA"
echo "===================================="

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Teste 1: Verificar se servidor está rodando
echo -e "\n${GREEN}[1/3] Verificando servidor...${NC}"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/)
if [ $STATUS -eq 200 ]; then
  echo "✓ Servidor está rodando"
else
  echo -e "${RED}✗ Servidor não está respondendo${NC}"
  exit 1
fi

# Teste 2: Requisição simples
echo -e "\n${GREEN}[2/3] Testando requisição simples...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Desenvolvedor Python - TechCorp",
    "base_cv": "João Silva - Dev Python com 5 anos de experiência"
  }')

if echo "$RESPONSE" | grep -q "error"; then
  echo -e "${RED}✗ Erro na requisição:${NC}"
  echo "$RESPONSE" | python3 -m json.tool
else
  echo "✓ Requisição processada com sucesso"
  echo "Primeiros 200 caracteres:"
  echo "$RESPONSE" | python3 -m json.tool | head -n 10
fi

# Teste 3: Teste de validação
echo -e "\n${GREEN}[3/3] Testando validação (campos vazios)...${NC}"
ERROR_RESPONSE=$(curl -s -X POST http://localhost:5000/processar-curriculo \
  -H "Content-Type: application/json" \
  -d '{"job_description": "", "base_cv": ""}')

if echo "$ERROR_RESPONSE" | grep -q "obrigatórios"; then
  echo "✓ Validação funcionando corretamente"
else
  echo -e "${RED}✗ Validação não está funcionando${NC}"
fi

echo -e "\n===================================="
echo "Testes concluídos!"
echo "===================================="
```

Execute:

```bash
chmod +x test.sh
./test.sh
```

---

## Notas Importantes:

1. **Timeout**: O processamento pode demorar 2-5 minutos devido ao pipeline de 3 etapas
2. **Rate Limit**: Se encontrar rate limit, o sistema automaticamente aguarda 60s e tenta novamente
3. **Formato da Resposta**: A resposta sempre será JSON com `optimized_cv` ou `error`
4. **Encoding**: Use UTF-8 para caracteres especiais em português

## Estrutura da Resposta de Sucesso:

```json
{
  "optimized_cv": "Texto completo do currículo otimizado...",
  "company_name": "Nome da Empresa",
  "keywords_count": 15
}
```

## Estrutura da Resposta de Erro:

```json
{
  "error": "Mensagem de erro detalhada"
}
```
