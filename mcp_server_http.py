#!/usr/bin/env python3
"""
Servidor HTTP para expor funções MCP do GoHighLevel para n8n
"""

import asyncio
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

# Importar funções MCP
from mcp_functions import (
    get_contacts, create_contact, send_sms, get_conversations, 
    create_opportunity, create_opportunity_smart, create_opportunity_easy,
    get_opportunities, get_pipelines
)
from mcp_functions_new import create_opportunity_natural

app = FastAPI(title="GoHighLevel MCP Server", version="1.0.0")

# Configurar CORS para n8n
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MCPRequest(BaseModel):
    method: str
    params: Dict[str, Any] = {}

# Mapeamento de métodos disponíveis
AVAILABLE_METHODS = {
    "get_contacts": get_contacts,
    "create_contact": create_contact,
    "send_sms": send_sms,
    "get_conversations": get_conversations,
    "create_opportunity": create_opportunity,
    "create_opportunity_smart": create_opportunity_smart,
    "create_opportunity_easy": create_opportunity_easy,
    "create_opportunity_natural": create_opportunity_natural,
    "get_opportunities": get_opportunities,
    "get_pipelines": get_pipelines,
}

@app.get("/")
async def root():
    return {
        "message": "GoHighLevel MCP Server",
        "available_methods": list(AVAILABLE_METHODS.keys()),
        "usage": "POST /mcp with {'method': 'method_name', 'params': {...}}"
    }

@app.get("/methods")
async def list_methods():
    """Lista todos os métodos disponíveis"""
    return {
        "methods": list(AVAILABLE_METHODS.keys()),
        "examples": {
            "get_contacts": {"limit": 10},
            "create_contact": {"firstName": "João", "email": "joao@email.com", "phone": "+5511999999999"},
            "create_opportunity_natural": {
                "nome": "Maria Silva",
                "telefone": "11987654321", 
                "email": "maria@email.com",
                "pipeline_name": "lead",
                "stage_name": "new lead",
                "valor": 1500
            }
        }
    }

@app.post("/mcp")
async def call_mcp_method(request: MCPRequest):
    """Chama uma função MCP"""
    if request.method not in AVAILABLE_METHODS:
        raise HTTPException(
            status_code=400, 
            detail=f"Método '{request.method}' não disponível. Métodos disponíveis: {list(AVAILABLE_METHODS.keys())}"
        )
    
    try:
        # Chamar a função MCP
        mcp_function = AVAILABLE_METHODS[request.method]
        result = await mcp_function(request.params)
        
        # Extrair o texto do resultado
        if result and hasattr(result[0], 'text'):
            response_text = result[0].text
            
            # Tentar fazer parse JSON se possível
            try:
                parsed_result = json.loads(response_text)
                return {
                    "success": True,
                    "method": request.method,
                    "data": parsed_result
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "method": request.method,
                    "data": response_text
                }
        else:
            return {
                "success": True,
                "method": request.method,
                "data": "Operação completada"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao executar método '{request.method}': {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor MCP para n8n...")
    print("📍 Acesse: http://localhost:3000")
    print("📋 Métodos: http://localhost:3000/methods")
    uvicorn.run(app, host="0.0.0.0", port=3000)