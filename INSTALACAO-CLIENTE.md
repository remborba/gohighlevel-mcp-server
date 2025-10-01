# GoHighLevel MCP - Instalação para Cliente

## O Que É

Sistema completo para automatizar GoHighLevel via n8n, sem precisar de OAuth2 ou White Label.

---

## Requisitos

- n8n instalado (qualquer versão)
- Conta GoHighLevel
- API Token do GoHighLevel
- Location ID do GoHighLevel

---

## Instalação (5 Minutos)

### 1. Importar Workflow

1. Baixe o arquivo `GHL-MCP-Base.json`
2. No seu n8n: Menu **☰** > **Import from File**
3. Selecione o arquivo
4. Clique em **Import**

### 2. Pronto!

O workflow já está configurado e funcional. Não precisa instalar nada adicional.

---

## Como Usar

### Operações Disponíveis

**Contatos:**
- `get_contacts` - Listar contatos
- `create_contact` - Criar contato

**Oportunidades:**
- `create_opportunity_natural` - Criar oportunidade
- `get_opportunities` - Listar oportunidades
- `get_pipelines` - Ver pipelines

**SMS:**
- `send_sms` - Enviar SMS

**Conversas:**
- `get_conversations` - Ver conversas

---

## Exemplos de Uso

### Criar Contato

1. Adicione um node antes do "GHL MCP"
2. Configure o input:

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

### Listar Contatos

```json
{
  "method": "get_contacts",
  "params": {
    "limit": 10
  }
}
```

### Criar Oportunidade

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
    "contactId": "id_do_contato_aqui",
    "message": "Olá! Esta é uma mensagem de teste."
  }
}
```

---

## Workflows Prontos

Incluímos workflows prontos para casos comuns:

1. **GHL-Contact-Management.json** - Gestão de contatos
2. **GHL-Opportunity-Pipeline.json** - Pipeline de oportunidades
3. **GHL-Appointment-Automation.json** - Automação de agendamentos

Importe conforme necessário.

---

## Integrar com Webhook

### Para Receber Dados Externos

1. Substitua o "Manual Trigger" por "Webhook"
2. Configure o path (ex: `/ghl-webhook`)
3. Use a URL gerada para receber dados

### Exemplo: Webhook + GHL MCP

```
[Webhook] → [Processar Dados] → [GHL MCP] → [Responder]
```

---

## Suporte

- Documentação completa: [Seu site]
- Dúvidas: [Seu email/whatsapp]
- Exemplos extras: [Repositório GitHub]

---

## Notas Importantes

- O servidor MCP é mantido 24/7
- Suas credenciais do GHL nunca são compartilhadas
- Todas as chamadas são feitas diretamente entre seu n8n e o servidor MCP
- Sem limite de uso
- Sem custos adicionais

---

## Próximos Passos

1. Teste com os exemplos acima
2. Adapte para seu caso de uso
3. Crie automações complexas combinando nodes

Qualquer dúvida, entre em contato!
