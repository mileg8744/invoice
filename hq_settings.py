"""Persisted HQ profile that overrides Config defaults at runtime."""

from __future__ import annotations

import json

from config import Config, INSTANCE_DIR

HQ_SETTINGS_PATH = INSTANCE_DIR / "hq_settings.json"

HQ_FIELDS = (
    "HQ_COPY_EMAIL",
    "MAIL_FROM",
    "PGU_NAME",
    "PGU_DEPT",
    "PGU_ADDRESS",
    "PGU_PHONE",
    "PGU_SIGNATORY",
    "PGU_TITLE",
    "BANK_NAME",
    "BANK_BRANCH",
    "BANK_ACCOUNT_NAME",
    "BANK_ACCOUNT_NO",
    "BANK_SWIFT",
)

FACTORY_DEFAULTS = {key: getattr(Config, key, "") or "" for key in HQ_FIELDS}


def default_hq_settings() -> dict:
    return dict(FACTORY_DEFAULTS)


def load_hq_settings() -> dict:
    data = default_hq_settings()
    if HQ_SETTINGS_PATH.exists():
        try:
            saved = json.loads(HQ_SETTINGS_PATH.read_text(encoding="utf-8"))
            if isinstance(saved, dict):
                for key in HQ_FIELDS:
                    if key in saved and saved[key] is not None:
                        data[key] = str(saved[key])
        except (OSError, json.JSONDecodeError):
            pass
    apply_hq_settings(data)
    return data


def apply_hq_settings(data: dict) -> None:
    for key in HQ_FIELDS:
        if key in data:
            setattr(Config, key, data[key])


def save_hq_settings(data: dict) -> dict:
    payload = default_hq_settings()
    for key in HQ_FIELDS:
        if key in data and data[key] is not None:
            payload[key] = str(data[key]).strip()
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)
    HQ_SETTINGS_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    apply_hq_settings(payload)
    return payload
