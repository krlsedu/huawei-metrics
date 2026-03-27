Aqui está o Release Notes técnico para a versão **v26.13.004**, focado em clareza e impacto técnico.

---

# 📝 Release Notes - v26.13.004

## Resumo
Esta versão foca na correção da serialização de métricas, garantindo a integridade dos dados temporais ao adotar objetos datetime com fuso horário (timezone-aware).

---

## 🐛 Fixes

### Core / Metrics Service
- **Correção na formatação de métricas JSON:** Ajustada a lógica de serialização no serviço de métricas para utilizar objetos `datetime` com informação de fuso horário. 
    - **Impacto:** Resolve problemas de inconsistência em dashboards e ferramentas de monitoramento que dependem de precisão temporal (UTC vs Local Time).
    - **Arquivo afetado:** `services/Metrics.py`

---

## 🚀 Features
*Nenhuma nova funcionalidade foi introduzida nesta versão.*

---

## 🔧 Chore
*Nenhuma tarefa de manutenção ou infraestrutura foi registrada nesta versão.*

---

**Informações Técnicas:**
- **Commit:** `a8a6c23`
- **Autor:** Carlos Eduardo Duarte Schwalm (krlsedu)
- **Data de Referência:** 2026