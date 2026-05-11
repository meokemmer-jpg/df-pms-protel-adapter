"""Protel-Auth-Manager [CRUX-MK].

Protel verwendet Basic-Auth + Tenant-Code:
- Username + Password (HTTP-Basic-Authorization)
- X-Protel-Tenant Header

ENV-Var-gated: ohne PROTEL_USERNAME -> Mock.

Welle-36.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProtelCredentials:
    """Kanonische Protel-Credentials.

    source ∈ {"env", "mock", "vault"}
    """
    username: str
    password: str
    tenant_code: str
    source: str
    fetched_iso: str


class ProtelAuth:
    """Manager fuer Protel Basic-Auth + Tenant-Code-Auth."""

    MOCK_USERNAME = "mock-protel-user"
    MOCK_PASSWORD = "mock-protel-password"
    MOCK_TENANT_CODE = "MOCK-HEYLOU-HILD-001"

    def __init__(self, sandbox_mode: Optional[bool] = None):
        if sandbox_mode is None:
            self.sandbox_mode = os.environ.get("DF_PMS_PROTEL_REAL_ENABLED", "false") != "true"
        else:
            self.sandbox_mode = sandbox_mode

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def get_credentials(self, tenant_id: str = "hildesheim") -> Optional[ProtelCredentials]:
        """Holt Credentials aus ENV oder Mock."""
        if self.sandbox_mode:
            return ProtelCredentials(
                username=self.MOCK_USERNAME,
                password=self.MOCK_PASSWORD,
                tenant_code=self.MOCK_TENANT_CODE,
                source="mock",
                fetched_iso=self._now_iso(),
            )

        username = os.environ.get("PROTEL_USERNAME", "")
        password = os.environ.get("PROTEL_PASSWORD", "")
        tenant_code = os.environ.get("PROTEL_TENANT_CODE", "")

        if not username or not password or not tenant_code:
            logger.warning(
                f"[protel-auth] missing credentials for tenant={tenant_id} "
                f"(USERNAME={'set' if username else 'EMPTY'}, "
                f"PASSWORD={'set' if password else 'EMPTY'}, "
                f"TENANT_CODE={'set' if tenant_code else 'EMPTY'})"
            )
            return None

        return ProtelCredentials(
            username=username,
            password=password,
            tenant_code=tenant_code,
            source="env",
            fetched_iso=self._now_iso(),
        )

    def validate(self, creds: Optional[ProtelCredentials]) -> bool:
        """Strukturelle Validierung."""
        if creds is None:
            return False
        if not creds.username or not creds.password or not creds.tenant_code:
            return False
        if creds.source not in ("env", "mock", "vault"):
            return False
        return True

    def refresh_if_expired(self, creds: Optional[ProtelCredentials]) -> Optional[ProtelCredentials]:
        """Re-fetch nach 24h."""
        if not self.validate(creds):
            return self.get_credentials()
        try:
            fetched = datetime.fromisoformat(creds.fetched_iso)
            now = datetime.now(timezone.utc)
            if now - fetched > timedelta(hours=24):
                return self.get_credentials()
        except (ValueError, TypeError):
            return self.get_credentials()
        return creds

    def is_real_mode(self) -> bool:
        return not self.sandbox_mode
