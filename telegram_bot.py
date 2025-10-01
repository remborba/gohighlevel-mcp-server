"""Telegram Bot para controlar GoHighLevel via MCP."""

import asyncio
import json
import os
import re
from typing import Dict, Any, List
import logging

from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import httpx

# Importar as funções do MCP
from mcp_functions import get_contacts, create_contact, send_sms, get_conversations, create_opportunity, create_opportunity_smart, create_opportunity_easy, get_opportunities, get_pipelines
from mcp_functions_new import create_opportunity_natural

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AUTHORIZED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not AUTHORIZED_CHAT_ID:
    raise ValueError("TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID devem estar configurados no .env")

class TelegramMCPBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configurar handlers de comandos."""
        # Comandos básicos
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        
        # Comandos MCP - Contatos
        self.application.add_handler(CommandHandler("criar_contato", self.create_contact_command))
        self.application.add_handler(CommandHandler("buscar_contatos", self.get_contacts_command))
        
        # Comandos MCP - SMS
        self.application.add_handler(CommandHandler("enviar_sms", self.send_sms_command))
        
        # Comandos MCP - Conversas
        self.application.add_handler(CommandHandler("listar_conversas", self.get_conversations_command))
        
        # Comandos MCP - Oportunidades
        self.application.add_handler(CommandHandler("venda", self.create_opportunity_easy_command))
        self.application.add_handler(CommandHandler("nova_oportunidade", self.create_opportunity_smart_command))
        self.application.add_handler(CommandHandler("criar_oportunidade", self.create_opportunity_command))
        self.application.add_handler(CommandHandler("buscar_oportunidades", self.get_opportunities_command))
        self.application.add_handler(CommandHandler("listar_pipelines", self.get_pipelines_command))
        
        # Handler para mensagens de texto livre (comandos naturais)
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text_message))
    
    async def is_authorized(self, update: Update) -> bool:
        """Verificar se o usuário está autorizado."""
        chat_id = str(update.effective_chat.id)
        if chat_id != AUTHORIZED_CHAT_ID:
            await update.message.reply_text("❌ Acesso negado. Bot não autorizado para este chat.")
            return False
        return True
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start."""
        if not await self.is_authorized(update):
            return
            
        welcome_msg = """
🤖 **Bot GoHighLevel MCP Ativo!**

Comandos disponíveis:

**📋 Contatos:**
• `/criar_contato Nome Email Telefone` - Criar novo contato
• `/buscar_contatos [limite]` - Listar contatos

**📱 SMS:**
• `/enviar_sms ID_CONTATO "mensagem"` - Enviar SMS

**💬 Conversas:**
• `/listar_conversas [limite]` - Listar conversas

**💰 Oportunidades:**
• `/venda` - Criar venda (SUPER fácil)
• `/nova_oportunidade` - Criar oportunidade (modo fácil) 
• `/criar_oportunidade` - Criar oportunidade (modo avançado)
• `/buscar_oportunidades [limite]` - Listar oportunidades
• `/listar_pipelines` - Ver pipelines e estágios

**📚 Ajuda:**
• `/help` - Ver todos os comandos

**💡 Dica:** Você também pode enviar mensagens naturais como:
"Criar contato João Silva" ou "Buscar últimos 10 contatos"
        """
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help."""
        if not await self.is_authorized(update):
            return
            
        help_msg = """
🆘 **Ajuda - Bot GoHighLevel MCP**

**📋 Gerenciar Contatos:**
```
/criar_contato João Silva joao@email.com 11999999999
/buscar_contatos 5
```

**📱 Enviar SMS:**
```
/enviar_sms abc123 "Olá! Como posso ajudar?"
```

**💬 Ver Conversas:**
```
/listar_conversas 10
```

**🗣️ Comandos Naturais:**
Você pode falar naturalmente:
• "Criar contato Maria Santos"
• "Buscar contatos"
• "Enviar SMS para João"
• "Ver conversas"

**⚡ Status:** Conectado ao GoHighLevel via MCP
        """
        await update.message.reply_text(help_msg, parse_mode='Markdown')
    
    async def create_contact_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /criar_contato."""
        if not await self.is_authorized(update):
            return
        
        if len(context.args) < 1:
            await update.message.reply_text(
                "❌ **Uso:** `/criar_contato Nome [Email] [Telefone]`\n\n"
                "**Exemplo:** `/criar_contato João Silva joao@email.com 11999999999`",
                parse_mode='Markdown'
            )
            return
        
        # Parsing argumentos
        args = context.args
        firstName = args[0]
        lastName = args[1] if len(args) > 1 and '@' not in args[1] else ""
        email = None
        phone = None
        
        for arg in args[1:]:
            if '@' in arg:
                email = arg
            elif arg.replace('+', '').replace('-', '').replace(' ', '').isdigit():
                phone = arg
            elif not lastName:
                lastName = arg
        
        # Criar contato via MCP
        try:
            contact_data = {"firstName": firstName}
            if lastName:
                contact_data["lastName"] = lastName
            if email:
                contact_data["email"] = email
            if phone:
                contact_data["phone"] = phone
            
            await update.message.reply_text("⏳ Criando contato...")
            
            result = await create_contact(contact_data)
            result_text = result[0].text
            
            await update.message.reply_text(
                f"✅ **Contato criado com sucesso!**\n\n{result_text}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao criar contato: {str(e)}")
    
    async def get_contacts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /buscar_contatos."""
        if not await self.is_authorized(update):
            return
        
        limit = 5  # default
        if context.args and context.args[0].isdigit():
            limit = int(context.args[0])
            limit = min(limit, 20)  # máximo 20
        
        try:
            await update.message.reply_text("⏳ Buscando contatos...")
            
            result = await get_contacts({"limit": limit})
            result_text = result[0].text
            
            await update.message.reply_text(
                f"📋 **Contatos encontrados:**\n\n```json\n{result_text}\n```",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao buscar contatos: {str(e)}")
    
    async def send_sms_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /enviar_sms."""
        if not await self.is_authorized(update):
            return
        
        if len(context.args) < 2:
            await update.message.reply_text(
                "❌ **Uso:** `/enviar_sms ID_CONTATO \"mensagem\"`\n\n"
                "**Exemplo:** `/enviar_sms abc123 \"Olá! Como posso ajudar?\"`",
                parse_mode='Markdown'
            )
            return
        
        contact_id = context.args[0]
        message = ' '.join(context.args[1:]).strip('"\'')
        
        try:
            await update.message.reply_text("⏳ Enviando SMS...")
            
            result = await send_sms({"contactId": contact_id, "message": message})
            result_text = result[0].text
            
            await update.message.reply_text(
                f"📱 **SMS enviado!**\n\n{result_text}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao enviar SMS: {str(e)}")
    
    async def get_conversations_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /listar_conversas."""
        if not await self.is_authorized(update):
            return
        
        limit = 5  # default
        if context.args and context.args[0].isdigit():
            limit = int(context.args[0])
            limit = min(limit, 20)  # máximo 20
        
        try:
            await update.message.reply_text("⏳ Buscando conversas...")
            
            result = await get_conversations({"limit": limit})
            result_text = result[0].text
            
            await update.message.reply_text(
                f"💬 **Conversas encontradas:**\n\n```json\n{result_text}\n```",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao buscar conversas: {str(e)}")
    
    async def create_opportunity_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /criar_oportunidade - Formato natural simples."""
        if not await self.is_authorized(update):
            return
        
        help_msg = """
💰 **Criar Oportunidade (Formato Simples)**

**Use assim:**
`/criar_oportunidade Nome Telefone Email Pipeline Stage [Valor]`

**Exemplos:**
```
/criar_oportunidade "João Silva" 11999999999 joao@email.com lead "new lead" 2500
/criar_oportunidade "Maria Santos" 11888888888 maria@teste.com vendas inicial 1800
/criar_oportunidade "Carlos Costa" 11777777777 "" padrão contato
```

**Pipelines:** vendas, leads, principal, padrão
**Estágios:** inicial, lead, "new lead", contato, interessado, qualificado, proposta, negociação

**💡 Valor é opcional! Use aspas se o estágio tem espaços.**
        """
        
        if len(context.args) < 3:
            await update.message.reply_text(help_msg, parse_mode='Markdown')
            return
        
        try:
            # Parsing SIMPLES e DIRETO por posição
            args = [arg.strip('"\'') for arg in context.args]
            
            # Formato fixo: Nome [Sobrenome] Telefone Email Pipeline Stage [Valor]
            if len(args) < 4:
                await update.message.reply_text("❌ Mínimo: Nome Telefone Email Pipeline")
                return
            
            # Identificar campos por posição e tipo
            nome_parts = []
            telefone = ""
            email = ""
            pipeline_name = "lead"
            stage_name = "new lead"
            valor = 0
            
            i = 0
            # 1. Nome (pode ser várias palavras até encontrar telefone)
            while i < len(args):
                arg = args[i]
                # Se é um número (telefone), para de adicionar ao nome
                if arg.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "").isdigit() and len(arg.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")) >= 8:
                    telefone = arg
                    i += 1
                    break
                else:
                    nome_parts.append(arg)
                    i += 1
            
            nome = " ".join(nome_parts)
            
            # 2. Email (próximo item que contém @)
            while i < len(args):
                if "@" in args[i] and "." in args[i]:
                    email = args[i]
                    i += 1
                    break
                i += 1
            
            # 3. Pipeline (próximo item)
            if i < len(args):
                pipeline_name = args[i].lower()
                i += 1
            
            # 4. Stage e Valor (processar o resto)
            remaining_args = args[i:]
            stage_parts = []
            
            # Verificar se o último argumento é um valor
            if remaining_args and remaining_args[-1].replace(",", "").replace(".", "").isdigit():
                try:
                    valor = float(remaining_args[-1].replace(",", "."))
                    stage_parts = remaining_args[:-1]  # Todos exceto o último
                except ValueError:
                    stage_parts = remaining_args
            else:
                stage_parts = remaining_args
            
            if stage_parts:
                stage_name = " ".join(stage_parts).lower()
            
            # Limpar e mapear pipeline
            if pipeline_name in ["leal", "lead", "leads"]:
                pipeline_name = "lead"
            elif pipeline_name in ["vendas", "sales"]:
                pipeline_name = "vendas"
            
            # Sempre permitir criação de novos contatos e oportunidades
            opportunity_data = {
                "nome": nome,
                "telefone": telefone,
                "email": email,
                "pipeline_name": pipeline_name,
                "stage_name": stage_name,
                "valor": valor,
                "force_new": True  # Forçar criação de novo contato se necessário
            }
            
            await update.message.reply_text("⏳ Criando oportunidade...")
            
            result = await create_opportunity_natural(opportunity_data)
            result_text = result[0].text
            
            await update.message.reply_text(
                f"🎉 **Oportunidade criada!**\n\n{result_text}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao criar oportunidade: {str(e)}")
    
    async def create_opportunity_easy_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /venda (SUPER fácil)."""
        if not await self.is_authorized(update):
            return
        
        help_msg = """
💰 **Criar Venda (SUPER FÁCIL)**

**Formato mais simples:**
`/venda "Título da Venda" "Nome do Cliente" [valor]`

**Exemplos:**
```
/venda "Venda Produto X" "João Silva" 2500
/venda "Consultoria" "Maria Santos" 1800
/venda "Serviço Premium" "Carlos Oliveira"
```

**🎯 O bot faz TUDO automaticamente:**
• ✅ Busca cliente existente ou cria novo
• ✅ Usa pipeline padrão (que você já tem)
• ✅ Coloca no estágio inicial
• ✅ Cria a oportunidade

**💡 Só precisa do título e nome do cliente!**
        """
        
        if len(context.args) < 2:
            await update.message.reply_text(help_msg, parse_mode='Markdown')
            return
        
        try:
            title = context.args[0].strip('"\'')
            contact_name = context.args[1].strip('"\'')
            value = float(context.args[2]) if len(context.args) > 2 else 0
            
            opportunity_data = {
                "title": title,
                "contact_name": contact_name,
                "value": value
            }
            
            await update.message.reply_text("⏳ Criando venda (modo super fácil)...")
            
            result = await create_opportunity_easy(opportunity_data)
            result_text = result[0].text
            
            await update.message.reply_text(
                f"🎉 **Venda criada!**\n\n{result_text}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao criar venda: {str(e)}")
    
    async def create_opportunity_smart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /nova_oportunidade (modo fácil)."""
        if not await self.is_authorized(update):
            return
        
        help_msg = """
💰 **Nova Oportunidade (Modo Fácil)**

**Formato:**
`/nova_oportunidade "Título" "Nome do Contato" [email] [telefone] PIPELINE_ID STAGE_ID [valor]`

**Exemplos:**
```
/nova_oportunidade "Venda João" "João Silva" joao@email.com 11999999999 Pipeline_SjYJh6QYcw6bdK6poVnL Stage_b63276fd-6525-42ba-a575-156cd8a5bdfe 2500
```

**Ou para contato existente:**
```
/nova_oportunidade "Venda Maria" "Maria Santos" "" "" Pipeline_SjYJh6QYcw6bdK6poVnL Stage_b63276fd-6525-42ba-a575-156cd8a5bdfe 1800
```

**💡 O bot vai:**
• Buscar contato existente por nome
• Criar novo contato se não encontrar
• Criar a oportunidade automaticamente
        """
        
        if len(context.args) < 4:
            await update.message.reply_text(help_msg, parse_mode='Markdown')
            return
        
        try:
            title = context.args[0].strip('"\'')
            contact_name = context.args[1].strip('"\'')
            contact_email = context.args[2] if len(context.args) > 2 and context.args[2] != '""' else None
            contact_phone = context.args[3] if len(context.args) > 3 and context.args[3] != '""' else None
            pipeline_id = context.args[4] if len(context.args) > 4 else None
            stage_id = context.args[5] if len(context.args) > 5 else None
            value = float(context.args[6]) if len(context.args) > 6 else 0
            
            opportunity_data = {
                "title": title,
                "contact_name": contact_name,
                "contact_email": contact_email,
                "contact_phone": contact_phone,
                "pipeline_id": pipeline_id,
                "stage_id": stage_id,
                "value": value
            }
            
            await update.message.reply_text("⏳ Criando oportunidade (modo inteligente)...")
            
            result = await create_opportunity_smart(opportunity_data)
            result_text = result[0].text
            
            await update.message.reply_text(
                f"💰 **Oportunidade criada!**\n\n{result_text}",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao criar oportunidade: {str(e)}")
    
    async def get_opportunities_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /buscar_oportunidades."""
        if not await self.is_authorized(update):
            return
        
        limit = 5  # default
        if context.args and context.args[0].isdigit():
            limit = int(context.args[0])
            limit = min(limit, 20)  # máximo 20
        
        try:
            await update.message.reply_text("⏳ Buscando oportunidades...")
            
            result = await get_opportunities({"limit": limit})
            result_text = result[0].text
            
            await update.message.reply_text(
                f"💰 **Oportunidades encontradas:**\n\n```json\n{result_text}\n```",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao buscar oportunidades: {str(e)}")
    
    async def get_pipelines_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /listar_pipelines."""
        if not await self.is_authorized(update):
            return
        
        try:
            await update.message.reply_text("⏳ Buscando pipelines...")
            
            result = await get_pipelines({})
            result_text = result[0].text
            
            await update.message.reply_text(
                f"🔄 **Pipelines e Estágios:**\n\n```json\n{result_text}\n```",
                parse_mode='Markdown'
            )
            
        except Exception as e:
            await update.message.reply_text(f"❌ Erro ao buscar pipelines: {str(e)}")
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para mensagens de texto livre (comandos naturais)."""
        if not await self.is_authorized(update):
            return
        
        text = update.message.text.lower()
        
        # Comandos naturais para criar contato
        if any(keyword in text for keyword in ['criar contato', 'novo contato', 'adicionar contato']):
            # Extrair nome do texto
            name_match = re.search(r'contato\s+([a-záêôção\s]+)', text, re.IGNORECASE)
            if name_match:
                name = name_match.group(1).strip()
                await update.message.reply_text(f"⏳ Criando contato: {name}")
                try:
                    result = await create_contact({"firstName": name})
                    result_text = result[0].text
                    await update.message.reply_text(f"✅ Contato criado!\n\n{result_text}")
                except Exception as e:
                    await update.message.reply_text(f"❌ Erro: {str(e)}")
            else:
                await update.message.reply_text("❌ Nome não identificado. Use: 'criar contato Nome Sobrenome'")
        
        # Comandos naturais para buscar contatos
        elif any(keyword in text for keyword in ['buscar contatos', 'listar contatos', 'ver contatos']):
            try:
                await update.message.reply_text("⏳ Buscando contatos...")
                result = await get_contacts({"limit": 5})
                result_text = result[0].text
                await update.message.reply_text(f"📋 Contatos:\n\n```json\n{result_text}\n```", parse_mode='Markdown')
            except Exception as e:
                await update.message.reply_text(f"❌ Erro: {str(e)}")
        
        # Comandos naturais para conversas
        elif any(keyword in text for keyword in ['ver conversas', 'listar conversas', 'conversas']):
            try:
                await update.message.reply_text("⏳ Buscando conversas...")
                result = await get_conversations({"limit": 5})
                result_text = result[0].text
                await update.message.reply_text(f"💬 Conversas:\n\n```json\n{result_text}\n```", parse_mode='Markdown')
            except Exception as e:
                await update.message.reply_text(f"❌ Erro: {str(e)}")
        
        # Comandos naturais para oportunidades
        elif any(keyword in text for keyword in ['criar oportunidade', 'nova oportunidade', 'adicionar oportunidade']):
            await update.message.reply_text(
                "💰 Para criar oportunidade use:\n"
                "`/criar_oportunidade \"Título\" ID_CONTATO ID_PIPELINE ID_ESTAGIO [VALOR]`\n\n"
                "💡 Primeiro veja os pipelines: `/listar_pipelines`",
                parse_mode='Markdown'
            )
        
        elif any(keyword in text for keyword in ['buscar oportunidades', 'listar oportunidades', 'ver oportunidades', 'oportunidades']):
            try:
                await update.message.reply_text("⏳ Buscando oportunidades...")
                result = await get_opportunities({"limit": 5})
                result_text = result[0].text
                await update.message.reply_text(f"💰 Oportunidades:\n\n```json\n{result_text}\n```", parse_mode='Markdown')
            except Exception as e:
                await update.message.reply_text(f"❌ Erro: {str(e)}")
        
        elif any(keyword in text for keyword in ['ver pipelines', 'listar pipelines', 'pipelines']):
            try:
                await update.message.reply_text("⏳ Buscando pipelines...")
                result = await get_pipelines({})
                result_text = result[0].text
                await update.message.reply_text(f"🔄 Pipelines:\n\n```json\n{result_text}\n```", parse_mode='Markdown')
            except Exception as e:
                await update.message.reply_text(f"❌ Erro: {str(e)}")
        
        else:
            await update.message.reply_text(
                "🤔 Não entendi o comando. Use `/help` para ver os comandos disponíveis.\n\n"
                "💡 **Exemplos:**\n"
                "• 'criar contato João Silva'\n"
                "• 'buscar contatos'\n"
                "• 'ver conversas'\n"
                "• 'buscar oportunidades'\n"
                "• 'ver pipelines'"
            )
    
    async def setup_bot_commands(self):
        """Configurar menu de comandos do bot."""
        commands = [
            BotCommand("start", "Iniciar bot"),
            BotCommand("help", "Ver ajuda"),
            BotCommand("criar_contato", "Criar novo contato"),
            BotCommand("buscar_contatos", "Listar contatos"),
            BotCommand("enviar_sms", "Enviar SMS"),
            BotCommand("listar_conversas", "Ver conversas"),
            BotCommand("venda", "Criar venda (SUPER fácil)"),
            BotCommand("nova_oportunidade", "Nova oportunidade (fácil)"),
            BotCommand("criar_oportunidade", "Criar oportunidade (avançado)"),
            BotCommand("buscar_oportunidades", "Listar oportunidades"),
            BotCommand("listar_pipelines", "Ver pipelines"),
        ]
        await self.application.bot.set_my_commands(commands)
    
    async def run(self):
        """Executar o bot."""
        logger.info("🤖 Iniciando Telegram Bot para GoHighLevel MCP...")
        
        # Configurar comandos do bot
        await self.setup_bot_commands()
        
        # Iniciar bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("✅ Bot está rodando! Pressione Ctrl+C para parar.")
        
        try:
            # Manter o bot rodando
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("⏹️ Parando bot...")
        finally:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

async def main():
    """Função principal."""
    bot = TelegramMCPBot()
    await bot.run()

if __name__ == "__main__":
    asyncio.run(main())