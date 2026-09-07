# Bosque County Night Sky Forum

A privacy-conscious, moderated Flask starter site for collecting community observations about outdoor lighting, glare, skyglow, and related concerns across Bosque County, Texas, including observations concerning the Lhoist Clifton Lime Plant.

## Important framing

This is an independent community forum, not an official government or regulatory site. The site is intentionally worded to collect observations and evidence without presenting unverified allegations as established facts.

## Privacy model

- The submission form does not request a name, email address, or phone number.
- The application does not intentionally save submitter IP addresses in its SQLite database.
- A hosting company, reverse proxy, CDN, DNS provider, firewall, or network provider may still retain connection/access logs. Do not promise guaranteed anonymity unless you have reviewed the hosting configuration and provider policies.
- Do not add analytics, advertising pixels, social-login buttons, embedded third-party forms, or unnecessary trackers if submitter privacy is a priority.

## Run locally

1. Install Python 3.11+.
2. In this folder: `python -m venv .venv`
3. Activate the virtual environment.
4. `pip install -r requirements.txt`
5. Set strong environment variables:
   - `ADMIN_PASSWORD` — long unique moderator password
   - `SECRET_KEY` — long random secret
6. Run `python app.py`
7. Visit http://127.0.0.1:5000
8. Moderator login: http://127.0.0.1:5000/admin/login

Do **not** deploy with the default `change-this-password` value.

## Before public deployment

Use HTTPS, a production WSGI server, CSRF protection, rate limiting, backups, a privacy notice tailored to the chosen host, and a moderation/correction policy. Consider obtaining legal advice before publishing serious allegations about identifiable people or organizations.

## Current public-record references used for site framing

- TCEQ records identify the Lhoist Clifton Lime Plant in Bosque County and its air-permitting record.
- Texas Local Government Code Chapter 240 contains specific outdoor-lighting regulatory authority for counties. Local applicability should be verified rather than assumed.
