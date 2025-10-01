# GoHighLevel MCP Server

Um servidor MCP (Model Context Protocol) para integrar o GoHighLevel com o Claude, permitindo gerenciar seus contatos, conversas, compromissos e oportunidades diretamente na interface do Claude.

## ✨ Funcionalidades

### 🧑‍💼 Gestão de Contatos
- **ghl_get_contacts**: Buscar contatos com filtros opcionais
- **ghl_get_contact**: Obter um contato específico por ID
- **ghl_create_contact**: Criar novos contatos
- **ghl_update_contact**: Atualizar contatos existentes

### 💬 Conversas e Mensagens
- **ghl_get_conversations**: Listar conversas recentes
- **ghl_send_message**: Enviar mensagens SMS/Email para contatos

### 📅 Agendamentos
- **ghl_get_appointments**: Buscar compromissos por período
- **ghl_create_appointment**: Criar novos agendamentos

### 🎯 Oportunidades de Vendas
- **ghl_get_pipelines**: Listar pipelines disponíveis
- **ghl_get_opportunities**: Buscar oportunidades por pipeline

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone <repository-url>
cd gohighlevel-mcp
```

### 2. Configure as variáveis de ambiente
```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione suas credenciais do GoHighLevel:

```env
# GoHighLevel API Configuration
GHL_API_KEY=your_ghl_api_key_here
GHL_LOCATION_ID=your_location_id_here
GHL_API_VERSION=v1

# Optional: Set base URL if using different environment
# GHL_BASE_URL=https://services.leadconnectorhq.com
```

### 3. Instale as dependências

#### Usando uv (recomendado)
```bash
uv sync
```

#### Usando pip
```bash
pip install -e .
```

## 🔑 Configuração do GoHighLevel

### Obter sua API Key
1. Acesse sua conta do GoHighLevel
2. Vá para Settings > Integrations > API
3. Gere uma nova API Key
4. Copie e cole no arquivo `.env`

### Obter seu Location ID
1. Na mesma tela de API, você encontrará seu Location ID
2. Ou acesse Settings > Company Settings e copie o ID da localização
3. Cole no arquivo `.env`

## 📦 Configuração no Claude Desktop

### 1. Localize o arquivo de configuração do Claude

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### 2. Adicione o servidor MCP

```json
{
  "mcpServers": {
    "gohighlevel": {
      "command": "python",
      "args": ["-m", "gohighlevel_mcp.server"],
      "cwd": "/path/to/gohighlevel-mcp",
      "env": {
        "GHL_API_KEY": "your_api_key_here",
        "GHL_LOCATION_ID": "your_location_id_here"
      }
    }
  }
}
```

### 3. Reinicie o Claude Desktop

Após salvar a configuração, reinicie o Claude Desktop para carregar o servidor MCP.

## 🛠️ Uso

Agora você pode usar os comandos do GoHighLevel diretamente no Claude:

### Exemplos de comandos:

**Buscar contatos:**
```
Mostre meus últimos 10 contatos do GoHighLevel
```

**Criar um contato:**
```
Crie um novo contato no GHL com nome "João Silva", email "joao@email.com" e telefone "(11)99999-9999"
```

**Enviar mensagem:**
```
Envie uma mensagem SMS para o contato ID "abc123" com o texto "Olá! Como você está?"
```

**Buscar compromissos:**
```
Mostre meus compromissos de hoje no GoHighLevel
```

**Criar compromisso:**
```
Agende uma reunião para amanhã às 14h com o contato ID "abc123" no calendário "cal_123"
```

## 🔧 Desenvolvimento

### Executar em modo de desenvolvimento
```bash
uv run python -m gohighlevel_mcp.server
```

### Executar testes
```bash
uv run pytest
```

### Estrutura do projeto
```
gohighlevel-mcp/
├── gohighlevel_mcp/
│   ├── __init__.py
│   ├── client.py          # Cliente da API do GoHighLevel
│   └── server.py          # Servidor MCP
├── tests/
├── .env.example
├── pyproject.toml
└── README.md
```

## 🚨 Solução de Problemas

### Erro: "GHL_API_KEY and GHL_LOCATION_ID must be set"
- Verifique se o arquivo `.env` está no diretório correto
- Confirme se as variáveis estão definidas corretamente
- Reinicie o Claude Desktop

### Erro: "Authorization failed"
- Verifique se sua API Key está correta
- Confirme se a API Key tem as permissões necessárias
- Teste a API Key diretamente usando Postman ou curl

### Erro: "Contact not found"
- Verifique se o ID do contato está correto
- Confirme se o contato pertence à localização configurada

## 📝 Logs e Debug

Para habilitar logs detalhados, adicione ao `.env`:
```env
DEBUG=true
```

## 🔒 Segurança

- **Nunca compartilhe** sua API Key do GoHighLevel
- Mantenha o arquivo `.env` fora do controle de versão
- Use variáveis de ambiente em produção
- Monitore o uso da API para detectar atividades suspeitas

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙋‍♂️ Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique a [seção de solução de problemas](#-solução-de-problemas)
2. Consulte a [documentação da API do GoHighLevel](https://marketplace.gohighlevel.com/docs/)
3. Abra uma issue no GitHub

---

**⚡ Potencialize seu GoHighLevel com o poder do Claude!**