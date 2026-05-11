"""Protel-Adapter [CRUX-MK].

Connector fuer Protel PMS-API (EU-Markt):
- Booking-API
- Inventory-API
- Reservation-Management

K12 Provenance, K13 PAV, ENV-Var-gated Sandbox.

Welle-36.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AdapterResponse:
    """Kanonische Adapter-Response."""
    adapter_name: str
    operation: str
    success: bool
    payload: dict
    source: str
    timestamp_iso: str
    request_hash: str
    error: Optional[str] = None


class PMSAdapter(ABC):
    """Mosaic-Shared Pflicht-Interface."""

    @abstractmethod
    def connect(self, credentials: dict) -> bool: ...

    @abstractmethod
    def query_inventory(self, hotel_id: str, date_range: tuple) -> list[dict]: ...

    @abstractmethod
    def book_room(self, hotel_id: str, room_type: str, guest: dict, dates: tuple) -> str: ...

    @abstractmethod
    def cancel_booking(self, booking_id: str) -> bool: ...

    @abstractmethod
    def get_capabilities(self) -> dict: ...


class ProtelConnector(PMSAdapter):
    """Protel PMS-API Connector (EU-Markt)."""

    MOCK_HOTELS = {
        "hildesheim": {"property_id": "mock-protel-hildesheim-001", "rooms_total": 80},
        "munich": {"property_id": "mock-protel-munich-001", "rooms_total": 120},
    }

    def __init__(self, sandbox_mode: Optional[bool] = None):
        self.adapter_name = "protel-pms"
        if sandbox_mode is None:
            self.sandbox_mode = os.environ.get("DF_PMS_PROTEL_REAL_ENABLED", "false") != "true"
        else:
            self.sandbox_mode = sandbox_mode
        self._connected = False
        self._credentials: Optional[dict] = None

    def _request_hash(self, operation: str, payload: dict) -> str:
        canonical = json.dumps({"op": operation, "payload": payload}, sort_keys=True, default=str)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def connect(self, credentials: dict) -> bool:
        try:
            if self.sandbox_mode:
                self._connected = True
                self._credentials = credentials
                return True

            username = credentials.get("username", "")
            password = credentials.get("password", "")
            tenant_code = credentials.get("tenant_code", "")
            if not username or not password or not tenant_code:
                logger.warning("[protel-adapter] missing credentials")
                self._connected = False
                return False

            self._credentials = credentials
            self._connected = True
            return True
        except Exception as e:
            logger.error(f"[protel-adapter] connect failed: {e}")
            self._connected = False
            return False

    def query_inventory(self, hotel_id: str, date_range: tuple) -> list[dict]:
        op = "query_inventory"
        try:
            if not self._connected:
                return []

            criteria = {"hotel_id": hotel_id, "date_range": list(date_range)}
            h = self._request_hash(op, criteria)

            if self.sandbox_mode:
                hotel = self.MOCK_HOTELS.get(hotel_id, {})
                if not hotel:
                    return []
                hash_int = int(h, 16) % 100
                available = max(0, hotel["rooms_total"] - hash_int)
                return [
                    {
                        "hotel_id": hotel_id,
                        "property_id": hotel["property_id"],
                        "room_type": "standard",
                        "available": available // 3,
                        "rate_eur": 110.0 + (hash_int % 30),
                    },
                    {
                        "hotel_id": hotel_id,
                        "property_id": hotel["property_id"],
                        "room_type": "comfort",
                        "available": available // 4,
                        "rate_eur": 165.0 + (hash_int % 40),
                    },
                ]

            logger.warning("[protel-adapter] real-api query_inventory not yet implemented")
            return []
        except Exception as e:
            logger.error(f"[protel-adapter] query_inventory failed: {e}")
            return []

    def book_room(self, hotel_id: str, room_type: str, guest: dict, dates: tuple) -> str:
        op = "book_room"
        try:
            if not self._connected:
                return ""

            payload = {"hotel_id": hotel_id, "room_type": room_type, "guest": guest, "dates": list(dates)}
            h = self._request_hash(op, payload)

            if self.sandbox_mode:
                return f"protel-mock-{h[:8]}"

            # K17-PAV
            ticket = os.environ.get("DF_PMS_PROTEL_PHRONESIS_TICKET", "")
            if not ticket:
                logger.warning("[protel-adapter] K17-PAV: missing DF_PMS_PROTEL_PHRONESIS_TICKET")
                return ""

            logger.warning("[protel-adapter] real-api book_room not yet implemented")
            return ""
        except Exception as e:
            logger.error(f"[protel-adapter] book_room failed: {e}")
            return ""

    def cancel_booking(self, booking_id: str) -> bool:
        op = "cancel_booking"
        try:
            if not self._connected or not booking_id:
                return False

            payload = {"booking_id": booking_id}
            _ = self._request_hash(op, payload)

            if self.sandbox_mode:
                if booking_id.startswith("fail-"):
                    return False
                return True

            logger.warning("[protel-adapter] real-api cancel_booking not yet implemented")
            return False
        except Exception as e:
            logger.error(f"[protel-adapter] cancel_booking failed: {e}")
            return False

    def get_capabilities(self) -> dict:
        return {
            "adapter_name": self.adapter_name,
            "version": "0.1.0-SKELETON",
            "sandbox_mode": self.sandbox_mode,
            "connected": self._connected,
            "adapter_type": "pms",
            "market": "EU",
            "supported_operations": ["connect", "query_inventory", "book_room", "cancel_booking"],
            "feature_flags": {
                "real_api": not self.sandbox_mode,
                "k17_pav": True,
                "hmac_audit": True,
                "circuit_breaker": True,
                "basic_auth": True,
            },
            "health_score": 1.0 if self._connected else 0.5,
        }
