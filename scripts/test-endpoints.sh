#!/bin/bash
# ==============================================================================
# Script: test-endpoints.sh
# Description: End-to-end integration test script for CRM Core Service APIs.
#              Tests /health, POST /clients/, and GET /clients/{client_id}.
#
# Prerequisites:
#   - Ensure services are running via docker-compose:
#       docker compose up -d
#   - Ensure curl is installed in your environment.
#
# Execution:
#   chmod +x ./scripts/test-endpoints.sh
#   ./scripts/test-endpoints.sh
#
# Custom Base URL (optional):
#   BASE_URL="http://localhost:8000" ./scripts/test-endpoints.sh
# ==============================================================================

set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "=================================================="
echo "Starting CRM Service API Endpoint Tests"
echo "Target Base URL: ${BASE_URL}"
echo "=================================================="

# ------------------------------------------------------------------------------
# 1. Health Check Endpoint (/health)
# ------------------------------------------------------------------------------
echo ""
echo "[Step 1/3] Testing GET /health endpoint..."

HEALTH_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "${BASE_URL}/health")
HEALTH_BODY=$(echo "${HEALTH_RESPONSE}" | sed '$d')
HEALTH_STATUS=$(echo "${HEALTH_RESPONSE}" | tail -n1 | sed 's/HTTP_STATUS://')

if [ "${HEALTH_STATUS}" -ne 200 ]; then
    echo "ERROR: Health check failed with status ${HEALTH_STATUS}"
    echo "Response: ${HEALTH_BODY}"
    exit 1
fi

echo "SUCCESS: Health check passed (HTTP 200). Response: ${HEALTH_BODY}"

# ------------------------------------------------------------------------------
# 2. Create Client Endpoint (POST /clients/)
# ------------------------------------------------------------------------------
echo ""
echo "[Step 2/3] Testing POST /clients/ endpoint..."

# Generate a random coach UUID or use a standard test UUID
TEST_COACH_ID="a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d"
TEST_TIMESTAMP=$(date +%s)
TEST_EMAIL="test.client.${TEST_TIMESTAMP}@example.com"

CLIENT_PAYLOAD=$(cat <<EOF
{
  "coach_id": "${TEST_COACH_ID}",
  "first_name": "Alexander",
  "last_name": "Hamilton",
  "email": "${TEST_EMAIL}",
  "phone_number": "+12025550143",
  "notes": "Initial coaching consultation client."
}
EOF
)

CREATE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" \
    -X POST "${BASE_URL}/clients/" \
    -H "Content-Type: application/json" \
    -d "${CLIENT_PAYLOAD}")

CREATE_BODY=$(echo "${CREATE_RESPONSE}" | sed '$d')
CREATE_STATUS=$(echo "${CREATE_RESPONSE}" | tail -n1 | sed 's/HTTP_STATUS://')

if [ "${CREATE_STATUS}" -ne 201 ]; then
    echo "ERROR: Failed to create client. HTTP Status: ${CREATE_STATUS}"
    echo "Response: ${CREATE_BODY}"
    exit 1
fi

echo "SUCCESS: Client created successfully (HTTP 201)."
echo "Response: ${CREATE_BODY}"

# Extract client ID from response JSON
if command -v jq >/dev/null 2>&1; then
    CLIENT_ID=$(echo "${CREATE_BODY}" | jq -r '.id')
elif command -v python3 >/dev/null 2>&1; then
    CLIENT_ID=$(echo "${CREATE_BODY}" | python3 -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
elif command -v python >/dev/null 2>&1; then
    CLIENT_ID=$(echo "${CREATE_BODY}" | python -c "import sys, json; print(json.load(sys.stdin).get('id', ''))")
else
    CLIENT_ID=$(echo "${CREATE_BODY}" | grep -o '"id":"[^"]*' | cut -d'"' -f4)
fi

if [ -z "${CLIENT_ID}" ] || [ "${CLIENT_ID}" = "null" ]; then
    echo "ERROR: Could not extract client 'id' from response."
    exit 1
fi

echo "Extracted Client ID: ${CLIENT_ID}"

# ------------------------------------------------------------------------------
# 3. Retrieve Client by ID (GET /clients/{client_id})
# ------------------------------------------------------------------------------
echo ""
echo "[Step 3/3] Testing GET /clients/${CLIENT_ID} endpoint..."

GET_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" "${BASE_URL}/clients/${CLIENT_ID}")
GET_BODY=$(echo "${GET_RESPONSE}" | sed '$d')
GET_STATUS=$(echo "${GET_RESPONSE}" | tail -n1 | sed 's/HTTP_STATUS://')

if [ "${GET_STATUS}" -ne 200 ]; then
    echo "ERROR: Failed to retrieve client by ID. HTTP Status: ${GET_STATUS}"
    echo "Response: ${GET_BODY}"
    exit 1
fi

echo "SUCCESS: Client retrieved successfully (HTTP 200)."
echo "Response: ${GET_BODY}"

echo ""
echo "=================================================="
echo "All CRM Service API endpoint tests passed!"
echo "=================================================="
exit 0
