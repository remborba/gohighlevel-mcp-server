"""Funções MCP para serem usadas pelo bot Telegram."""

import asyncio
import json
import os
from typing import Any, Dict

from dotenv import load_dotenv
from mcp.types import TextContent
import httpx

# Load environment variables
load_dotenv()

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

async def get_contacts(args: dict) -> list[TextContent]:
    """Get contacts from GoHighLevel."""
    if not http_client:
        await initialize_client()
    
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
        
        # Formatar contatos de forma mais legível
        formatted_contacts = []
        for contact in contacts[:limit]:
            formatted_contact = {
                "id": contact.get("id"),
                "name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
                "email": contact.get("email"),
                "phone": contact.get("phone"),
                "tags": contact.get("tags", [])
            }
            formatted_contacts.append(formatted_contact)
        
        result = {
            "total_contacts": len(formatted_contacts),
            "contacts": formatted_contacts
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao buscar contatos: {str(e)}")]

async def create_contact(args: dict) -> list[TextContent]:
    """Create a new contact in GoHighLevel."""
    # Sempre inicializar cliente para garantir que está configurado
    await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    contact_data = {
        "locationId": location_id,
        **args
    }
    
    try:
        response = await http_client.post("/contacts/", json=contact_data)
        
        # Log para debug
        print(f"Create contact request: {contact_data}")
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        if response.status_code == 422:
            return [TextContent(type="text", text=f"❌ Erro 422: Dados inválidos. Verifique se todos os campos obrigatórios estão preenchidos. Response: {response.text}")]
        
        response.raise_for_status()
        
        # Verificar se a resposta tem conteúdo antes de fazer parse JSON
        if not response.text.strip():
            return [TextContent(type="text", text="❌ Resposta vazia da API do GoHighLevel")]
        
        result = response.json()
        
        # Formatar resposta de forma mais legível
        if "contact" in result:
            contact = result["contact"]
            formatted_result = {
                "success": True,
                "contact_id": contact.get("id"),
                "name": f"{contact.get('firstName', '')} {contact.get('lastName', '')}".strip(),
                "email": contact.get("email"),
                "phone": contact.get("phone"),
                "created_at": contact.get("dateAdded")
            }
        else:
            formatted_result = result
        
        return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao criar contato: {str(e)}")]

async def send_sms(args: dict) -> list[TextContent]:
    """Send SMS message to a contact in GoHighLevel."""
    if not http_client:
        await initialize_client()
    
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
        
        formatted_result = {
            "success": True,
            "contact_id": contact_id,
            "message": message,
            "sent_at": result.get("dateAdded"),
            "message_id": result.get("id")
        }
        
        return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
    
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
                
                formatted_result = {
                    "success": True,
                    "conversation_id": conv_id,
                    "contact_id": contact_id,
                    "message": message,
                    "message_id": msg_result.get("id")
                }
                
                return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
            
        except Exception as e2:
            error_msg = f"Erro ao enviar SMS: {str(e)}\nTentativa alternativa: {str(e2)}"
            return [TextContent(type="text", text=error_msg)]

async def get_conversations(args: dict) -> list[TextContent]:
    """Get conversations from GoHighLevel."""
    if not http_client:
        await initialize_client()
    
    limit = args.get("limit", 10)
    location_id = os.getenv("GHL_LOCATION_ID")
    
    try:
        response = await http_client.get(f"/locations/{location_id}/conversations", params={"limit": str(limit)})
        response.raise_for_status()
        
        data = response.json()
        conversations = data.get("conversations", [])
        
        # Formatar conversas de forma mais legível
        formatted_conversations = []
        for conv in conversations[:limit]:
            formatted_conv = {
                "id": conv.get("id"),
                "contact_id": conv.get("contactId"),
                "last_message": conv.get("lastMessageBody"),
                "last_message_date": conv.get("lastMessageDate"),
                "unread_count": conv.get("unreadCount", 0)
            }
            formatted_conversations.append(formatted_conv)
        
        result = {
            "total_conversations": len(formatted_conversations),
            "conversations": formatted_conversations
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao buscar conversas: {str(e)}")]

async def create_opportunity_smart(args: dict) -> list[TextContent]:
    """Create opportunity with smart contact and pipeline resolution."""
    if not http_client:
        await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    title = args.get("title")
    contact_name = args.get("contact_name")
    contact_email = args.get("contact_email")
    contact_phone = args.get("contact_phone") 
    contact_id = args.get("contact_id")
    pipeline_name = args.get("pipeline_name")
    pipeline_id = args.get("pipeline_id")
    stage_name = args.get("stage_name")
    stage_id = args.get("stage_id")
    value = args.get("value", 0)
    
    if not title:
        return [TextContent(type="text", text="❌ Título da oportunidade é obrigatório")]
    
    # 1. Resolver contato
    final_contact_id = contact_id
    
    if not final_contact_id and contact_name:
        # Buscar contato por nome
        contacts_result = await get_contacts({"limit": 50})
        contacts_data = json.loads(contacts_result[0].text)
        
        for contact in contacts_data.get("contacts", []):
            if contact_name.lower() in contact.get("name", "").lower():
                final_contact_id = contact.get("id")
                break
        
        # Se não encontrou, criar novo contato
        if not final_contact_id:
            new_contact_data = {"firstName": contact_name}
            if contact_email:
                new_contact_data["email"] = contact_email
            if contact_phone:
                new_contact_data["phone"] = contact_phone
                
            contact_result = await create_contact(new_contact_data)
            contact_response = json.loads(contact_result[0].text)
            final_contact_id = contact_response.get("contact_id")
    
    if not final_contact_id:
        return [TextContent(type="text", text="❌ Não foi possível resolver o contato. Use ID diretamente ou forneça nome/email")]
    
    # 2. Resolver pipeline e stage por nome ou ID
    final_pipeline_id = pipeline_id
    final_stage_id = stage_id
    
    # Se não tem IDs, buscar por nome
    if not final_pipeline_id or not final_stage_id:
        # Buscar oportunidades existentes para pegar IDs de exemplo
        try:
            opportunities_result = await get_opportunities({"limit": 20})
            opportunities_data = json.loads(opportunities_result[0].text)
            
            if opportunities_data.get("opportunities"):
                # Usar IDs de oportunidades existentes como padrão
                sample_opp = opportunities_data["opportunities"][0]
                final_pipeline_id = final_pipeline_id or sample_opp.get("pipeline_id") or sample_opp.get("pipelineId")
                final_stage_id = final_stage_id or sample_opp.get("stage") or sample_opp.get("pipelineStageId")
        except:
            pass
    
    # Se ainda não tem IDs, usar valores padrão que podem funcionar
    if not final_pipeline_id:
        final_pipeline_id = pipeline_name or "Pipeline_SjYJh6QYcw6bdK6poVnL"  # Usar o que você já tem
    if not final_stage_id:
        final_stage_id = stage_name or "Stage_b63276fd-6525-42ba-a575-156cd8a5bdfe"  # Usar o que você já tem
    
    opportunity_data = {
        "locationId": location_id,
        "title": title,
        "contactId": final_contact_id,
        "pipelineId": final_pipeline_id,
        "pipelineStageId": final_stage_id,
        "monetaryValue": value
    }
    
    try:
        response = await http_client.post("/opportunities/", json=opportunity_data)
        response.raise_for_status()
        
        result = response.json()
        
        # Formatar resposta de forma mais legível
        if "opportunity" in result:
            opportunity = result["opportunity"]
            formatted_result = {
                "success": True,
                "opportunity_id": opportunity.get("id"),
                "title": opportunity.get("title"),
                "contact_id": opportunity.get("contactId"),
                "pipeline_id": opportunity.get("pipelineId"),
                "stage_id": opportunity.get("pipelineStageId"),
                "value": opportunity.get("monetaryValue"),
                "status": opportunity.get("status"),
                "created_at": opportunity.get("dateAdded")
            }
        else:
            formatted_result = result
        
        return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao criar oportunidade: {str(e)}")]

async def create_opportunity(args: dict) -> list[TextContent]:
    """Create a new opportunity in GoHighLevel."""
    if not http_client:
        await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    # Campos obrigatórios
    required_fields = ["title", "contactId", "pipelineId", "pipelineStageId"]
    missing_fields = [field for field in required_fields if not args.get(field)]
    
    if missing_fields:
        return [TextContent(type="text", text=f"Campos obrigatórios faltando: {', '.join(missing_fields)}")]
    
    opportunity_data = {
        "locationId": location_id,
        **args
    }
    
    try:
        response = await http_client.post("/opportunities/", json=opportunity_data)
        response.raise_for_status()
        
        result = response.json()
        
        # Formatar resposta de forma mais legível
        if "opportunity" in result:
            opportunity = result["opportunity"]
            formatted_result = {
                "success": True,
                "opportunity_id": opportunity.get("id"),
                "title": opportunity.get("title"),
                "contact_id": opportunity.get("contactId"),
                "pipeline_id": opportunity.get("pipelineId"),
                "stage_id": opportunity.get("pipelineStageId"),
                "value": opportunity.get("monetaryValue"),
                "status": opportunity.get("status"),
                "created_at": opportunity.get("dateAdded")
            }
        else:
            formatted_result = result
        
        return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao criar oportunidade: {str(e)}")]

async def get_opportunities(args: dict) -> list[TextContent]:
    """Get opportunities from GoHighLevel."""
    if not http_client:
        await initialize_client()
    
    limit = args.get("limit", 10)
    location_id = os.getenv("GHL_LOCATION_ID")
    
    params = {
        "locationId": location_id,
        "limit": str(limit)
    }
    
    try:
        response = await http_client.get("/opportunities/", params=params)
        response.raise_for_status()
        
        data = response.json()
        opportunities = data.get("opportunities", [])
        
        # Formatar oportunidades de forma mais legível
        formatted_opportunities = []
        for opp in opportunities[:limit]:
            formatted_opp = {
                "id": opp.get("id"),
                "title": opp.get("title"),
                "contact_id": opp.get("contactId"),
                "value": opp.get("monetaryValue"),
                "status": opp.get("status"),
                "stage": opp.get("pipelineStageId"),
                "created_at": opp.get("dateAdded")
            }
            formatted_opportunities.append(formatted_opp)
        
        result = {
            "total_opportunities": len(formatted_opportunities),
            "opportunities": formatted_opportunities
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao buscar oportunidades: {str(e)}")]

async def get_pipelines(args: dict) -> list[TextContent]:
    """Get pipelines from GoHighLevel."""
    if not http_client:
        await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    try:
        # Tentar endpoint correto para pipelines
        response = await http_client.get("/pipelines/", params={"locationId": location_id})
        response.raise_for_status()
        
        data = response.json()
        pipelines = data.get("pipelines", [])
        
        # Formatar pipelines de forma mais legível
        formatted_pipelines = []
        for pipeline in pipelines:
            stages = []
            for stage in pipeline.get("stages", []):
                stages.append({
                    "id": stage.get("id"),
                    "name": stage.get("name"),
                    "position": stage.get("position")
                })
            
            formatted_pipeline = {
                "id": pipeline.get("id"),
                "name": pipeline.get("name"),
                "stages": stages
            }
            formatted_pipelines.append(formatted_pipeline)
        
        result = {
            "total_pipelines": len(formatted_pipelines),
            "pipelines": formatted_pipelines
        }
        
        return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        # Tentar endpoint alternativo
        try:
            response2 = await http_client.get(f"/opportunities/pipelines", params={"locationId": location_id})
            response2.raise_for_status()
            
            data2 = response2.json()
            return [TextContent(type="text", text=json.dumps(data2, indent=2, ensure_ascii=False))]
            
        except Exception as e2:
            # Se ambos falharem, retornar IDs de exemplo
            example_data = {
                "error": "Não foi possível buscar pipelines pela API",
                "message": "Use estas informações de exemplo ou consulte o GoHighLevel:",
                "exemplo_uso": "/criar_oportunidade \"Título\" ID_CONTATO PIPELINE_ID STAGE_ID VALOR",
                "como_encontrar_ids": {
                    "pipeline_id": "Vá em GoHighLevel > Settings > Pipelines",
                    "stage_id": "Dentro do pipeline, cada estágio tem um ID",
                    "contact_id": "Use /buscar_contatos para ver IDs"
                },
                "erro_original": str(e),
                "erro_alternativo": str(e2)
            }
            
            return [TextContent(type="text", text=json.dumps(example_data, indent=2, ensure_ascii=False))]

async def create_opportunity_natural(args: dict) -> list[TextContent]:
    """Create opportunity with natural language parameters."""
    # Sempre inicializar cliente para garantir que está configurado
    await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    # Parâmetros simples
    nome = args.get("nome")
    telefone = args.get("telefone") 
    email = args.get("email")
    pipeline_name = args.get("pipeline_name", "").lower()
    stage_name = args.get("stage_name", "").lower()
    valor = args.get("valor", 0)
    # Incluir timestamp para evitar duplicatas
    import datetime
    timestamp = datetime.datetime.now().strftime("%H:%M")
    titulo = args.get("titulo") or f"{nome} - {pipeline_name} - {timestamp}"
    contact_id = args.get("contact_id")  # ID de contato fornecido diretamente
    
    if not nome:
        return [TextContent(type="text", text="❌ Nome é obrigatório")]
    
    # 1. Estratégia de criação de contato
    final_contact_id = contact_id
    force_new = args.get("force_new", False)
    
    if not final_contact_id:
        if force_new or email:
            # Criar novo contato diretamente se forçado ou se temos email
            try:
                import random
                unique_suffix = random.randint(1000, 9999)
                
                new_contact_data = {
                    "locationId": location_id,
                    "firstName": nome
                }
                
                if email:
                    # Se email já existir, adicionar sufixo único
                    unique_email = f"{email.split('@')[0]}+{unique_suffix}@{email.split('@')[1]}" if "@" in email else f"{email}+{unique_suffix}"
                    new_contact_data["email"] = unique_email
                    
                if telefone:
                    # Adicionar sufixo ao telefone se necessário
                    clean_phone = telefone.replace("+", "").replace("-", "").replace(" ", "")
                    new_contact_data["phone"] = f"+{clean_phone}"
                
                # Criar contato diretamente
                contact_response = await http_client.post("/contacts/", json=new_contact_data)
                if contact_response.status_code == 201:
                    contact_data = contact_response.json()
                    final_contact_id = contact_data.get("contact", {}).get("id")
                elif contact_response.status_code == 422:
                    # Se falhar, usar email original
                    new_contact_data["email"] = email
                    contact_response = await http_client.post("/contacts/", json=new_contact_data)
                    if contact_response.status_code == 201:
                        contact_data = contact_response.json()
                        final_contact_id = contact_data.get("contact", {}).get("id")
                        
            except Exception as e:
                print(f"Erro ao criar contato: {e}")
        
        # Se ainda não conseguiu criar, buscar existente
        if not final_contact_id:
            contacts_result = await get_contacts({"limit": 50})
            contacts_data = json.loads(contacts_result[0].text)
            
            for contact in contacts_data.get("contacts", []):
                contact_name = contact.get("name", "").lower()
                contact_email = contact.get("email", "").lower()
                
                if (nome.lower() in contact_name or 
                    (email and email.lower() == contact_email)):
                    final_contact_id = contact.get("id")
                    break
    
    if not final_contact_id:
        return [TextContent(type="text", text="❌ Não foi possível criar contato. Tente novamente com um email válido.")]
    
    # 2. Mapear nomes de pipeline para IDs (seus IDs reais)
    pipeline_map = {
        "vendas": "SjYJh6QYcw6bdK6poVnL",
        "leads": "SjYJh6QYcw6bdK6poVnL", 
        "principal": "SjYJh6QYcw6bdK6poVnL",
        "padrão": "SjYJh6QYcw6bdK6poVnL",
        "default": "SjYJh6QYcw6bdK6poVnL"
    }
    
    # 3. Mapear nomes de estágio para IDs
    stage_map = {
        "inicial": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
        "lead": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
        "new lead": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
        "novo lead": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
        "contato": "a85fd236-f7ee-4a30-8d81-18bc44461892",
        "contacted": "a85fd236-f7ee-4a30-8d81-18bc44461892",
        "prospect": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
        "interessado": "d4998af7-728e-400b-9d27-d5b344061afc",
        "hot lead": "d4998af7-728e-400b-9d27-d5b344061afc",
        "qualificado": "d4998af7-728e-400b-9d27-d5b344061afc",
        "proposta": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
        "proposal": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
        "negociação": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
        "negociacao": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
        "fechado": "b63276fd-6525-42ba-a575-156cd8a5bdfe",
        "closed": "b63276fd-6525-42ba-a575-156cd8a5bdfe"
    }
    
    # Buscar IDs pelos nomes
    final_pipeline_id = pipeline_map.get(pipeline_name, "SjYJh6QYcw6bdK6poVnL")
    final_stage_id = stage_map.get(stage_name, "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd")
    
    opportunity_data = {
        "locationId": location_id,
        "name": titulo,
        "contactId": final_contact_id,
        "pipelineId": final_pipeline_id,
        "pipelineStageId": final_stage_id,
        "status": "open",
        "monetaryValue": valor
    }
    
    print(f"=== DEBUG OPPORTUNITY CREATION ===")
    print(f"Data being sent: {opportunity_data}")
    print(f"Final contact ID: {final_contact_id}")
    print(f"Final pipeline ID: {final_pipeline_id}")
    print(f"Final stage ID: {final_stage_id}")
    
    try:
        response = await http_client.post("/opportunities/", json=opportunity_data)
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        response.raise_for_status()
        
        result = response.json()
        
        if "opportunity" in result:
            opportunity = result["opportunity"]
            formatted_result = {
                "✅ SUCESSO": "Oportunidade criada!",
                "👤 Cliente": nome,
                "📞 Telefone": telefone or "Não informado",
                "📧 Email": email or "Não informado",
                "💰 Valor": f"R$ {valor}",
                "🔄 Pipeline": pipeline_name or "Padrão",
                "📊 Estágio": stage_name or "Inicial",
                "🆔 ID": opportunity.get("id"),
                "📅 Criado": opportunity.get("dateAdded")
            }
        else:
            formatted_result = result
        
        return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Erro ao criar oportunidade: {str(e)}")]

async def create_opportunity_easy(args: dict) -> list[TextContent]:
    """Create opportunity with just title and contact name."""
    if not http_client:
        await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    title = args.get("title")
    contact_name = args.get("contact_name")
    contact_email = args.get("contact_email")
    contact_phone = args.get("contact_phone")
    value = args.get("value", 0)
    
    if not title:
        return [TextContent(type="text", text="❌ Título da oportunidade é obrigatório")]
    
    if not contact_name:
        return [TextContent(type="text", text="❌ Nome do contato é obrigatório")]
    
    # 1. Resolver contato
    final_contact_id = None
    
    # Buscar contato por nome
    contacts_result = await get_contacts({"limit": 50})
    contacts_data = json.loads(contacts_result[0].text)
    
    for contact in contacts_data.get("contacts", []):
        if contact_name.lower() in contact.get("name", "").lower():
            final_contact_id = contact.get("id")
            break
    
    # Se não encontrou, criar novo contato
    if not final_contact_id:
        new_contact_data = {"firstName": contact_name}
        if contact_email:
            new_contact_data["email"] = contact_email
        if contact_phone:
            new_contact_data["phone"] = contact_phone
            
        contact_result = await create_contact(new_contact_data)
        contact_response = json.loads(contact_result[0].text)
        final_contact_id = contact_response.get("contact_id")
    
    if not final_contact_id:
        return [TextContent(type="text", text="❌ Não foi possível resolver o contato")]
    
    # 2. Usar pipeline e stage padrão (seus IDs que funcionaram)
    default_pipeline_id = "Pipeline_SjYJh6QYcw6bdK6poVnL"
    default_stage_id = "Stage_b63276fd-6525-42ba-a575-156cd8a5bdfe"
    
    opportunity_data = {
        "locationId": location_id,
        "title": title,
        "contactId": final_contact_id,
        "pipelineId": default_pipeline_id,
        "pipelineStageId": default_stage_id,
        "monetaryValue": value
    }
    
    try:
        response = await http_client.post("/opportunities/", json=opportunity_data)
        response.raise_for_status()
        
        result = response.json()
        
        # Formatar resposta de forma mais legível
        if "opportunity" in result:
            opportunity = result["opportunity"]
            formatted_result = {
                "success": True,
                "message": f"Oportunidade '{title}' criada para {contact_name}",
                "opportunity_id": opportunity.get("id"),
                "title": opportunity.get("title"),
                "contact_id": opportunity.get("contactId"),
                "value": f"R$ {opportunity.get('monetaryValue', 0)}",
                "status": opportunity.get("status"),
                "created_at": opportunity.get("dateAdded"),
                "pipeline_used": "Pipeline padrão",
                "stage_used": "Estágio inicial"
            }
        else:
            formatted_result = result
        
        return [TextContent(type="text", text=json.dumps(formatted_result, indent=2, ensure_ascii=False))]
    
    except Exception as e:
        return [TextContent(type="text", text=f"Erro ao criar oportunidade: {str(e)}")]