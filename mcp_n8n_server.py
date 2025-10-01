#!/usr/bin/env python3
"""
Servidor MCP otimizado para n8n com stdio
"""

import asyncio
import json
import sys
from mcp.server.stdio import stdio_server
from mcp.server import Server
from mcp.types import (
    Resource, 
    Tool,
    TextContent, 
    ImageContent, 
    EmbeddedResource
)

# Importar todas as funções MCP
from mcp_functions import (
    get_contacts, create_contact, send_sms, get_conversations,
    create_opportunity, create_opportunity_smart, create_opportunity_easy,
    get_opportunities, get_pipelines
)
from mcp_functions_new import create_opportunity_natural

# Criar servidor MCP
server = Server("gohighlevel-mcp")

# Registrar todas as ferramentas
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """Lista todas as ferramentas disponíveis"""
    return [
        Tool(
            name="get_contacts",
            description="Buscar contatos do GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "number", "description": "Número máximo de contatos", "default": 10}
                }
            }
        ),
        Tool(
            name="create_contact", 
            description="Criar novo contato no GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "firstName": {"type": "string", "description": "Nome"},
                    "lastName": {"type": "string", "description": "Sobrenome (opcional)"},
                    "email": {"type": "string", "description": "Email"},
                    "phone": {"type": "string", "description": "Telefone"}
                },
                "required": ["firstName"]
            }
        ),
        Tool(
            name="create_opportunity_natural",
            description="Criar oportunidade com linguagem natural",
            inputSchema={
                "type": "object", 
                "properties": {
                    "nome": {"type": "string", "description": "Nome do contato"},
                    "telefone": {"type": "string", "description": "Telefone"},
                    "email": {"type": "string", "description": "Email"},
                    "pipeline_name": {"type": "string", "description": "Nome do pipeline", "enum": ["lead", "vendas", "padrão"]},
                    "stage_name": {"type": "string", "description": "Nome do estágio", "enum": ["new lead", "hot lead", "contacted", "proposal sent", "closed"]},
                    "valor": {"type": "number", "description": "Valor da oportunidade", "default": 0}
                },
                "required": ["nome"]
            }
        ),
        Tool(
            name="send_sms",
            description="Enviar SMS para contato",
            inputSchema={
                "type": "object",
                "properties": {
                    "contactId": {"type": "string", "description": "ID do contato"},
                    "message": {"type": "string", "description": "Mensagem SMS"}
                },
                "required": ["contactId", "message"]
            }
        ),
        Tool(
            name="get_opportunities",
            description="Buscar oportunidades",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {"type": "number", "description": "Limite de resultados", "default": 10}
                }
            }
        ),
        Tool(
            name="get_pipelines",
            description="Buscar pipelines disponíveis",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Executar ferramentas"""
    
    # Mapear nome da ferramenta para função
    tool_functions = {
        "get_contacts": get_contacts,
        "create_contact": create_contact,
        "create_opportunity_natural": create_opportunity_natural,
        "send_sms": send_sms,
        "get_opportunities": get_opportunities,
        "get_pipelines": get_pipelines
    }
    
    if name not in tool_functions:
        return [TextContent(type="text", text=f"Ferramenta '{name}' não encontrada")]
    
    try:
        # Chamar a função correspondente
        result = await tool_functions[name](arguments)
        return result
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao executar '{name}': {str(e)}")]

async def main():
    """Executar servidor stdio"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    print("🚀 Iniciando servidor MCP para n8n...", file=sys.stderr)
    asyncio.run(main())