Aqui está o Release Notes técnico para a versão **v26.14.007**, focado em estabilidade e correção de tipos no ambiente de execução.

---

# 📝 Release Notes - v26.14.007

## Resumo
Esta versão foca na correção de um erro de tipagem na inicialização de threads, garantindo que as configurações de ambiente sejam interpretadas corretamente pelo runtime do Python.

---

## 🐛 Fixes

- **Tratamento de Variáveis de Ambiente (`app.py`):**
    - Corrigido bug onde a variável `TIME_SLEEP` era lida como *string* (padrão do OS), causando falhas na criação de threads.
    - Implementada a conversão explícita para `integer` antes do uso, garantindo a compatibilidade com as funções de temporização do sistema.

## 🔧 Chore

- **Refatoração de Código:** Pequeno ajuste técnico no arquivo principal para aumentar a resiliência do carregamento de configurações.

---

### 🛠 Detalhes Técnicos
- **Commit:** `47c5ec2`
- **Arquivos alterados:** `app.py` (+1 linha)
- **Autor:** Carlos Eduardo Duarte Schwalm