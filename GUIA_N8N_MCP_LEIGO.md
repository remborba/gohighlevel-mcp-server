# 🚀 GUIA COMPLETO: Como usar MCP GoHighLevel no n8n (Para Leigos)

## 📋 **PASSO 1: Iniciar o Servidor MCP**

### 1.1 Abrir terminal/prompt
- **Windows**: Win + R → digite `cmd` → Enter
- **Mac/Linux**: Abrir Terminal

### 1.2 Navegar para a pasta do projeto
```bash
cd "E:\ClaudeCode\Projetos\gohighlevel-mcp"
```

### 1.3 Iniciar o servidor
```bash
python mcp_server_http.py
```

**✅ Você deve ver:**
```
🚀 Iniciando servidor MCP para n8n...
📍 Acesse: http://localhost:3000
📋 Métodos: http://localhost:3000/methods
```

**❗ IMPORTANTE**: Deixe este terminal aberto! O servidor precisa ficar rodando.

---

## 📋 **PASSO 2: Testar o Servidor**

### 2.1 Abrir navegador
- Vá para: `http://localhost:3000`

### 2.2 Verificar se funciona
**✅ Você deve ver algo assim:**
```json
{
  "message": "GoHighLevel MCP Server",
  "available_methods": [
    "get_contacts",
    "create_contact", 
    "create_opportunity_natural",
    "send_sms"
  ]
}
```

---

## 📋 **PASSO 3: Configurar no n8n**

### 3.1 Abrir o n8n
- Acesse seu n8n (normalmente `http://localhost:5678`)

### 3.2 Criar novo workflow
- Clique em **"New Workflow"**

### 3.3 Adicionar node MCP
- Clique no **"+"** para adicionar node
- Procure por **"MCP"** 
- Selecione o node **"MCP Trigger"** ou **"MCP"**

### 3.4 Configurar o node MCP
**No campo URL, digite:**
```
http://localhost:3000/mcp
```

---

## 📋 **PASSO 4: Configurar Operações**

### 4.1 Para BUSCAR CONTATOS:
```json
{
  "method": "get_contacts",
  "params": {
    "limit": 10
  }
}
```

### 4.2 Para CRIAR CONTATO:
```json
{
  "method": "create_contact",
  "params": {
    "firstName": "João",
    "email": "joao@email.com",
    "phone": "+5511999999999"
  }
}
```

### 4.3 Para CRIAR OPORTUNIDADE:
```json
{
  "method": "create_opportunity_natural",
  "params": {
    "nome": "Maria Silva",
    "telefone": "11987654321",
    "email": "maria@email.com",
    "pipeline_name": "lead",
    "stage_name": "new lead",
    "valor": 1500
  }
}
```

---

## 📋 **PASSO 5: Exemplo Prático Completo**

### 5.1 Criar workflow simples:

**Node 1: Manual Trigger**
- Adicione um **"Manual Trigger"**

**Node 2: HTTP Request**
- Adicione **"HTTP Request"**
- **Method**: `POST`
- **URL**: `http://localhost:3000/mcp`
- **Body Type**: `JSON`
- **Body**:
```json
{
  "method": "get_contacts",
  "params": {
    "limit": 5
  }
}
```

**Node 3: Code (para processar resultado)**
- Adicione node **"Code"**
- **JavaScript**:
```javascript
// Processar resposta do MCP
const mcpResponse = $input.first().json;

if (mcpResponse.success) {
  const contacts = mcpResponse.data.contacts || [];
  
  return contacts.map(contact => ({
    id: contact.id,
    name: contact.name,
    email: contact.email,
    phone: contact.phone
  }));
} else {
  throw new Error('Erro no MCP: ' + mcpResponse.error);
}
```

### 5.2 Executar e testar
- Clique em **"Test workflow"**
- Verifique se retorna os contatos do GoHighLevel

---

## 📋 **PASSO 6: Workflows Avançados**

### 6.1 Webhook → Criar Oportunidade
```json
Node 1: Webhook (recebe dados)
↓
Node 2: HTTP Request (chama MCP)
{
  "method": "create_opportunity_natural",
  "params": {
    "nome": "{{$json.nome}}",
    "telefone": "{{$json.telefone}}",
    "email": "{{$json.email}}",
    "pipeline_name": "lead",
    "stage_name": "new lead",
    "valor": "{{$json.valor}}"
  }
}
↓
Node 3: Telegram (notificar sucesso)
```

### 6.2 Automação de Follow-up
```json
Node 1: Cron (agendamento)
↓ 
Node 2: MCP - Buscar oportunidades
↓
Node 3: Filter (filtrar por stage)
↓ 
Node 4: MCP - Enviar SMS
↓
Node 5: Telegram (relatório)
```

---

## 🔧 **TROUBLESHOOTING (Solução de Problemas)**

### ❌ "Cannot connect to localhost:3000"
**Solução:**
1. Verificar se o servidor MCP está rodando
2. Abrir terminal e rodar: `python mcp_server_http.py`
3. Verificar se não há firewall bloqueando

### ❌ "Method not found"
**Solução:**
1. Verificar se o método existe em: `http://localhost:3000/methods`
2. Conferir a escrita do método (case-sensitive)

### ❌ "GHL_API_KEY not found"
**Solução:**
1. Verificar arquivo `.env`
2. Confirmar se as variáveis estão corretas:
   ```
   GHL_API_KEY=sua-api-key
   GHL_LOCATION_ID=seu-location-id
   ```

### ❌ "422 Unprocessable Entity"
**Solução:**
1. Verificar se todos os campos obrigatórios estão preenchidos
2. Conferir formato dos dados (email válido, telefone correto)

---

## 📚 **MÉTODOS DISPONÍVEIS**

| Método | Descrição | Parâmetros Obrigatórios |
|--------|-----------|------------------------|
| `get_contacts` | Buscar contatos | `limit` (opcional) |
| `create_contact` | Criar contato | `firstName` |
| `create_opportunity_natural` | Criar oportunidade | `nome` |
| `send_sms` | Enviar SMS | `contactId`, `message` |
| `get_opportunities` | Buscar oportunidades | `limit` (opcional) |
| `get_pipelines` | Buscar pipelines | Nenhum |

---

## 🎯 **PRÓXIMOS PASSOS**

1. **Teste básico**: Criar workflow simples de buscar contatos
2. **Integração**: Conectar com webhook de formulário
3. **Automação**: Criar pipeline de follow-up automático
4. **Notificações**: Integrar com Telegram/Email
5. **Relatórios**: Dashboard de performance

---

## 📞 **SUPORTE**

Se tiver dúvidas:
1. Verificar logs do servidor MCP no terminal
2. Testar métodos em `http://localhost:3000/methods`
3. Conferir documentação do n8n sobre HTTP Request nodes

**✅ Pronto! Agora você tem MCP GoHighLevel funcionando no n8n!** 🎉