# GoHighLevel MCP v2 - Guia de Instalação para Cliente

## O Que É

Sistema completo para automatizar GoHighLevel via n8n usando **suas próprias credenciais**.

---

## Instalação (3 Passos)

### Passo 1: Configurar Variáveis de Ambiente no n8n

No seu n8n, adicione estas variáveis de ambiente:

**Como adicionar:**
- Se n8n local: arquivo `.env` na pasta do n8n
- Se Docker: `docker-compose.yml` na seção `environment`
- Se EasyPanel: Settings > Environment

**Variáveis:**
```
GHL_API_KEY=seu_token_do_gohighlevel_aqui
GHL_LOCATION_ID=seu_location_id_aqui
```

**Onde pegar essas informações:**
1. GoHighLevel > Settings > Company > API Keys
2. Copie seu API Token
3. Copie seu Location ID

**Reinicie o n8n** após adicionar as variáveis.

---

### Passo 2: Importar Workflow

1. Baixe o arquivo `GHL-MCP-v2-Client.json`
2. No n8n: Menu **☰** > **Import from File**
3. Selecione o arquivo
4. Clique em **Import**

---

### Passo 3: Testar

1. Abra o workflow importado
2. Clique em **Execute Workflow**
3. Deve criar um contato "João Silva" no seu GHL

✅ **Funcionou? Pronto para usar!**

---

## Como Funciona

O workflow tem 3 nodes:

1. **Manual Trigger** - Inicia o workflow
2. **Setup Credentials** - Pega suas credenciais das variáveis de ambiente
3. **GHL MCP Server** - Envia pro servidor e executa no GHL

**Suas credenciais:**
- Ficam no SEU n8n (seguro)
- Nunca são armazenadas no servidor MCP
- São enviadas apenas na hora da requisição

---

## Operações Disponíveis

Para mudar a operação, edite o node "Setup Credentials":

### Listar Contatos
```json
{
  "credentials": {
    "apiKey": "{{ $env.GHL_API_KEY }}",
    "locationId": "{{ $env.GHL_LOCATION_ID }}"
  },
  "method": "get_contacts",
  "params": {
    "limit": 10
  }
}
```

### Criar Contato
```json
{
  "credentials": {
    "apiKey": "{{ $env.GHL_API_KEY }}",
    "locationId": "{{ $env.GHL_LOCATION_ID }}"
  },
  "method": "create_contact",
  "params": {
    "firstName": "Maria",
    "lastName": "Santos",
    "email": "maria@email.com",
    "phone": "+5511988887777"
  }
}
```

### Enviar SMS
```json
{
  "credentials": {
    "apiKey": "{{ $env.GHL_API_KEY }}",
    "locationId": "{{ $env.GHL_LOCATION_ID }}"
  },
  "method": "send_sms",
  "params": {
    "contactId": "id_do_contato",
    "message": "Olá! Mensagem automática."
  }
}
```

### Ver Pipelines
```json
{
  "credentials": {
    "apiKey": "{{ $env.GHL_API_KEY }}",
    "locationId": "{{ $env.GHL_LOCATION_ID }}"
  },
  "method": "get_pipelines",
  "params": {}
}
```

---

## Integração com Webhooks

Para usar com webhook (receber dados externos):

1. Substitua "Manual Trigger" por "Webhook"
2. Configure o path
3. O restante funciona igual

**Exemplo:** Webhook recebe lead do Facebook Ads → Cria contato no GHL

---

## Segurança

✅ Suas credenciais ficam no seu n8n  
✅ Credenciais são enviadas apenas na requisição  
✅ Servidor MCP não armazena nada  
✅ Conexão HTTPS criptografada  

---

## Suporte

- Dúvidas: [Seu contato]
- Documentação: [Seu site]

---

## FAQ

**P: Minhas credenciais estão seguras?**
R: Sim. Elas ficam no SEU n8n e são enviadas criptografadas (HTTPS) apenas quando necessário.

**P: Posso usar múltiplas contas GHL?**
R: Sim. Crie variáveis diferentes (GHL_API_KEY_2, etc) e workflows separados.

**P: Tem limite de uso?**
R: Não. Use quanto precisar.

**P: E se eu mudar meu token do GHL?**
R: Basta atualizar a variável de ambiente e reiniciar o n8n.

---

Pronto para começar! Qualquer dúvida, entre em contato.
