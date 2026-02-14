from mcp.server.fastmcp import FastMCP
from .services import SMSService
from .repository import ContactRepository, SMSRepository
from .database import init_db
from .utils import normalize_phone


# Initialize DB tables
init_db()

mcp = FastMCP("mcp-ph-sms")
sms_service = SMSService.get_instance()
contact_repo = ContactRepository()
sms_repo = SMSRepository()


@mcp.tool()
def contacts_list(limit: int = 50, tag: str | None = None, q: str | None = None):
    """List contacts with regex-like filtering."""
    contacts = contact_repo.list(limit, tag, q)
    return contacts


@mcp.tool()
def contacts_get(contact_id: int):
    """Get contact by ID."""
    return contact_repo.get(contact_id)


@mcp.tool()
def contacts_create(
    name: str, phone: str, tags: list[str] | None = [], notes: str | None = None
):
    """Create a contact."""
    norm_phone = normalize_phone(phone)
    # Ensure tags is a list if None passed
    safe_tags = tags if tags is not None else []
    return contact_repo.create(name, norm_phone, safe_tags, notes)


@mcp.tool()
def contacts_update(
    contact_id: int,
    name: str | None = None,
    phone: str | None = None,
    tags: list[str] | None = None,
    notes: str | None = None,
):
    """Update contact."""
    updates = {}
    if name:
        updates["name"] = name
    if phone:
        updates["phone"] = normalize_phone(phone)
    if tags is not None:
        updates["tags"] = tags
    if notes:
        updates["notes"] = notes
    return contact_repo.update(contact_id, **updates)


@mcp.tool()
def contacts_delete(contact_id: int):
    """Delete a contact."""
    return contact_repo.delete(contact_id)


@mcp.tool()
async def sms_send(recipient: str, message: str, dry_run: bool = False):
    """Send SMS."""
    return await sms_service.send_sms(recipient, message, dry_run)


@mcp.tool()
def sms_history(limit: int = 20, contact_id: int | None = None):
    """View SMS history."""
    return sms_repo.list(limit, contact_id)


@mcp.prompt()
def compose_sms(topic: str):
    return f"Draft an SMS about: {topic}"
