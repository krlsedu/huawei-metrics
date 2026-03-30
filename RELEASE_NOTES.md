Aqui está o Release Notes técnico para a versão **v26.14.006**, focado em melhorias de infraestrutura e configurabilidade do monitoramento.

---

# Release Notes - v26.14.006

## Resumo
Esta versão foca na refatoração do sistema de monitoramento em background, removendo valores fixos (*hardcoded*) e permitindo maior flexibilidade operacional através de variáveis de ambiente.

---

## 🚀 Features

- **Configurabilidade de Intervalo de Monitoramento:** Implementada a capacidade de definir a duração do *sleep* no monitoramento via variável de ambiente `TIME_SLEEP`. Isso permite ajustes dinâmicos de performance sem necessidade de alteração no código-fonte.
- **Injeção de Dependência de Configuração:** A função `monitorar_huawei_background` agora recebe explicitamente os parâmetros de tempo, melhorando a testabilidade e o controle do fluxo de execução.

## 🐛 Fixes

- **Validação de Inicialização:** Adicionada verificação condicional para a existência da variável `TIME_SLEEP` antes do disparo da thread de background, prevenindo erros de execução ou loops inesperados caso a configuração esteja ausente.

## 🔧 Chore

- Refatoração do arquivo `app.py` para substituição de valores estáticos por variáveis dinâmicas.

---

### Detalhes Técnicos
- **Commit Principal:** `e0a78d3`
- **Arquivos Alterados:** `app.py`
- **Autor:** Carlos Eduardo Duarte Schwalm