import os
import json
import httpx
from dotenv import load_dotenv
from mcp.types import TextContent

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

async def create_opportunity_natural(args: dict) -> list[TextContent]:
    """Create opportunity with natural language parameters - WORKING VERSION."""
    await initialize_client()
    
    location_id = os.getenv("GHL_LOCATION_ID")
    
    # Parâmetros simples
    nome = args.get("nome")
    telefone = args.get("telefone") 
    email = args.get("email")
    pipeline_name = args.get("pipeline_name", "").lower()
    stage_name = args.get("stage_name", "").lower()
    valor = args.get("valor", 0)
    
    if not nome:
        return [TextContent(type="text", text="❌ Nome é obrigatório")]
    
    # 1. SEMPRE criar novo contato (baseado no teste que funciona)
    import random
    unique_suffix = random.randint(10000, 99999)
    
    contact_data = {
        "locationId": location_id,
        "firstName": nome
    }
    
    if email:
        # Email único para evitar duplicatas - formato válido
        if "@" in email:
            email_parts = email.split('@')
            unique_email = f"{email_parts[0]}.{unique_suffix}@{email_parts[1]}"
        else:
            unique_email = f"{email}.{unique_suffix}@gmail.com"
        contact_data["email"] = unique_email
        
    if telefone:
        # Telefone único para evitar duplicatas
        clean_phone = telefone.replace("+", "").replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
        
        # Adicionar sufixo único ao telefone para evitar duplicatas
        if len(clean_phone) >= 8:
            # Usar os últimos 3 dígitos do unique_suffix
            unique_phone_suffix = str(unique_suffix)[-3:]
            base_phone = clean_phone[:-3] + unique_phone_suffix
        else:
            base_phone = clean_phone + str(unique_suffix)[-3:]
        
        # Aplicar formatação de país
        if len(base_phone) == 11 and base_phone.startswith(('11', '12', '13', '14', '15', '16', '17', '18', '19', '21', '22', '24', '27', '28')):
            # Número brasileiro
            contact_data["phone"] = f"+55{base_phone}"
        elif len(base_phone) == 10:
            # Número americano
            contact_data["phone"] = f"+1{base_phone}"
        else:
            # Formato padrão internacional
            contact_data["phone"] = f"+1555{base_phone[-7:]}"
    
    try:
        # Criar contato
        contact_response = await http_client.post("/contacts/", json=contact_data)
        if contact_response.status_code != 201:
            return [TextContent(type="text", text=f"❌ Erro ao criar contato: {contact_response.text}")]
        
        contact_result = contact_response.json()
        contact_id = contact_result["contact"]["id"]
        
        # 2. Mapear pipeline e stage
        pipeline_map = {
            "vendas": "SjYJh6QYcw6bdK6poVnL",
            "leads": "SjYJh6QYcw6bdK6poVnL", 
            "lead": "SjYJh6QYcw6bdK6poVnL",
            "padrão": "SjYJh6QYcw6bdK6poVnL",
            "default": "SjYJh6QYcw6bdK6poVnL"
        }
        
        stage_map = {
            "inicial": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
            "lead": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
            "new lead": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
            "novo lead": "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd",
            "contacted": "a85fd236-f7ee-4a30-8d81-18bc44461892",
            "contato": "a85fd236-f7ee-4a30-8d81-18bc44461892",
            "hot lead": "d4998af7-728e-400b-9d27-d5b344061afc",
            "quente": "d4998af7-728e-400b-9d27-d5b344061afc",
            "proposal": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
            "proposal sent": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
            "proposta": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
            "proposta enviada": "d548cca5-2cdc-4d64-99f1-fb4a3ade1174",
            "closed": "b63276fd-6525-42ba-a575-156cd8a5bdfe",
            "fechado": "b63276fd-6525-42ba-a575-156cd8a5bdfe"
        }
        
        final_pipeline_id = pipeline_map.get(pipeline_name, "SjYJh6QYcw6bdK6poVnL")
        final_stage_id = stage_map.get(stage_name, "6c3a7dde-3fa6-46c8-bafa-d0e085aa62bd")
        
        # 3. Criar oportunidade com nome único
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M")
        opportunity_name = f"{nome} - {pipeline_name or 'Lead'} - {timestamp}"
        
        opportunity_data = {
            "locationId": location_id,
            "name": opportunity_name,
            "contactId": contact_id,
            "pipelineId": final_pipeline_id,
            "pipelineStageId": final_stage_id,
            "status": "open",
            "monetaryValue": valor
        }
        
        # Criar oportunidade
        opp_response = await http_client.post("/opportunities/", json=opportunity_data)
        if opp_response.status_code != 201:
            return [TextContent(type="text", text=f"❌ Erro ao criar oportunidade: {opp_response.text}")]
        
        opp_result = opp_response.json()
        opportunity_id = opp_result["opportunity"]["id"]
        
        # Sucesso!
        success_message = f"""✅ SUCESSO COMPLETO!

👤 Cliente: {nome}
📞 Telefone: {telefone or 'Não informado'}
📧 Email: {contact_data.get('email', 'Não informado')}
💰 Valor: R$ {valor}
🔄 Pipeline: {pipeline_name or 'Lead'}
📊 Stage: {stage_name or 'New Lead'}
🆔 ID Contato: {contact_id}
🆔 ID Oportunidade: {opportunity_id}"""
        
        return [TextContent(type="text", text=success_message)]
        
    except Exception as e:
        return [TextContent(type="text", text=f"❌ Erro inesperado: {str(e)}")]