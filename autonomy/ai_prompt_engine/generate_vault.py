import uuid
import datetime
from autonomy.pipeline import event_bus
from autonomy.pipeline.event_definitions import EVENT_VAULT_CREATED

def create_vault(user_id, vault_data):
    """
    Create a new vault and dispatch the 'vault_created' event.
    Args:
        user_id (str): The ID of the user creating the vault.
        vault_data (dict): Metadata and content for the new vault.
    Returns:
        dict: Vault record with assigned ID and timestamps.
    """
    vault_id = str(uuid.uuid4())
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    vault_record = {
        'vault_id': vault_id,
        'user_id': user_id,
        'created_at': now,
        'metadata': vault_data
    }
    # Dispatch the event to the event-driven pipeline
    event_bus.dispatch_event(EVENT_VAULT_CREATED, vault_record)
    return vault_record

if __name__ == "__main__":
    # Example usage
    user_id = "test_user"
    vault_data = {
        "title": "Example Vault",
        "description": "This is a sample vault for event-driven testing.",
        "tags": ["sample", "test", "event-driven"]
    }
    result = create_vault(user_id, vault_data)
    print("Vault created and event dispatched:", result)
