import os
import requests
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DB_ID = os.getenv("NOTION_DB_ID")

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

from autonomy.security.ai_safety_layer import anti_sentience_guard

def push_to_notion(vault_data: Dict[str, Any]) -> Dict[str, Any]:
    """Push vault data to Notion dashboard."""
    try:
        logger.info(f"Pushing vault data to Notion: {vault_data['title']}")
        
        # Validate required environment variables
        if not NOTION_TOKEN:
            raise ValueError("NOTION_TOKEN environment variable is not set")
            
        if not NOTION_DB_ID:
            raise ValueError("NOTION_DB_ID environment variable is not set")
            
        # AI SAFETY CHECKS
        for field in ["description", "summary", "revenue_blurb"]:
            val = vault_data.get(field, "")
            if val and not anti_sentience_guard(val, user=vault_data.get('user'), action=f'push_to_notion:{field}'):
                logger.error(f"AI safety violation: Unsafe sentience/agency patterns detected in Notion push field '{field}'.")
                raise Exception(f"AI safety violation: Unsafe sentience/agency patterns detected in Notion push field '{field}'.")

        # Prepare data for Notion
        data = {
            "parent": {"database_id": NOTION_DB_ID},
            "properties": {
                "Name": {"title": [{"text": {"content": vault_data['title']}}]},
                "Description": {"rich_text": [{"text": {"content": vault_data['description']}}]},
                "Summary": {"rich_text": [{"text": {"content": vault_data.get("summary", "")}}]},
                "Revenue": {"rich_text": [{"text": {"content": vault_data.get("revenue_blurb", "")}}]},
                "Chapters": {"rich_text": [{"text": {"content": ", ".join(vault_data['chapters'])}}]},
                "Status": {"select": {"name": "Generated"}},
                "Created": {"date": {"start": datetime.now().isoformat()}},
                "CTA": {"rich_text": [{"text": {"content": vault_data['cta']}}]},
                "Type": {"select": {"name": "Vault"}},
                "Brand": {"select": {"name": "AIFOLIO™"}}
            }
        }
        
        # Make API request
        logger.info("Sending data to Notion API")
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        
        # Handle response
        if response.status_code != 200:
            logger.error(f"Notion API error: {response.text}")
            raise Exception(f"Notion API error: {response.status_code}")
            
        logger.info("Successfully pushed vault data to Notion")
        return response.json()
        
    except Exception as e:
        logger.error(f"Error pushing to Notion: {str(e)}")
        raise
