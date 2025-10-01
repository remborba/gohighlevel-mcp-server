# 🤖 Configuração do Telegram Bot para n8n

## 📋 Pré-requisitos
- Conta no Telegram
- Acesso ao n8n
- Bot do Telegram criado via @BotFather

## 🚀 Passo a Passo

### 1. Criar Bot no Telegram
1. Abra o Telegram e procure por `@BotFather`
2. Envie `/newbot`
3. Escolha um nome: **GHL Automação Bot**
4. Escolha um username: **ghl_automacao_bot** (ou similar)
5. Guarde o **TOKEN** fornecido (ex: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Obter Chat ID
1. Envie uma mensagem para seu bot
2. Acesse: `https://api.telegram.org/bot[SEU_TOKEN]/getUpdates`
3. Procure por `"id":` na resposta - esse é seu Chat ID

### 3. Configurar Credenciais no n8n

#### Telegram Bot API:
- **Credential Type**: Telegram API
- **Access Token**: `SEU_TOKEN_DO_BOT`

### 4. Configurar Variáveis de Ambiente

No n8n, adicione a variável:
- **Nome**: `TELEGRAM_CHAT_ID`
- **Valor**: `SEU_CHAT_ID`

### 5. Importar Workflows

Importe os 3 workflows Telegram:
1. `ghl-contact-management.json` → **GoHighLevel - Gestão de Contatos (Telegram)**
2. `ghl-opportunity-pipeline.json` → **GoHighLevel - Pipeline de Oportunidades (Telegram)**
3. `ghl-appointment-automation.json` → **GoHighLevel - Automação de Agendamentos (Telegram)**

**Nota**: Todos os workflows foram totalmente convertidos para usar Telegram em vez de Slack.

### 6. Configurar Webhooks no GoHighLevel

Vá em Settings → Integrations → Webhooks e configure:

#### Para Contatos:
- **URL**: `https://SEU_N8N.com/webhook/ghl-webhook-contact`
- **Events**: Contact Create, Contact Update

#### Para Oportunidades:
- **URL**: `https://SEU_N8N.com/webhook/ghl-opportunity-webhook`
- **Events**: Opportunity Stage Update

#### Para Agendamentos:
- **URL**: `https://SEU_N8N.com/webhook/ghl-appointment-webhook`
- **Events**: Appointment Create, Appointment Update

## ✅ Teste
1. Crie um contato no GHL
2. Verifique se recebeu notificação no Telegram
3. Se não funcionar, verifique logs do n8n

## 🔧 Troubleshooting

### Bot não responde:
- Verifique se o token está correto
- Confirme se o Chat ID está certo

### Webhooks não disparam:
- Teste a URL do webhook no browser
- Verifique se os workflows estão ativos no n8n

### Formatação estranha:
- Confirme que `parse_mode: "Markdown"` está configurado