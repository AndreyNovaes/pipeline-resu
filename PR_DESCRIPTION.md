## Resumo
Atualiza as versões das dependências Python para resolver erro de compatibilidade no cliente OpenAI.

## Problema
Ao executar `python3 app.py`, ocorria o seguinte erro:
```
TypeError: Client.__init__() got an unexpected keyword argument 'proxies'
```

## Solução
Atualizadas as versões das bibliotecas no `requirements.txt`:

| Biblioteca | Versão Anterior | Nova Versão |
|------------|----------------|-------------|
| Flask | 3.0.0 | **3.0.3** |
| google-generativeai | 0.3.2 | **0.8.3** |
| openai | 1.6.1 | **1.54.0** ⭐ |
| python-dotenv | 1.0.0 | **1.0.1** |
| httpx | - | **0.27.2** (nova) |

A principal correção está na biblioteca `openai`, que teve mudanças significativas na API do cliente entre a versão 1.6.1 e 1.54.0.

## Mudanças
- ✅ Atualizado `requirements.txt` com versões compatíveis
- ✅ Adicionada dependência `httpx` para melhor compatibilidade
- ✅ Testado localmente para garantir funcionamento

## Tipo de Mudança
- [x] Bug fix (mudança que corrige um problema)
- [ ] Nova funcionalidade
- [ ] Breaking change

## Como Testar
```bash
# Desinstalar dependências antigas
pip uninstall -y Flask google-generativeai openai python-dotenv httpx

# Reinstalar com versões corretas
pip install -r requirements.txt

# Executar aplicação
python3 app.py
```

A aplicação deve iniciar sem erros em `http://localhost:5000`
