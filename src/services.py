import httpx
import time
import httpx
import time
import logging
from threading import Lock
from .config import get_settings
from .repository import SMSRepository, ContactRepository
from .utils import normalize_phone


logger = logging.getLogger(__name__)


class SMSService:
    _instance = None
    _lock = Lock()
    _last_sent_time = 0
    RATE_LIMIT_SECONDS = 10.0

    def __init__(self):
        self.settings = get_settings()
        self.sms_repo = SMSRepository()
        self.contact_repo = ContactRepository()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def _wait_for_rate_limit(self):
        with self._lock:
            now = time.time()
            elapsed = now - self._last_sent_time
            if elapsed < self.RATE_LIMIT_SECONDS:
                wait_time = self.RATE_LIMIT_SECONDS - elapsed
                logger.info(f"Rate limiting active. Waiting {wait_time:.2f}s...")
                time.sleep(wait_time)
            self._last_sent_time = time.time()

    async def send_sms(
        self, recipient: str, message: str, dry_run: bool = False
    ) -> str:
        contact_id = None

        if recipient.isdigit() and len(recipient) < 8:
            contact = self.contact_repo.get(int(recipient))
            if not contact:
                raise ValueError(f"Contact ID {recipient} not found.")
            phone = contact.phone
            contact_id = contact.id
        else:
            phone = normalize_phone(recipient)
            contact = self.contact_repo.get_by_phone(phone)
            if contact:
                contact_id = contact.id

        if dry_run:
            logger.info(f"[DRY RUN] to {phone}: {message}")
            return f"Dry run success. Message to {phone}"

        self._wait_for_rate_limit()

        async with httpx.AsyncClient() as client:
            headers = {"x-api-key": self.settings.SMS_API_KEY}
            payload = {"recipient": phone, "message": message}

            try:
                response = await client.post(
                    f"{self.settings.SMS_API_BASE_URL}/send/sms",
                    json=payload,
                    headers=headers,
                    timeout=self.RATE_LIMIT_SECONDS,
                )

                status = "sent" if response.status_code == 200 else "failed"
                self.sms_repo.log(
                    phone, message, status, response.status_code, contact_id
                )

                if response.status_code == 429:
                    raise Exception("Rate limit exceeded.")

                response.raise_for_status()
                return (
                    f"SMS sent to {phone}. ID: {response.json().get('id', 'unknown')}"
                )

            except httpx.RequestError as e:
                self.sms_repo.log(phone, message, "failed", 503, contact_id)
                raise Exception(f"Connection error: {str(e)}")
