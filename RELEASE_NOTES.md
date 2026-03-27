Aqui está o Release Notes técnico para a versão **v26.13.003**, estruturado com base nas alterações identificadas no commit.

---

# 📦 Release Notes - v26.13.003

## Resumo Técnico
Esta versão foca na expansão da infraestrutura de dados, introduzindo persistência analítica via ClickHouse e otimizando a coleta de métricas. Foram implementadas melhorias significativas no processamento em segundo plano para garantir maior escalabilidade na ingestão de dados.

---

## 🚀 Features

*   **Integração com ClickHouse:** Implementação do novo serviço `ClickHouseDb.py`, permitindo o armazenamento de dados em alta performance para fins analíticos.
*   **Ingestão de Dados em Background:** Otimização do fluxo principal (`app.py`) para suportar a ingestão de dados de forma assíncrona, reduzindo o tempo de resposta da aplicação.
*   **Novo Sistema de Métricas:** Introdução do serviço `Metrics.py` com suporte a formatação em **JSON**, facilitando a integração com ferramentas de monitoramento (ex: Prometheus, Grafana).
*   **Expansão do Provedor Huawei:** Atualização no serviço `Huawei.py` para suporte a novos campos ou métodos de coleta.

## 🐛 Fixes

*   **Ajustes de Conectividade:** Correções pontuais na comunicação entre serviços internos e a camada de persistência.
*   **Estabilidade no App Core:** Refatoração de blocos lógicos no `app.py` para melhor tratamento de exceções durante o processamento de métricas.

## 🔧 Chore

*   **Atualização de Dependências:** Inclusão de novas bibliotecas no `requirements.txt` necessárias para a conexão com ClickHouse.
*   **Orquestração Docker:** Ajustes no `docker-compose.yml` para provisionamento e configuração dos novos serviços de banco de dados e rede.
*   **Estrutura de Pacotes:** Inicialização do módulo `service/__init__.py`.

---

### 📊 Estatísticas do Commit
- **Arquivos alterados:** 7
- **Inserções:** 168
- **Deleções:** 7
- **Responsável:** Carlos Eduardo Duarte Schwalm