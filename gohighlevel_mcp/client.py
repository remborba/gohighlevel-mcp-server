"""GoHighLevel API client for MCP server."""

import os
from typing import Dict, List, Optional, Any
import httpx
from pydantic import BaseModel, Field


class GHLContact(BaseModel):
    """GoHighLevel contact model."""
    id: Optional[str] = None
    name: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    customFields: Dict[str, Any] = Field(default_factory=dict)


class GHLConversation(BaseModel):
    """GoHighLevel conversation model."""
    id: Optional[str] = None
    contactId: Optional[str] = None
    locationId: Optional[str] = None
    lastMessageBody: Optional[str] = None
    lastMessageDirection: Optional[str] = None
    unreadCount: int = 0


class GHLAppointment(BaseModel):
    """GoHighLevel appointment model."""
    id: Optional[str] = None
    calendarId: Optional[str] = None
    contactId: Optional[str] = None
    title: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    status: Optional[str] = None


class GoHighLevelClient:
    """Client for GoHighLevel API integration."""
    
    def __init__(self, api_key: str, location_id: str, api_version: str = "v1"):
        self.api_key = api_key
        self.location_id = location_id
        self.api_version = api_version
        self.base_url = os.getenv("GHL_BASE_URL", "https://services.leadconnectorhq.com")
        
        self.client = httpx.AsyncClient(
            base_url=f"{self.base_url}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Version": "2021-07-28"
            },
            timeout=30.0
        )
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
    
    async def get_contacts(self, limit: int = 100, query: Optional[str] = None) -> List[GHLContact]:
        """Get contacts from GoHighLevel."""
        params = {
            "locationId": self.location_id,
            "limit": str(limit)
        }
        
        if query:
            params["query"] = query
            
        response = await self.client.get(f"/contacts/", params=params)
        response.raise_for_status()
        
        data = response.json()
        contacts = []
        
        if "contacts" in data:
            for contact_data in data["contacts"]:
                contacts.append(GHLContact(**contact_data))
        
        return contacts
    
    async def get_contact(self, contact_id: str) -> Optional[GHLContact]:
        """Get a specific contact by ID."""
        response = await self.client.get(f"/contacts/{contact_id}")
        
        if response.status_code == 404:
            return None
            
        response.raise_for_status()
        return GHLContact(**response.json()["contact"])
    
    async def create_contact(self, contact: GHLContact) -> GHLContact:
        """Create a new contact in GoHighLevel."""
        contact_data = contact.model_dump(exclude_none=True)
        contact_data["locationId"] = self.location_id
        
        response = await self.client.post("/contacts/", json=contact_data)
        response.raise_for_status()
        
        return GHLContact(**response.json()["contact"])
    
    async def update_contact(self, contact_id: str, contact: GHLContact) -> GHLContact:
        """Update an existing contact."""
        contact_data = contact.model_dump(exclude_none=True)
        
        response = await self.client.put(f"/contacts/{contact_id}", json=contact_data)
        response.raise_for_status()
        
        return GHLContact(**response.json()["contact"])
    
    async def get_conversations(self, limit: int = 20) -> List[GHLConversation]:
        """Get conversations from GoHighLevel."""
        params = {
            "locationId": self.location_id,
            "limit": str(limit)
        }
        
        response = await self.client.get("/conversations/", params=params)
        response.raise_for_status()
        
        data = response.json()
        conversations = []
        
        if "conversations" in data:
            for conv_data in data["conversations"]:
                conversations.append(GHLConversation(**conv_data))
        
        return conversations
    
    async def send_message(self, conversation_id: str, message: str, message_type: str = "SMS") -> Dict[str, Any]:
        """Send a message in a conversation."""
        message_data = {
            "type": message_type,
            "message": message,
            "conversationId": conversation_id
        }
        
        response = await self.client.post(f"/conversations/messages", json=message_data)
        response.raise_for_status()
        
        return response.json()
    
    async def get_appointments(self, limit: int = 50, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[GHLAppointment]:
        """Get appointments from GoHighLevel."""
        params = {
            "locationId": self.location_id,
            "limit": str(limit)
        }
        
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
            
        response = await self.client.get("/appointments/", params=params)
        response.raise_for_status()
        
        data = response.json()
        appointments = []
        
        if "events" in data:
            for apt_data in data["events"]:
                appointments.append(GHLAppointment(**apt_data))
        
        return appointments
    
    async def create_appointment(self, appointment: GHLAppointment) -> GHLAppointment:
        """Create a new appointment."""
        apt_data = appointment.model_dump(exclude_none=True)
        apt_data["locationId"] = self.location_id
        
        response = await self.client.post("/appointments/", json=apt_data)
        response.raise_for_status()
        
        return GHLAppointment(**response.json())
    
    async def get_pipelines(self) -> List[Dict[str, Any]]:
        """Get pipelines from GoHighLevel."""
        params = {"locationId": self.location_id}
        
        response = await self.client.get("/opportunities/pipelines", params=params)
        response.raise_for_status()
        
        return response.json().get("pipelines", [])
    
    async def get_opportunities(self, pipeline_id: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Get opportunities from GoHighLevel."""
        params = {
            "locationId": self.location_id,
            "limit": str(limit)
        }
        
        if pipeline_id:
            params["pipelineId"] = pipeline_id
            
        response = await self.client.get("/opportunities/", params=params)
        response.raise_for_status()
        
        return response.json().get("opportunities", [])