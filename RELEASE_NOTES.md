# Release Notes - v26.13.001

Esta versão consolida a implementação do **Huawei AX3 Pro Prometheus Exporter**, focando na estabilidade da coleta de métricas, melhoria no tratamento de erros e padronização do pipeline de CI/CD.

---

### 🚀 Features

*   **Monitoramento Prometheus:** Implementação de endpoint nativo para exportação de métricas (`/prometheus-metrics`).
*   **Health Check:** Adição de rota de saúde (`/health`) e método `is_valid` para monitoramento do status da aplicação e dos serviços Huawei/Metrics.
*   **Suporte a Docker:** Criação de `Dockerfile` otimizado e `docker-compose.yml` para orquestração local.
*   **Dashboard Grafana:** Inclusão de template JSON pré-configurado para visualização das métricas do roteador Huawei AX3 Pro.
*   **CORS Support:** Adicionado suporte a Cross-Origin Resource Sharing (CORS) na API Flask.
*   **Documentação Técnica:** Criação de guia de execução no `README.md`, além dos arquivos de governança `LICENSE` e `CODE_OF_CONDUCT.md`.

---

### 🐛 Fixes

*   **Tratamento de Erros:** Refatoração robusta no tratamento de exceções durante a conversão de métricas e no processo de scraping.
*   **Estabilidade do Scraper:** Ajuste no caminho do target do scraper no serviço Huawei e atualização da lógica de verificação de validade de variáveis.
*   **Limpeza de Binários:** Remoção de arquivos executáveis (`phantomjs.exe`, `ghostdriver.log`) do repositório para reduzir o tamanho do artefato e evitar conflitos de ambiente.
*   **Ajuste de Rotas:** Padronização do endpoint de métricas e parâmetros de execução do Flask.

---

### 🔧 Chore

*   **CI/CD Pipeline:** Atualização do `Jenkinsfile` com suporte a credenciais SSH e melhorias no deploy automatizado.
*   **Gerenciamento de Dependências:** Atualização do `requirements.txt` e inclusão de novas bibliotecas necessárias.
*   **Git Ignore:** Atualização do `.gitignore` para ignorar arquivos de log, binários e arquivos de sistema.
*   **Refatoração de Código:** Limpeza de seções obsoletas no `README.md` (Histórico de Versões e Autores) e simplificação do `Dockerfile`.
*   **Build Automation:** Sincronização de versões via `version.txt` através de múltiplos gatilhos de build automatizados.

---
*Build consolidado por Tech Lead.*