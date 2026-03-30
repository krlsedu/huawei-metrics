Aqui está o Release Notes técnico para a versão **v26.14.005**, estruturado conforme as boas práticas de engenharia.

---

# 📦 Release Notes - v26.14.005

## Resumo Técnico
Esta versão foca na otimização da performance de coleta de dados (scraping) e na resiliência do sistema. A principal mudança é a desaceleração e o isolamento do processamento de rede WAN, garantindo que falhas externas não impactem o fluxo principal da aplicação.

---

## 🚀 Features
- **Isolamento de Thread para WAN:** Implementação de uma thread dedicada para o scraping de WAN. Isso evita gargalos no loop principal e permite que a coleta de dados de rede ocorra de forma assíncrona.
- **Ajuste de Intervalo de Scraping:** O tempo de atualização do scraper foi ajustado para **5 segundos**, otimizando o consumo de recursos e evitando possíveis bloqueios por excesso de requisições.

## 🐛 Fixes
- **Melhoria no Error Handling:** Refatoração da lógica de tratamento de exceções durante o processo de scraping, garantindo que erros pontuais de rede não causem o encerramento inesperado do serviço.

## 🔧 Chore
- **Update de Infraestrutura:** Atualização da imagem Docker para a versão `26.14.005` no arquivo `docker-compose.yml`.
- **Refatoração de Código:** Limpeza e reestruturação do arquivo `app.py` para suporte à nova arquitetura multi-thread.

---

### 🛠 Detalhes Técnicos (Diff Stats)
- **Arquivos alterados:** 2
- **Inserções:** 23
- **Deleções:** 16
- **Commit ID:** `b82041f`
- **Autor:** Carlos Eduardo Duarte Schwalm (krlsedu)