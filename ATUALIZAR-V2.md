# Atualizar Servidor MCP para Versão 2.0

## O Que Mudou

✅ Agora aceita credenciais por requisição  
✅ Cada cliente pode usar suas próprias credenciais  
✅ Backward compatible (ainda aceita credenciais do .env como fallback)

---

## Atualização no Servidor

### 1. Atualizar Dockerfile

Abra o `Dockerfile` e mude a última linha:

**Antes:**
```dockerfile
CMD ["python", "mcp_server_http.py"]
```

**Depois:**
```dockerfile
CMD ["python", "mcp_server_http_v2.py"]
```

### 2. Atualizar requirements.txt

Adicione a biblioteca httpx:

```
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
requests==2.31.0
httpx==0.25.1
pydantic==2.5.0
```

### 3. Fazer Push pro GitHub

No terminal:

```bash
cd E:\ClaudeCode\Projetos\gohighlevel-mcp
git add .
git commit -m "Update para v2.0 - Suporte a credenciais dinâmicas"
git push
```

### 4. Redeployar no EasyPanel

1. Vá no EasyPanel
2. App `mcp-github`
3. Clique em **Implantar** (botão verde)
4. Aguarde o build (2-3 minutos)

### 5. Testar

Acesse: `https://mcp-github.va1qz0.easypanel.host/`

Deve aparecer:
```json
{
  "message": "GoHighLevel MCP Server v2.0 - Suporta credenciais dinâmicas"
}
```

---

## Como o Cliente Usa

### Workflow Atualizado

O cliente adiciona um node **"Set"** ou **"Code"** no início do workflow para configurar suas credenciais uma única vez:

**Node Set:**
```
Field 1:
- Name: credentials
- Value (JSON):
{
  "apiKey": "token_do_cliente",
  "locationId": "location_id_do_cliente"
}

Field 2:
- Name: method
- Value: create_contact

Field 3:
- Name: params
- Value (JSON):
{
  "firstName": "João",
  "email": "joao@email.com"
}
```

**OU Node Code:**
```javascript
return [{
  json: {
    credentials: {
      apiKey: $env.GHL_API_KEY,  // Do environment do n8n
      locationId: $env.GHL_LOCATION_ID
    },
    method: "create_contact",
    params: {
      firstName: "João",
      email: "joao@email.com"
    }
  }
}];
```

---

## Vantagens

1. ✅ Cliente usa suas próprias credenciais
2. ✅ Credenciais ficam no n8n do cliente (seguro)
3. ✅ Você não gerencia credenciais de terceiros
4. ✅ Múltiplos clientes no mesmo servidor
5. ✅ Ainda funciona com credenciais padrão (seu uso pessoal)

---

## Próximos Passos

1. Fazer update do servidor
2. Testar
3. Atualizar workflow do cliente
4. Redistribuir

Qualquer erro, verifique os logs no EasyPanel.
