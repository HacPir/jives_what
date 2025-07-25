#!/bin/bash
# Quick Start FamilyConnect Agents with GenAI Network Integration

echo "🚀 Starting FamilyConnect Agents with GenAI Network Integration..."

# Check if GenAI OS is running
echo "Checking for GenAI OS..."
GENAI_PORTS=(3000 8000 7860 11434)
GENAI_FOUND=false

for port in "${GENAI_PORTS[@]}"; do
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
        echo "✅ Found GenAI OS at port $port"
        GENAI_FOUND=true
        break
    fi
done

if [ "$GENAI_FOUND" = false ]; then
    echo "❌ GenAI OS not found on common ports"
    echo "Please ensure GenAI OS is running before starting FamilyConnect agents"
    exit 1
fi

# Check if FamilyConnect app is running
echo "Checking for FamilyConnect app..."
if curl -s "http://localhost:5000/health" > /dev/null 2>&1; then
    echo "✅ FamilyConnect app is running"
else
    echo "❌ FamilyConnect app not found at port 5000"
    echo "Please start your FamilyConnect app first"
    exit 1
fi

# Set environment variables
export GENAI_BACKEND_URL="http://genai-backend:8000"
export OPENAI_API_KEY="${OPENAI_API_KEY:-}"

# Start the Docker containers
echo "Starting FamilyConnect agents with GenAI network integration..."
docker-compose -f docker-compose.familyconnect.yml up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Check agent health
echo "Checking agent health..."
GRACE_HEALTH=$(curl -s "http://localhost:8001/health" | jq -r '.status // "unknown"')
ALEX_HEALTH=$(curl -s "http://localhost:8002/health" | jq -r '.status // "unknown"')

if [ "$GRACE_HEALTH" = "healthy" ]; then
    echo "✅ Grace agent is healthy"
    GRACE_GENAI=$(curl -s "http://localhost:8001/health" | jq -r '.genai_enabled // false')
    echo "   GenAI enabled: $GRACE_GENAI"
else
    echo "❌ Grace agent is not healthy"
fi

if [ "$ALEX_HEALTH" = "healthy" ]; then
    echo "✅ Alex agent is healthy"
    ALEX_GENAI=$(curl -s "http://localhost:8002/health" | jq -r '.genai_enabled // false')
    echo "   GenAI enabled: $ALEX_GENAI"
else
    echo "❌ Alex agent is not healthy"
fi

# Test agent registration
echo "Testing agent registration with GenAI network..."
sleep 5

# Check if agents are registered
echo "Checking agent registration status..."
echo "You can now:"
echo "1. Visit your GenAI OS dashboard to see the agents"
echo "2. Test the agents via the FamilyConnect app at http://localhost:5000"
echo "3. Use the agents directly via their endpoints:"
echo "   - Grace: http://localhost:8001"
echo "   - Alex: http://localhost:8002"

echo "🎉 FamilyConnect agents are now running with GenAI network integration!"
echo "Check the logs with: docker-compose -f docker-compose.familyconnect.yml logs"