Aqui está o Release Notes técnico para a versão **v26.14.004**, focado em clareza e padronização para a equipe de engenharia.

---

# 📦 Release Notes - v26.14.004

## Resumo
Esta versão foca na padronização técnica do esquema de dados no ClickHouse, visando consistência com as convenções de nomenclatura internacionais do projeto.

---

## 🔧 Chore
- **Padronização de Schema (ClickHouse):** Refatoração do nome da coluna de `dados` para `data`. 
    - *Impacto:* Melhora a consistência semântica do banco de dados.
    - *Arquivos afetados:* `service/ClickHouseDb.py`.

---

## 📝 Notas Técnicas de Migração
> [!IMPORTANT]
> Esta alteração modifica o contrato de dados entre a aplicação e o ClickHouse. Certifique-se de que as queries externas ou dashboards de BI que consomem esta tabela foram atualizados para refletir o novo nome da coluna (`data`).

---
**Tech Lead:** Carlos Eduardo Duarte Schwalm (krlsedu)
**Commit:** `8a8a47e`