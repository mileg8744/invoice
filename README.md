# PGU Overseas Education Invoice Portal

POSCO Group University web app for issuing, acknowledging, and collecting overseas education invoices.

## Run

`
pip install -r requirements.txt
python app.py
`

Open http://127.0.0.1:5000

## Accounts

- HQ Super Admin: admin / admin1004
- 62 overseas entities: entity code (e.g. 01AR01, 02VN01) / posco1234

Entity accounts are forced to change password on first login.

## Features

- Korean / English UI toggle (top-right KO/EN)
- 62-entity master, CSV/Excel bulk upsert, admin password reset
- Entity self-service for English address, contact emails, phone
- Education program catalog and hybrid invoice creation (manual + Excel)
- Numbering: PGU-YYYY-HALF-SEQ (sequence resets each half-year)
- KRW cost basis to USD/EUR, VAT exempt 0%
- Issue sends an English A4 PDF to entity contact emails
- Entity Acknowledge, HQ Paid posting, reminder resend, CSV export
- Audit log for issue / acknowledge / collection events

If SMTP is not configured, messages are stored in the outbox/ folder.

Environment:
MAIL_ENABLED=true
MAIL_HOST=smtp.office365.com
MAIL_PORT=587
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_FROM=pgu.invoice@posco.com
BANK_ACCOUNT_NO=...
