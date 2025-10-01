"""Tests for the GoHighLevel client."""

import pytest
from unittest.mock import AsyncMock, patch
import httpx

from gohighlevel_mcp.client import GoHighLevelClient, GHLContact


@pytest.fixture
def ghl_client():
    """Create a test GHL client."""
    return GoHighLevelClient(
        api_key="test_key",
        location_id="test_location",
        api_version="v1"
    )


@pytest.mark.asyncio
async def test_get_contacts(ghl_client):
    """Test getting contacts from GHL."""
    mock_response = {
        "contacts": [
            {
                "id": "contact_1",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
                "phone": "+1234567890",
                "tags": ["lead"],
                "customFields": {}
            }
        ]
    }
    
    with patch.object(ghl_client.client, 'get') as mock_get:
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.raise_for_status = AsyncMock()
        
        contacts = await ghl_client.get_contacts(limit=10)
        
        assert len(contacts) == 1
        assert contacts[0].firstName == "John"
        assert contacts[0].email == "john@example.com"


@pytest.mark.asyncio
async def test_create_contact(ghl_client):
    """Test creating a contact in GHL."""
    new_contact = GHLContact(
        firstName="Jane",
        lastName="Smith",
        email="jane@example.com",
        phone="+1987654321"
    )
    
    mock_response = {
        "contact": {
            "id": "new_contact_id",
            "firstName": "Jane",
            "lastName": "Smith", 
            "email": "jane@example.com",
            "phone": "+1987654321",
            "tags": [],
            "customFields": {}
        }
    }
    
    with patch.object(ghl_client.client, 'post') as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status = AsyncMock()
        
        created_contact = await ghl_client.create_contact(new_contact)
        
        assert created_contact.id == "new_contact_id"
        assert created_contact.firstName == "Jane"
        assert created_contact.email == "jane@example.com"


@pytest.mark.asyncio
async def test_get_contact_not_found(ghl_client):
    """Test getting a contact that doesn't exist."""
    with patch.object(ghl_client.client, 'get') as mock_get:
        mock_get.return_value.status_code = 404
        
        contact = await ghl_client.get_contact("nonexistent_id")
        
        assert contact is None