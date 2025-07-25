#!/bin/bash
# Register FamilyConnect agents with GenAI OS

echo "🚀 Registering FamilyConnect agents with GenAI OS..."

# Test if GenAI OS is running
GENAI_PORTS=(3000 8000 7860 11434)
GENAI_URL=""

for port in "${GENAI_PORTS[@]}"; do
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
        GENAI_URL="http://localhost:$port"
        echo "✅ Found GenAI OS at $GENAI_URL"
        break
    fi
done

if [ -z "$GENAI_URL" ]; then
    echo "❌ GenAI OS not found on common ports"
    echo "Please ensure GenAI OS is running and accessible"
    exit 1
fi

# Register Grace agent
echo "Registering Grace agent..."
curl -X POST "$GENAI_URL/api/agents/register" \
    -H "Content-Type: application/json" \
    -d @grace-agent-manifest.json

# Register Alex agent  
echo "Registering Alex agent..."
curl -X POST "$GENAI_URL/api/agents/register" \
    -H "Content-Type: application/json" \
    -d @alex-agent-manifest.json

echo "✅ Registration complete!"
echo "Your FamilyConnect agents should now appear in the GenAI OS dashboard"
