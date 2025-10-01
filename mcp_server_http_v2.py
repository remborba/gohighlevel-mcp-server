#!/usr/bin/env python3
"""
Servidor HTTP para expor funções MCP do GoHighLevel para n8n
VERSÃO COM SUPORTE A CREDENCIAIS DINÂMICAS
"""

import asyncio
import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import httpx

app = FastAPI(title="GoHighLevel MCP Server", version="2.0.0")

# Configurar CORS para n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Credentials(BaseModel):
    apiKey: str
    locationId: str

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any] = {}
    credentials: Optional[Credentials] = None  # Credenciais opcionais

# Credenciais padrão do .env (fallback)
DEFAULT_API_KEY = os.getenv("GHL_API_KEY", "")
DEFAULT_LOCATION_ID = os.getenv("GHL_LOCATION_ID", "")
GHL_BASE_URL = "https://services.leadconnectorhq.com"

# Métodos disponíveis
AVAILABLE_METHODS = [
    "get_contacts",
    "create_contact",
    "send_sms",
    "get_conversations",
    "create_opportunity",
    "get_opportunities",
    "get_pipelines",
]

async def make_ghl_request(method: str, endpoint: str, api_key: str, location_id: str, data: dict = None):
    """Faz requisição ao GoHighLevel"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    url = f"{GHL_BASE_URL}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        if method == "GET":
            params = {"locationId": location_id, **data} if data else {"locationId": location_id}
            response = await client.get(url, headers=headers, params=params)
        else:  # POST
            payload = {"locationId": location_id, **data} if data else {"locationId": location_id}
            response = await client.post(url, headers=headers, json=payload)
    
    response.raise_for_status()
    return response.json()

@app.get("/")
async def root():
    return {
        "message": "GoHighLevel MCP Server v2.0 - Suporta credenciais dinâmicas",
        "available_methods": AVAILABLE_METHODS,
        "usage": {
            "endpoint": "POST /mcp",
            "body": {
                "method": "method_name",
                "credentials": {
                    "apiKey": "seu_token_ghl",
                    "locationId": "seu_location_id"
                },
                "params": {}
            },
            "note": "Credentials são opcionais. Se não fornecidas, usa credenciais padrão do servidor."
        }
    }

@app.get("/methods")
async def list_methods():
    """Lista todos os métodos disponíveis"""
    return {
        "methods": AVAILABLE_METHODS,
        "examples": {
            "get_contacts": {
                "method": "get_contacts",
                "credentials": {
                    "apiKey": "seu_token",
                    "locationId": "seu_location_id"
                },
                "params": {"limit": 10}
            },
            "create_contact": {
                "method": "create_contact",
                "credentials": {
                    "apiKey": "seu_token",
                    "locationId": "seu_location_id"
                },
                "params": {
                    "firstName": "João",
                    "email": "joao@email.com",
                    "phone": "+5511999999999"
                }
            }
        }
    }

@app.post("/mcp")
async def call_mcp_method(request: MCPRequest):
    """Chama uma função MCP com credenciais dinâmicas"""
    
    if request.method not in AVAILABLE_METHODS:
        raise HTTPException(
            status_code=400,
            detail=f"Método '{request.method}' não disponível. Métodos: {AVAILABLE_METHODS}"
        )
    
    # Usar credenciais fornecidas ou padrão
    api_key = request.credentials.apiKey if request.credentials else DEFAULT_API_KEY
    location_id = request.credentials.locationId if request.credentials else DEFAULT_LOCATION_ID
    
    if not api_key or not location_id:
        raise HTTPException(
            status_code=400,
            detail="Credenciais não fornecidas e não há credenciais padrão configuradas"
        )
    
    try:
        # Processar cada método
        if request.method == "get_contacts":
            limit = request.params.get("limit", 10)
            result = await make_ghl_request(
                "GET",
                "/contacts/",
                api_key,
                location_id,
                {"limit": limit}
            )
            
        elif request.method == "create_contact":
            result = await make_ghl_request(
                "POST",
                "/contacts/",
                api_key,
                location_id,
                request.params
            )
            
        elif request.method == "send_sms":
            contact_id = request.params.get("contactId")
            message = request.params.get("message")
            result = await make_ghl_request(
                "POST",
                f"/conversations/messages",
                api_key,
                location_id,
                {
                    "type": "SMS",
                    "contactId": contact_id,
                    "message": message
                }
            )
            
        elif request.method == "get_conversations":
            limit = request.params.get("limit", 10)
            result = await make_ghl_request(
                "GET",
                "/conversations/",
                api_key,
                location_id,
                {"limit": limit}
            )
            
        elif request.method == "get_opportunities":
            result = await make_ghl_request(
                "GET",
                "/opportunities/search",
                api_key,
                location_id,
                request.params
            )
            
        elif request.method == "get_pipelines":
            result = await make_ghl_request(
                "GET",
                "/opportunities/pipelines",
                api_key,
                location_id,
                {}
            )
            
        else:
            raise HTTPException(status_code=400, detail=f"Método {request.method} ainda não implementado")
        
        return {
            "success": True,
            "method": request.method,
            "data": result
        }
        
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erro na API do GHL: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao executar método '{request.method}': {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando GoHighLevel MCP Server v2.0")
    print("✅ Suporte a credenciais dinâmicas ativado")
    print("📍 Acesse: http://localhost:3000")
    print("📋 Métodos: http://localhost:3000/methods")
    uvicorn.run(app, host="0.0.0.0", port=3000)
