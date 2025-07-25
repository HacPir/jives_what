#!/bin/bash

echo "📦 Packaging FamilyConnect Agents for Docker Upload"
echo "=================================================="

# Create deployment package
PACKAGE_NAME="familyconnect-agents-docker"
PACKAGE_DIR="/tmp/$PACKAGE_NAME"

# Clean and create package directory
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

# Copy essential files
echo "📋 Copying agent files..."
cp standalone_grace_agent.py "$PACKAGE_DIR/"
cp standalone_alex_agent.py "$PACKAGE_DIR/"
cp requirements.txt "$PACKAGE_DIR/"
cp docker-compose.yml "$PACKAGE_DIR/"
cp Dockerfile.grace "$PACKAGE_DIR/"
cp Dockerfile.alex "$PACKAGE_DIR/"
cp start-docker-agents.sh "$PACKAGE_DIR/"
cp docker-deployment-guide.md "$PACKAGE_DIR/"

# Create README for the package
cat > "$PACKAGE_DIR/README.md" << 'EOF'
# FamilyConnect AI Agents - Docker Package

## Quick Start

1. **Deploy with Docker Compose**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"  # Optional
   docker-compose up --build -d
   ```

2. **Verify Deployment**
   ```bash
   curl http://localhost:8001/health  # Grace Agent
   curl http://localhost:8002/health  # Alex Agent
   ```

3. **Integration**
   - Grace Agent: http://localhost:8001
   - Alex Agent: http://localhost:8002
   - Both agents provide OpenAI-compatible `/v1/chat/completions` endpoints
   - Agents will automatically integrate with your GenAI AgentOS

## Files Included

- `standalone_grace_agent.py` - Complete Grace elderly companion agent
- `standalone_alex_agent.py` - Complete Alex family coordinator agent
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Container orchestration
- `Dockerfile.grace` - Grace agent container
- `Dockerfile.alex` - Alex agent container
- `start-docker-agents.sh` - Quick deployment script
- `docker-deployment-guide.md` - Complete deployment guide

## Agent Capabilities

### Grace Agent (Port 8001)
- Elderly companion with warm, patient personality
- Emotional support and health monitoring
- OpenAI-compatible chat completions

### Alex Agent (Port 8002)
- Family coordinator with professional efficiency
- Care management and family communication
- OpenAI-compatible chat completions

Both agents work with or without OpenAI API keys and provide full integration with GenAI AgentOS systems.
EOF

# Create deployment archive
cd /tmp
tar -czf "$PACKAGE_NAME.tar.gz" "$PACKAGE_NAME/"

echo "✅ Package created: /tmp/$PACKAGE_NAME.tar.gz"
echo ""
echo "📋 Package Contents:"
tar -tzf "$PACKAGE_NAME.tar.gz"
echo ""
echo "🚀 Upload Instructions:"
echo "   1. Upload the $PACKAGE_NAME.tar.gz file to your Docker server"
echo "   2. Extract: tar -xzf $PACKAGE_NAME.tar.gz"
echo "   3. Deploy: cd $PACKAGE_NAME && docker-compose up --build -d"
echo "   4. Test: curl http://localhost:8001/health"
echo ""
echo "🎯 Your agents will then be available at:"
echo "   - Grace Agent: http://localhost:8001"
echo "   - Alex Agent: http://localhost:8002"
echo "   - Both agents provide OpenAI-compatible endpoints"
echo "   - They will auto-integrate with your GenAI AgentOS"