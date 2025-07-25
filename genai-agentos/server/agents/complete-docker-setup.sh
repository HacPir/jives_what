#!/bin/bash

echo "🚀 Complete Docker Setup for GenAI Integration"
echo "=============================================="

# Step 1: Start Docker agents
echo "Step 1: Starting Docker agents..."
chmod +x docker-start.sh
./docker-start.sh

# Step 2: Wait for agents to be fully ready
echo "Step 2: Waiting for agents to stabilize..."
sleep 15

# Step 3: Register with GenAI software
echo "Step 3: Registering agents with GenAI software..."
python3 genai-integration.py

# Step 4: Final verification
echo "Step 4: Final verification..."
echo ""
echo "🔍 Agent Status:"
docker-compose ps

echo ""
echo "📊 Agent Health:"
curl -s http://localhost:8001/health | python3 -m json.tool 2>/dev/null || echo "Grace agent not responding"
curl -s http://localhost:8002/health | python3 -m json.tool 2>/dev/null || echo "Alex agent not responding"

echo ""
echo "🎯 Your GenAI software should now show:"
echo "   - Grace Agent (elderly companion)"
echo "   - Alex Agent (family coordinator)"
echo "   - Both with OpenAI-compatible endpoints"

echo ""
echo "📋 Next Steps:"
echo "   1. Open your GenAI dashboard"
echo "   2. Look for the registered agents"
echo "   3. Test communication with them"
echo "   4. Use them in your applications"

echo ""
echo "🛠️  Troubleshooting:"
echo "   - View logs: docker-compose logs grace-agent"
echo "   - View logs: docker-compose logs alex-agent"
echo "   - Restart: docker-compose restart"
echo "   - Stop: docker-compose down"