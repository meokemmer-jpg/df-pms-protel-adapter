"""df-pms-protel-adapter [CRUX-MK].

Welle-36 HeyLou-Mosaic-Adapter fuer Protel PMS (EU-Markt).
"""

from __future__ import annotations

__version__ = "0.1.0-SKELETON"
__df_id__ = "df-pms-protel-adapter"
__welle__ = "welle-36"


def get_connector():
    from src.protel_adapter import ProtelConnector
    return ProtelConnector


def get_auth():
    from src.protel_auth import ProtelAuth
    return ProtelAuth


def get_orchestrator():
    from src.adapter_orchestrator import ProtelAdapterOrchestrator
    return ProtelAdapterOrchestrator


def get_audit_logger():
    from src.audit_logger import AuditLogger
    return AuditLogger


__all__ = ["__version__", "__df_id__", "__welle__", "get_connector", "get_auth", "get_orchestrator", "get_audit_logger"]
