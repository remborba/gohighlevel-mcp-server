# 🤖 Setup do Bot Telegram para Controlar GoHighLevel

## 📋 O que é?
Um bot Telegram que permite controlar o GoHighLevel através de comandos de texto. Você pode:
- Criar contatos
- Buscar contatos  
- Enviar SMS
- Ver conversas
- Usar comandos naturais como "criar contato João Silva"

## 🚀 Passo a Passo

### 1. Configurar Token do Bot
1. **Procure @BotFather no Telegram**
2. **Envie `/newbot`**
3. **Escolha nome**: GoHighLevel Control Bot
4. **Escolha username**: ghl_control_bot (ou similar)
5. **Copie o TOKEN** fornecido

### 2. Obter seu Chat ID
1. **Envie qualquer mensagem para seu bot**
2. **Acesse**: `https://api.telegram.org/bot[SEU_TOKEN]/getUpdates`
3. **Procure por `"id"`** na resposta - esse é seu Chat ID

### 3. Configurar .env
Edite o arquivo `.env` e adicione:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

### 4. Instalar Dependências
```bash
pip install python-telegram-bot>=20.7
```

### 5. Executar o Bot
```bash
python telegram_bot.py
```

## 💬 Comandos Disponíveis

### 📋 Contatos
```
/criar_contato João Silva joao@email.com 11999999999
/buscar_contatos 5
```

### 📱 SMS  
```
/enviar_sms abc123 "Olá! Como posso ajudar?"
```

### 💬 Conversas
```
/listar_conversas 10
```

### 🗣️ Comandos Naturais
Você pode falar naturalmente:
```
"Criar contato Maria Santos"
"Buscar contatos"
"Ver conversas"
```

## 🔐 Segurança
- ✅ **Bot autorizado apenas para seu Chat ID**
- ✅ **Verificação de permissões em cada comando**
- ✅ **Conexão segura com GoHighLevel via MCP**

## 📱 Exemplo de Uso

1. **Criar contato:**
   ```
   /criar_contato João Silva joao@email.com 11999999999
   ```
   Bot responde: ✅ Contato criado com sucesso!

2. **Buscar contatos:**
   ```
   /buscar_contatos 3
   ```
   Bot lista os últimos 3 contatos

3. **Comando natural:**
   ```
   "criar contato Ana Paula"
   ```
   Bot cria o contato automaticamente

## 🚨 Troubleshooting

### Bot não responde:
- Verifique se o TOKEN está correto
- Confirme se o CHAT_ID está certo
- Verifique se o bot está rodando (`python telegram_bot.py`)

### Erro de autorização:
- Confirme que está enviando do chat correto
- Verifique se TELEGRAM_CHAT_ID está configurado

### Erro MCP/GoHighLevel:
- Verifique se GHL_API_KEY está válida
- Confirme se GHL_LOCATION_ID está correto
- Teste o MCP separadamente primeiro

## 🔄 Mantendo o Bot Rodando

### Opção 1: Screen (Linux/Mac)
```bash
screen -S telegram-bot
python telegram_bot.py
# Ctrl+A+D para sair
```

### Opção 2: nohup
```bash
nohup python telegram_bot.py &
```

### Opção 3: PM2 (Recomendado)
```bash
npm install -g pm2
pm2 start telegram_bot.py --name ghl-telegram-bot
pm2 save
pm2 startup
```

## 🎯 Próximos Passos
- ✅ Bot funcionando
- ✅ Comandos básicos configurados
- 🔄 Workflows n8n para notificações automáticas
- 🔄 Bot para controle manual

**Agora você tem controle total do GoHighLevel via Telegram!** 🚀