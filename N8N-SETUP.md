# 🔗 Configuração dos Workflows n8n para GoHighLevel

Este guia mostra como configurar os workflows n8n para automação completa do GoHighLevel junto com o MCP server.

## 📋 Workflows Disponíveis

### 1. 🧑‍💼 Gestão de Contatos (`ghl-contact-management.json`)
**Funcionalidades:**
- Webhook para eventos de contatos (criação/atualização)
- Envio automático de mensagem de boas-vindas para novos contatos
- Adição automática de tags para categorização
- Notificações no Slack para novos contatos e atualizações

### 2. 🎯 Pipeline de Oportunidades (`ghl-opportunity-pipeline.json`)
**Funcionalidades:**
- Webhook para mudanças de estágio em oportunidades
- Mensagens automáticas para oportunidades ganhas
- Notificações diferenciadas para vendas fechadas e perdidas
- Relatório semanal automático de vendas no Slack
- Adição de tags baseada no resultado da oportunidade

### 3. 📅 Automação de Agendamentos (`ghl-appointment-automation.json`)
**Funcionalidades:**
- Webhook para novos agendamentos e atualizações
- Confirmação automática por SMS e Email
- Lembretes diários para agendamentos do dia seguinte
- Notificações no Slack para toda a equipe

## 🚀 Instalação dos Workflows

### Passo 1: Importar os Workflows

1. **Acesse seu n8n**
2. **Clique em "Import workflow"**
3. **Selecione um dos arquivos JSON:**
   - `n8n-workflows/ghl-contact-management.json`
   - `n8n-workflows/ghl-opportunity-pipeline.json`
   - `n8n-workflows/ghl-appointment-automation.json`

### Passo 2: Configurar Credenciais

#### 🔑 GoHighLevel API
1. **Vá em Settings > Credentials**
2. **Crie nova credencial "HTTP Header Auth"**
3. **Configure:**
   - **Nome:** `GoHighLevel API`
   - **Header Name:** `Authorization`
   - **Header Value:** `Bearer YOUR_GHL_API_KEY`

#### 💬 Slack API (Opcional)
1. **Crie uma nova credencial "Slack API"**
2. **Configure com seu token do Slack**
3. **Teste a conexão**

### Passo 3: Configurar Webhooks no GoHighLevel

#### 🔗 URLs dos Webhooks
Após ativar os workflows, você receberá URLs como:
```
https://your-n8n-instance.com/webhook/ghl-webhook
https://your-n8n-instance.com/webhook/ghl-opportunity-webhook
https://your-n8n-instance.com/webhook/ghl-appointment-webhook
```

#### ⚙️ Configuração no GoHighLevel
1. **Acesse GoHighLevel > Settings > Integrations > Webhooks**
2. **Crie novos webhooks:**

**Para Contatos:**
- **URL:** `https://your-n8n-instance.com/webhook/ghl-webhook`
- **Eventos:** Contact Create, Contact Update
- **Método:** POST

**Para Oportunidades:**
- **URL:** `https://your-n8n-instance.com/webhook/ghl-opportunity-webhook`
- **Eventos:** Opportunity Stage Update
- **Método:** POST

**Para Agendamentos:**
- **URL:** `https://your-n8n-instance.com/webhook/ghl-appointment-webhook`
- **Eventos:** Appointment Create, Appointment Update
- **Método:** POST

## 🛠️ Personalização dos Workflows

### 📝 Mensagens Personalizadas

#### Mensagem de Boas-Vindas (Contatos)
Edite o nó "Enviar Mensagem de Boas-Vindas":
```json
{
  "message": "Olá {{firstName}}! Seja bem-vindo(a) à nossa empresa. Em breve entraremos em contato! 😊"
}
```

#### Confirmação de Agendamento
Edite o nó "Enviar SMS de Confirmação":
```json
{
  "message": "✅ Agendamento confirmado!\n\n📅 Data: {{date}}\n🕐 Horário: {{time}}\n\nAguardamos você! 😊"
}
```

### 🏷️ Tags Automáticas

#### Para Novos Contatos
```json
{
  "tags": ["novo-contato", "via-webhook", "lead-automatico"]
}
```

#### Para Oportunidades Ganhas
```json
{
  "tags": ["cliente-convertido", "pipeline-won", "follow-up-pos-venda"]
}
```

### 📊 Canais do Slack

Personalize os canais conforme sua estrutura:
- `#gohighlevel` - Notificações gerais
- `#vendas` - Oportunidades e relatórios
- `#agendamentos` - Confirmações e lembretes

## ⏰ Agendamentos Automáticos

### Relatório Semanal de Vendas
- **Frequência:** Segundas-feiras às 9h
- **Cron:** `0 9 * * 1`
- **Customização:** Edite o trigger "Relatório Semanal"

### Lembretes de Agendamento
- **Frequência:** Diariamente às 10h
- **Cron:** `0 10 * * *`
- **Customização:** Edite o trigger "Lembretes Diários"

## 🔄 Integração com MCP Server

### Comandos no Claude que disparam n8n:
```
"Crie um contato no GHL" → MCP Server → API GHL → Webhook → n8n
"Agende uma reunião" → MCP Server → API GHL → Webhook → n8n
"Mude o estágio da oportunidade" → MCP Server → API GHL → Webhook → n8n
```

### Fluxo Completo:
1. **Claude** (via MCP) faz ação no GHL
2. **GoHighLevel** dispara webhook
3. **n8n** recebe webhook e executa automação
4. **n8n** envia notificações e executa ações adicionais

## 🚨 Solução de Problemas

### Webhook não está funcionando
1. **Verifique a URL do webhook no n8n**
2. **Confirme se o workflow está ativo**
3. **Teste manualmente enviando POST para a URL**

### Credenciais inválidas
1. **Verifique se a API Key do GHL está correta**
2. **Confirme se tem as permissões necessárias**
3. **Teste a API diretamente**

### Slack não recebe notificações
1. **Verifique as credenciais do Slack**
2. **Confirme se o bot tem permissão no canal**
3. **Teste enviando mensagem manual**

## 📈 Monitoramento

### Logs de Execução
- Acesse **Executions** no n8n para ver logs detalhados
- Monitore falhas e sucessos
- Configure alertas para falhas

### Métricas Importantes
- Taxa de sucesso dos webhooks
- Tempo de resposta das automações
- Volume de mensagens enviadas

## 🔧 Manutenção

### Atualizações Regulares
1. **Revisar mensagens** - Manter relevantes e atualizadas
2. **Verificar webhooks** - Garantir que estão funcionando
3. **Monitorar logs** - Identificar e corrigir erros
4. **Testar integrações** - Validar funcionamento completo

### Backup
- Exporte regularmente os workflows
- Mantenha backup das credenciais
- Documente customizações específicas

---

## 🎉 Pronto para Usar!

Com esses workflows configurados, você terá:
- ✅ Automação completa de contatos
- ✅ Gestão inteligente de oportunidades
- ✅ Confirmações automáticas de agendamentos
- ✅ Relatórios e notificações em tempo real
- ✅ Integração perfeita com Claude via MCP

**🚀 Potencialize seu GoHighLevel com automação de força total!**