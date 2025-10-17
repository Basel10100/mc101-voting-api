# MC101 Postman Testing Guide

This guide shows you exactly how to run the complete Postman chain test for the MC101 Notes & Voting API.

## Prerequisites

- Docker and Docker Compose installed
- Postman installed
- Git for version control

## Step 1: Start the API Services

From the project root directory, run:

```bash
# Validate Docker Compose configuration
docker compose config

# Start all services (FastAPI, PostgreSQL, Nginx, backup cron)
docker compose up --build
```

Wait until you see logs indicating services are healthy. You should see:
- `voting_app` container running on port 8000
- `voting_db` (PostgreSQL) running
- `nginx` reverse proxy on ports 80/443

## Step 2: Verify API is Running

Test the health endpoint:

```bash
curl -sS http://localhost:8000/health | jq .
```

Expected response:
```json
{
  "message": "The service is up and running!",
  "status": 200
}
```

Visit the API docs at: http://localhost:8000/mc101docs

## Step 3: Import Postman Environment

1. Open Postman
2. Click the gear icon ⚙️ (top right) or go to "Environments" in the sidebar
3. Click "Import"
4. Select the file: `mc101-env.json` (from project root)
5. After import, select "MC101 Notes & Voting - Local" as your active environment (dropdown at top right)

## Step 4: Import Postman Collection

1. In Postman, go to "Collections" (left sidebar)
2. Click "Import"
3. Select the file: `MC101-Collection.postman_collection.json`
4. You'll see "MC101 Notes & Voting API - Full Chain" in your collections

## Step 5: Configure Environment Variables

Make sure these variables are set in your active environment:

- `baseUrl`: http://localhost:8000
- `email`: Siamak.khatami@kristiania.no
- `name`: Test User
- `password`: TestPass123!
- `newPassword`: NewPass123!
- `notePassword`: MyNoteSecret!

## Step 6: Run the Collection

### Method A: Using Postman Collection Runner (GUI)

1. Right-click the collection "MC101 Notes & Voting API - Full Chain"
2. Select "Run collection"
3. In the Collection Runner window:
   - Ensure "MC101 Notes & Voting - Local" environment is selected
   - Keep iterations = 1
   - Click "Run MC101 Notes & Voting API - Full Chain"
4. Watch all 11 requests execute in sequence
5. Verify all tests pass (green checkmarks)

### Method B: Using Newman (CLI)

Install Newman if not already installed:

```bash
npm install -g newman
```

Run the collection:

```bash
newman run MC101-Collection.postman_collection.json \
  -e mc101-env.json \
  -r json,cli \
  --reporter-json-export postman-results/newman-run-$(date +%Y%m%d-%H%M%S).json
```

## Step 7: Export Test Results

### From Postman Runner:

1. After the run completes, click "Export Results" button
2. Save the file as: `postman-run-Siamak.khatami@kristiania.no-YYYYMMDD.json`
3. Move it to the `postman-results/` folder in the project

### From Newman:

Results are automatically saved to `postman-results/` directory.

## Step 8: Commit Results to Repository

```bash
# Add the results file
git add postman-results/postman-run-*.json

# Commit
git commit -m "Add Postman chain test results for Siamak.khatami@kristiania.no"

# Push to remote
git push
```

## Test Sequence (Chain Order)

The collection runs these requests in order:

1. **Register User** - Create new user with Siamak.khatami@kristiania.no
2. **Login User** - Get JWT token
3. **Get User Info** - Verify token works and user data
4. **Update User** - Change user name
5. **Create Note (App-level)** - Note with app-level encryption
6. **Get Note (App-level)** - Verify auto-decryption
7. **Create Note (Personal)** - Note with personal password encryption
8. **Get Note (Personal)** - Decrypt with password
9. **Update Note** - Switch app-level note to personal encryption
10. **Change Password** - Update user password
11. **Delete User** - Remove user account

## Expected Test Results

All requests should return:
- ✅ Correct status codes (201, 200, 204)
- ✅ Expected response structure
- ✅ Response time < 2000ms
- ✅ Token captured and reused across requests
- ✅ Note IDs captured for subsequent operations

## Troubleshooting

### Services not starting

```bash
# Check logs
docker compose logs -f

# Restart services
docker compose down
docker compose up --build
```

### Connection refused errors

Verify `baseUrl` in Postman environment matches your running instance:
- Local dev: http://localhost:8000
- Docker: http://localhost:8000
- Nginx TLS: https://localhost

### JWT token errors

Re-run the Login request manually and verify the token is saved to `{{token}}` variable.

### Personal note decryption fails

Ensure the `password` query parameter matches the password used during note creation (stored in `{{notePassword}}`).

## Additional Resources

- API Documentation: http://localhost:8000/mc101docs
- Nginx Configuration: `nginx/nginx.conf`
- Environment Variables: `.env`
- Docker Compose: `docker-compose.yml`

## Contact

For issues with this test suite, contact the development team or refer to the project README.
