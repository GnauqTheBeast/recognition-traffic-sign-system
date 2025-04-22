#!/bin/bash

# exit if error
set -e

SERVICES=(
  "api_gateway"
  "user_service"
  "traffic_sign_service"
  "eureka_server"
)

echo "👉 Start build Spring Boot service..."

for SERVICE in "${SERVICES[@]}"; do
  echo "🔨 Build: $SERVICE"
  (cd "$SERVICE" && mvn clean install -DskipTests)
done

echo "✅ Build successfully."

echo "🐳 Starting Docker Compose..."
docker compose up --build -d

echo "🚀 Deploy successfully!"
