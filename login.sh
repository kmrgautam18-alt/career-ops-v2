#!/bin/bash

TOKEN=$(curl -s \
-X POST http://localhost:8000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
  "email":"admin@test.com",
  "password":"Admin123@"
}' | jq -r '.data.access_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ Login failed"
    return 1
fi

export TOKEN

echo "✅ Login successful"
echo "Token loaded into \$TOKEN"