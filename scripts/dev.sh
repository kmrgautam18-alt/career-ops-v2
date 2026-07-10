#!/bin/bash

BASE_URL="http://localhost:8000"

EMAIL="admin@test.com"
PASSWORD="Admin123@"

login() {

    TOKEN=$(curl -s \
        -X POST "$BASE_URL/api/v1/auth/login" \
        -H "Content-Type: application/json" \
        -d "{
            \"email\":\"$EMAIL\",
            \"password\":\"$PASSWORD\"
        }" | jq -r '.data.access_token')

    if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
        echo "❌ Login failed"
        return 1
    fi

    export TOKEN

    echo "✅ Login successful"
}

token() {
    echo "$TOKEN"
}

me() {

    curl \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/users/me"

    echo
}

resumes() {

    curl \
    -H "Authorization: Bearer $TOKEN" \
    "$BASE_URL/api/v1/resumes"

    echo
}

upload_resume() {

    curl \
    -H "Authorization: Bearer $TOKEN" \
    -F "title=$2" \
    -F "file=@$1" \
    "$BASE_URL/api/v1/resumes/upload"

    echo
}

download_resume() {

    curl \
    -H "Authorization: Bearer $TOKEN" \
    -o downloaded.pdf \
    "$BASE_URL/api/v1/resumes/$1/download"

    echo
}

preview_resume() {

    curl \
    -H "Authorization: Bearer $TOKEN" \
    -o preview.pdf \
    "$BASE_URL/api/v1/resumes/$1/preview"

    echo
}

rebuild() {
    podman build -t career-ops:latest .
}

restart() {
    podman stop career-ops 2>/dev/null
    podman rm career-ops 2>/dev/null

    podman run -d \
      --name career-ops \
      --network careerops-network \
      --env-file .env \
      -p 8000:8000 \
      localhost/career-ops:latest
}