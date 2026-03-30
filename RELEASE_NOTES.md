Aqui está o Release Notes técnico para a versão **v26.14.001**, estruturado conforme as boas práticas de engenharia.

---

# 📦 Release Notes - v26.14.001

## Resumo
Esta versão foca na correção de integridade de dados nos serviços de telemetria e na atualização da infraestrutura de build e versionamento do projeto.

---

### 🐛 Fixes
*   **Metrics Service:** Corrigida a formatação de métricas JSON para utilizar objetos `datetime` com suporte a fuso horário (*timezone-aware*). Esta alteração evita inconsistências em ambientes distribuídos e garante a precisão temporal dos logs e dashboards.

### 🔧 Chore
*   **Build System:** Disparado o processo de build automático para a transição de versão (Ref: `26.13.004` -> `26.14.001`).
*   **Infrastructure:** Atualização do arquivo `docker-compose.yml` e sincronização do arquivo global de versão (`version.txt`).
*   **Documentation:** Atualização do histórico de alterações no `RELEASE_NOTES.md`.

---

### 🛠 Detalhes Técnicos
*   **ID do Commit:** `a8a6c23` (Fix de métricas)
*   **ID do Commit:** `bea5a33` (Trigger de Build)
*   **Arquivos afetados:** 4
*   **Impacto:** Baixo. Recomenda-se o deploy imediato para normalização da série temporal de métricas.