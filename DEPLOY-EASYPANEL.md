# 🚀 Deploy no EasyPanel - Guia Completo Para Iniciantes

## PARTE 1: Preparar os Arquivos

✅ Já criado! Os arquivos necessários foram criados:
- `Dockerfile` - Instruções para criar o container
- `requirements.txt` - Dependências do Python
- `.dockerignore` - Arquivos a ignorar

## PARTE 2: Subir Código pro GitHub

### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/
2. Clique no botão verde **"New"** (canto superior direito)
3. Nome do repositório: `gohighlevel-mcp-server`
4. Deixe como **Public**
5. **NÃO** marque nenhum checkbox (README, .gitignore, etc)
6. Clique em **"Create repository"**

### Passo 2: Subir o Código

Abra o terminal/prompt de comando na pasta do projeto e execute:

```bash
# Ir até a pasta do projeto
cd E:\ClaudeCode\Projetos\gohighlevel-mcp

# Inicializar Git (se ainda não tiver)
git init

# Adicionar todos os arquivos (EXCETO o .env - que tem suas credenciais)
git add .
git commit -m "Deploy inicial"

# Conectar com seu repositório GitHub (substitua SEU-USUARIO pelo seu usuário do GitHub)
git remote add origin https://github.com/SEU-USUARIO/gohighlevel-mcp-server.git

# Enviar o código
git branch -M main
git push -u origin main
```

**IMPORTANTE:** O arquivo `.env` NÃO vai ser enviado (tem suas credenciais). Você vai configurar as variáveis no EasyPanel.

---

## PARTE 3: Configurar no EasyPanel

### Passo 1: Acessar o EasyPanel

1. Acesse seu EasyPanel (onde seu n8n está)
2. Faça login

### Passo 2: Criar Novo App

1. Clique em **"New App"** ou **"Add App"**
2. Selecione **"Deploy from GitHub"**
3. Conecte sua conta do GitHub (se ainda não conectou)
4. Selecione o repositório: `gohighlevel-mcp-server`
5. Branch: `main`

### Passo 3: Configurar o App

**Nome do App:**
```
ghl-mcp-server
```

**Configurações de Build:**
- Build Type: **Dockerfile**
- Dockerfile Path: `Dockerfile` (deixe padrão)

**Porta:**
```
3000
```

### Passo 4: Configurar Variáveis de Ambiente

Ainda na configuração do app, vá em **"Environment Variables"** e adicione:

```
GHL_API_KEY=cole_seu_token_do_ghl_aqui
GHL_LOCATION_ID=cole_seu_location_id_aqui
GHL_API_VERSION=v1
```

**Onde pegar essas informações?**
- Abra seu arquivo `.env` local (tem as credenciais)
- Copie os valores de lá

### Passo 5: Deploy!

1. Clique em **"Deploy"** ou **"Create App"**
2. Aguarde o build (2-5 minutos)
3. Quando terminar, vai aparecer uma URL tipo:
   ```
   https://ghl-mcp-server.seu-dominio.easypanel.io
   ```

### Passo 6: Testar

Abra no navegador:
```
https://ghl-mcp-server.seu-dominio.easypanel.io/
```

Deve aparecer:
```json
{
  "message": "GoHighLevel MCP Server",
  "available_methods": [...]
}
```

✅ **Funcionou? Servidor está no ar!**

---

## PARTE 4: Conectar no n8n

### Passo 1: No seu n8n (que já está no EasyPanel)

1. Crie um novo workflow
2. Adicione um node **HTTP Request**

### Passo 2: Configurar o Node

**URL:**
```
https://ghl-mcp-server.seu-dominio.easypanel.io/mcp
```

**Method:** `POST`

**Body:**
```json
{
  "method": "get_contacts",
  "params": {
    "limit": 10
  }
}
```

**Headers:**
```
Content-Type: application/json
```

### Passo 3: Testar

1. Execute o node
2. Deve retornar os contatos do GHL

---

## PARTE 5: Métodos Disponíveis

Você pode chamar qualquer um desses métodos no n8n:

### Criar Contato
```json
{
  "method": "create_contact",
  "params": {
    "firstName": "João",
    "lastName": "Silva",
    "email": "joao@email.com",
    "phone": "+5511999999999"
  }
}
```

### Buscar Contatos
```json
{
  "method": "get_contacts",
  "params": {
    "limit": 50
  }
}
```

### Criar Oportunidade (Jeito Natural)
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

### Enviar SMS
```json
{
  "method": "send_sms",
  "params": {
    "contactId": "id_do_contato",
    "message": "Sua mensagem aqui"
  }
}
```

### Ver Pipelines
```json
{
  "method": "get_pipelines",
  "params": {}
}
```

---

## DICAS IMPORTANTES

### 1. Ver Logs no EasyPanel
- Vá no seu app `ghl-mcp-server`
- Clique em **"Logs"**
- Aí você vê se tem algum erro

### 2. Atualizar o Código
Sempre que fizer alteração:
```bash
git add .
git commit -m "descrição da alteração"
git push
```

O EasyPanel detecta automaticamente e faz novo deploy.

### 3. Reiniciar o Servidor
No EasyPanel:
- App > **"Restart"**

### 4. Domínio Customizado (Opcional)
Se quiser um domínio próprio tipo `ghl.seudominio.com`:
- No EasyPanel: App > Settings > Domains
- Adicione seu domínio
- Configure o DNS apontando pro EasyPanel

---

## TROUBLESHOOTING

### Erro: "Cannot connect to server"
- Verifique se o app está rodando no EasyPanel
- Veja os logs

### Erro: "Missing API credentials"
- Verifique as variáveis de ambiente no EasyPanel
- Certifique-se que `GHL_API_KEY` e `GHL_LOCATION_ID` estão corretas

### App não inicia
- Veja os logs do build
- Verifique se o Dockerfile está correto

---

## PRÓXIMOS PASSOS

Agora você pode:
1. ✅ Criar workflows no n8n conectando nesse servidor
2. ✅ Compartilhar a URL com outras pessoas/empresas
3. ✅ Cada empresa usa com suas próprias credenciais (você mostra como eles sobem)

Quer que eu crie workflows prontos do n8n pra você usar?
