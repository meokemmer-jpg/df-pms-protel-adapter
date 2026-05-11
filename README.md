# df-pms-protel-adapter [CRUX-MK]

**14. Foundation-DF (Welle-36 HeyLou-Mosaic-Layer): Protel PMS-Adapter (EU-Markt).**

Mosaic-Adapter fuer Protel PMS (Marktfuehrer im EU-Hospitality-Segment).
ENV-Var-gated Sandbox-Default-Mode, Mock-Fallback Pflicht, K17-PAV, HMAC-SHA256.

## Architektur

- `ProtelConnector` (Booking/Inventory-API + Protel-API-Wrapper)
- `ProtelAuth` (Basic-Auth + Tenant-Code-Pattern)
- `ProtelAdapterOrchestrator` (LaunchAgent-Entry-Point)
- `AuditLogger` (HMAC-SHA256 JSONL)

## Protel-Spezifika

Protel verwendet **Basic-Auth + Tenant-Code**:
- Username + Password im Authorization-Header (HTTP-Basic)
- Tenant-Code als zusaetzlicher Header `X-Protel-Tenant`
- Property-spezifische Endpoints

## ENV-Vars

| Var | Default | Pflicht | Beschreibung |
|-----|---------|---------|--------------|
| `DF_PMS_PROTEL_REAL_ENABLED` | `false` | nein | Aktiviert Real-API |
| `PROTEL_USERNAME` | `""` | bei Real | API-User |
| `PROTEL_PASSWORD` | `""` | bei Real | API-Password |
| `PROTEL_TENANT_CODE` | `""` | bei Real | Property-Tenant-Code |
| `DF_PMS_PROTEL_PHRONESIS_TICKET` | `""` | bei Real-Booking | K17-PAV |
| `DF_PMS_PROTEL_HMAC_SECRET` | `""` | nein | Audit-Secret |

## Welle-36 Status

- Tier: SKELETON-CONDITIONAL
- LaunchAgent-Cadence: 7200s

## Install

```bash
cp scripts/com.kemmer.df-pms-protel-adapter.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.kemmer.df-pms-protel-adapter.plist
```

## Tests

```bash
python3 -m pytest tests/ -v
```

[CRUX-MK]
