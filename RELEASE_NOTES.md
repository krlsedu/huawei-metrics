Com base na análise do commit `b92bd51` e no diff dos arquivos, aqui está o Release Notes técnico para a versão **v26.14.002**.

---

# 📦 Release Notes - v26.14.002

## Resumo Técnico
Esta versão foca na robustez da coleta de métricas e na atualização da infraestrutura de containers. Houve uma refatoração significativa no serviço de telemetria para melhorar a performance e a confiabilidade dos dados coletados.

---

## 🚀 Features

### Refatoração do Serviço de Métricas (`services/Metrics.py`)
*   **Otimização de Coleta:** Implementação de lógica aprimorada para processamento de dados (73 inserções vs 41 deleções), visando maior precisão na extração de indicadores de performance.
*   **Melhoria na Estrutura de Dados:** Reestruturação interna do serviço para facilitar a escalabilidade de novos endpoints de monitoramento.

---

## 🐛 Fixes

### Estabilidade da Aplicação (`app.py`)
*   Ajustes pontuais na inicialização do core da aplicação para garantir compatibilidade com as novas definições do serviço de métricas.

---

## 🔧 Chore

### Atualização de Infraestrutura (`docker-compose.yml`)
*   Atualização de tags/versões de imagens no ambiente de orquestração para garantir paridade entre os ambientes de desenvolvimento e produção.
*   Ajuste fino em definições de serviços para suportar as mudanças de telemetria.

### Build & CI/CD
*   **Triggered Build:** Sincronização de versão para o pipeline subsequente (26.14.003).

---

**Tech Lead:** Carlos Eduardo Duarte Schwalm (krlsedu)
**Commit Hash:** `b92bd51`