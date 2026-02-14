import asyncio
from src.services import SMSService
from src.repository import ContactRepository, SMSRepository
from src.database import init_db


async def test_logic():
    print("--- Initializing DB ---")
    init_db()

    contact_repo = ContactRepository()
    sms_service = SMSService.get_instance()

    print("\n--- Testing Contacts ---")
    # Create or Get
    phone = "+639171234567"  # Normalized manually for test
    c = contact_repo.get_by_phone(phone)
    if not c:
        # Check if non-normalized exists to avoid unique error if partial migration
        c = contact_repo.get_by_phone("09171234567")
        if not c:
            c = contact_repo.create("Jansen", phone, ["friend", "dev"], "Test contact")
        else:
            print("Found via old format, updating...")
            contact_repo.update(c.id, phone=phone)
            c = contact_repo.get(c.id)
    print(f"Contact: {c.name} ({c.phone}) - ID: {c.id}")

    # List
    contacts = contact_repo.list()
    print(f"Found {len(contacts)} contacts.")

    print("\n--- Testing SMS (Dry Run) ---")
    # Send
    try:
        result = await sms_service.send_sms(c.phone, "Hello from Python!", dry_run=True)
        print(f"SMS Result: {result}")
    except Exception as e:
        print(f"SMS Error: {e}")

    print("\n--- Done ---")


if __name__ == "__main__":
    asyncio.run(test_logic())
