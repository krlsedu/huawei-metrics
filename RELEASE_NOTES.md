Olá, time. Como Tech Lead responsável, analisei o commit `9510e42` e consolidei as alterações para a versão **v26.13.002**.

Esta release foca na expansão da observabilidade de rede, introduzindo a coleta de métricas de tráfego WAN, além de melhorias na infraestrutura de containerização.

---

# Release Notes - v26.13.002

## 🚀 Features
*   **Métricas de Tráfego WAN:** Implementado suporte para coleta e exposição de métricas de tráfego WAN (Wide Area Network).
*   **Atualização do Scraper:** Evolução da lógica de scraping no serviço `Huawei.py` para suportar os novos datapoints.
*   **Novo Módulo de Métricas:** Adição do serviço `Metrics.py` para centralizar a lógica de processamento de indicadores.

## 🐛 Fixes
*   **Ajuste na Inicialização:** Pequena correção na lógica de bootstrap do `app.py` para garantir a correta carga dos novos serviços de métricas.

## 🔧 Chore
*   **Otimização Docker:** Adição do arquivo `.dockerignore` robusto para reduzir o contexto de build e aumentar a segurança da imagem.
*   **Padronização de Nomenclatura:** Criação dos arquivos de metadados `app_name.txt` e `docker_name.txt` para automação de CI/CD.

---

### 📝 Resumo Técnico
*   **Total de arquivos alterados:** 6
*   **Linhas adicionadas:** 77
*   **Linhas removidas:** 2
*   **Impacto:** Alta melhoria na visibilidade de performance de rede para dispositivos Huawei.

**Assinado por:**
*Tech Lead*