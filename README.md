# Pre-requisites
## Conda
Venv => You can not choose the python version.
We use poetry for package management. Poetry builds up its package upon a virtual environment. We can use either of Venv or Conda. Conda give us the ability to choose the python version regardless of our default python. 
## Poetry
Before using poetry, ensure you have activated the intended python version either by using that or by using conda.
### Poetry commands
`poetry init`: Inits a poetry for the project
`poetry install`: Installs the poetry based on the initialized setup with `poetry init` command and updates the `poetry.lock` file.
`poetry update`: Updates the env if any package is added but not installed as well as updating the new compatible versions. 
`poetry add PACKAGE_NAME`: Adds a package
`poetry remove PACKAGE_NAME`: Removes a package
`poetry export -f requirements.txt --output requirements.txt --without-hashes`: Exports all packages with their versions into the requirements.txt file.

Ensure poetry can export requirements and the plugin is installed.
`poetry self add poetry-plugin-export`

# Project: A Voting system

We are going to simulate a small voting system in which users can vote to their candidates after authentication.
This session is only about authentication.

## MC101 Notes & Voting API (Microservices)

This app provides:
- User auth via OAuth2 JWT (register, login, logout, change password, update profile)
- Encrypted personal notes (AES-GCM) with two modes:
	- Personal encryption: user supplies a password; required again for decrypt
	- App-level encryption: uses app secret; decrypted automatically on read
- Voting sample (candidates, votes, vote counts)
- PostgreSQL via SQLAlchemy ORM
- Nginx reverse proxy with TLS, rate limiting, and security headers
- Hourly Postgres backups (7-day retention) via a cron container

### Services
- voting_app: FastAPI app (Uvicorn)
- voting_db: PostgreSQL 15
- nginx: reverse proxy, TLS, rate limit
- db_backup_cron: hourly backups to ./backups

### Setup
1) Copy the env example and set secrets
```
cp example.env.txt .env
# Edit .env: set JWT_SECRET_KEY and APP_ENCRYPTION_KEY to strong secrets
```

2) Start the stack
```
docker compose up --build
```

3) Open API docs
- https://localhost/mc101docs

### Endpoints (high level)
- Auth
	- POST /users/register
	- POST /users/login
	- POST /users/logout
	- POST /users/change-password
	- GET  /users/info
	- PATCH /users/
	- DELETE /users/
- Notes
	- POST /users/notes  (body: title, content, personal_encryption, password?)
	- GET  /users/notes/{note_id}?password=...
	- PATCH /users/notes/{note_id}  (can update title/content and switch encryption)
- Voting (sample)
	- POST /admin/candidate
	- GET  /admin/votes/all-candidates/count
	- POST /users/vote

### Security
- OAuth2PasswordBearer for JWT
- Nginx rate limiting 5r/s with small burst
- Security headers (CSP, XFO, XCTO, Referrer-Policy)
- Data-at-rest: Notes encrypted (AES-GCM + PBKDF2-HMAC), salts and nonces stored per note

### Backups
Backups are written hourly to ./backups/ and pruned after 7 days.

### Dev/Test locally
Use TestClient from tests/ as reference. To run pytest, install dev deps:
```
pip install -r requirements.txt pytest
pytest -q
```

