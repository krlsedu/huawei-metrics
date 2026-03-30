Aqui está o Release Notes técnico para a versão **v26.14.003**, focado em clareza para a equipe de engenharia e stakeholders técnicos.

---

# 📦 Release Notes - v26.14.003

## Resumo
Esta atualização foca na padronização e confiabilidade da coleta de métricas do sistema. O objetivo principal foi alinhar a exportação de dados com padrões de mercado (Prometheus) e refinar o cálculo de tráfego de rede para garantir observabilidade precisa.

---

## 🚀 Features
- **Padronização Prometheus:** Formatação do output JSON de métricas ajustada para total compatibilidade com as convenções do Prometheus, facilitando a integração com dashboards Grafana.
- **Cálculo de Tráfego LAN/WAN:** Implementação de lógica aprimorada para a distinção e cálculo de tráfego de rede, garantindo maior precisão nos dados de throughput.

## 🐛 Fixes
- **Consistência de Nomenclatura:** Refatoração de identificadores e variáveis no serviço de métricas para eliminar ambiguidades e seguir o padrão do projeto.
- **Documentação Inline:** Melhoria significativa nos comentários do código (`Metrics.py`), facilitando a manutenção futura e o entendimento da lógica de agregação.

## 🔧 Chore
- **Refatoração de Código:** Limpeza e reestruturação do arquivo `services/Metrics.py` (61 inserções, 50 deleções), resultando em um código mais modular e performático.

---

### 🛠 Detalhes Técnicos
- **Commit:** `b54a276`
- **Arquivo afetado:** `services/Metrics.py`
- **Autor:** Carlos Eduardo Duarte Schwalm (krlsedu)