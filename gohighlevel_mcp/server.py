"""GoHighLevel MCP Server implementation."""

import asyncio
import json
import os
from typing import Any

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx

# Load environment variables
load_dotenv()

app = Server("gohighlevel-mcp")

# Initialize HTTP client
http_client = None

async def initialize_client():
    """Initialize the HTTP client for GoHighLevel API."""
    global http_client
    
    api_key = os.getenv("GHL_API_KEY")
    location_id = os.getenv("GHL_LOCATION_ID")
    
    if not api_key or not location_id:
        raise ValueError("GHL_API_KEY and GHL_LOCATION_ID must be set in environment variables")
    
    http_client = httpx.AsyncClient(
        base_url="https://services.leadconnectorhq.com",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Version": "2021-07-28"
        },
        timeout=30.0
    )

@app.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="ghl_get_contacts",
            description="Get contacts from GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of contacts to return (default: 10)",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="ghl_create_contact",
            description="Create a new contact in GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "firstName": {"type": "string", "description": "First name"},
                    "lastName": {"type": "string", "description": "Last name"},
                    "email": {"type": "string", "description": "Email address"},
                    "phone": {"type": "string", "description": "Phone number"}
                },
                "required": ["firstName"]
            }
        ),
        Tool(
            name="ghl_send_sms",
            description="Send SMS message to a contact in GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "contactId": {"type": "string", "description": "Contact ID to send SMS to"},
                    "message": {"type": "string", "description": "SMS message content"}
                },
                "required": ["contactId", "message"]
            }
        ),
        Tool(
            name="ghl_get_conversations",
            description="Get conversations from GoHighLevel",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of conversations to return (default: 10)",
                        "default": 10
                    }
                }
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if not http_client:
        await initialize_client()
    
    if name == "ghl_get_contacts":
        return await get_contacts(arguments)
    elif name == "ghl_create_contact":
        return await create_contact(arguments)
    elif name == "ghl_send_sms":
        return await send_sms(arguments)
    elif name == "ghl_get_conversations":
        return await get_conversations(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")

async def get_contacts(args: dict) -> list[TextContent]:
    """Get contacts from GoHighLevel."""
    limit = args.get("limit", 10)
    location_id = os.getenv("GHL_LOCATION_ID")
    
    params = {
        "locationId": location_id,
        "limit": str(limit)
    }
    
    try:
        response = await http_client.get("/contacts/", params=params)
        response.raise_for_status()
        
        data = response.json()
        contacts = data.get("contacts", [])
        
        result = {
            "total_contacts": len(contacts),
            "contacts": contacts[:limit]
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao buscar contatos: {str(e)}")]

async def create_contact(args: dict) -> list[TextContent]:
    """Create a new contact in GoHighLevel."""
    location_id = os.getenv("GHL_LOCATION_ID")
    
    contact_data = {
        "locationId": location_id,
        **args
    }
    
    try:
        response = await http_client.post("/contacts/", json=contact_data)
        response.raise_for_status()
        
        result = response.json()
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao criar contato: {str(e)}")]

async def send_sms(args: dict) -> list[TextContent]:
    """Send SMS message to a contact in GoHighLevel."""
    contact_id = args.get("contactId")
    message = args.get("message")
    
    if not contact_id or not message:
        return [TextContent(type="text", text="Erro: contactId e message são obrigatórios")]
    
    # Primeira tentativa: endpoint direto
    message_data = {
        "type": "SMS",
        "contactId": contact_id,
        "message": message,
        "locationId": os.getenv("GHL_LOCATION_ID")
    }
    
    try:
        response = await http_client.post("/conversations/messages", json=message_data)
        response.raise_for_status()
        
        result = response.json()
        success_msg = f"✅ SMS enviado com sucesso!\n\nPara: {contact_id}\nMensagem: {message}\n\nResposta: {json.dumps(result, indent=2)}"
        return [TextContent(type="text", text=success_msg)]
    
    except Exception as e:
        # Segunda tentativa: criar conversa primeiro
        try:
            conversation_data = {
                "contactId": contact_id,
                "locationId": os.getenv("GHL_LOCATION_ID")
            }
            
            conv_response = await http_client.post("/conversations", json=conversation_data)
            conv_result = conv_response.json()
            
            if "conversation" in conv_result:
                conv_id = conv_result["conversation"]["id"]
                
                msg_data = {
                    "type": "SMS",
                    "message": message,
                    "conversationId": conv_id
                }
                
                msg_response = await http_client.post("/conversations/messages", json=msg_data)
                msg_response.raise_for_status()
                
                msg_result = msg_response.json()
                success_msg = f"✅ SMS enviado com sucesso!\n\nConversa criada: {conv_id}\nMensagem: {message}\n\nResposta: {json.dumps(msg_result, indent=2)}"
                return [TextContent(type="text", text=success_msg)]
            
        except Exception as e2:
            error_msg = f"❌ Erro ao enviar SMS: {str(e)}\n\nTentativa alternativa: {str(e2)}"
            return [TextContent(type="text", text=error_msg)]

async def get_conversations(args: dict) -> list[TextContent]:
    """Get conversations from GoHighLevel."""
    limit = args.get("limit", 10)
    location_id = os.getenv("GHL_LOCATION_ID")
    
    params = {
        "locationId": location_id,
        "limit": str(limit)
    }
    
    try:
        response = await http_client.get(f"/locations/{location_id}/conversations", params={"limit": str(limit)})
        response.raise_for_status()
        
        data = response.json()
        conversations = data.get("conversations", [])
        
        result = {
            "total_conversations": len(conversations),
            "conversations": conversations[:limit]
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao buscar conversas: {str(e)}")]

async def main():
    """Main entry point for the MCP server."""
    await initialize_client()
    
    async with stdio_server() as (read_stream, write_stream):
        from mcp.server.models import InitializationOptions
        from mcp.types import ServerCapabilities
        await app.run(read_stream, write_stream, InitializationOptions(
            server_name="gohighlevel-mcp",
            server_version="1.0.0",
            capabilities=ServerCapabilities(
                tools={}
            )
        ))

if __name__ == "__main__":
    asyncio.run(main())