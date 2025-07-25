# Port Configuration for FamilyConnect × GenAI OS Integration

## Port Assignments

### GenAI OS (Original)
- **Frontend Dashboard**: 3000
- **Backend API**: 8000
- **WebSocket Router**: 8080
- **PostgreSQL**: 5432
- **Redis**: 6379

### FamilyConnect Integration
- **Your FamilyConnect App**: 5000 (running in Replit)
- **FamilyConnect Backend Proxy**: 5001 (Docker container)
- **Grace Agent**: 8001 (Docker container)
- **Alex Agent**: 8002 (Docker container)

## No Port Conflicts

The configuration ensures:
- Your FamilyConnect app continues running on port 5000
- GenAI OS dashboard remains on port 3000
- GenAI OS API remains on port 8000
- Grace and Alex agents use separate ports (8001, 8002)
- Optional proxy on port 5001 for Docker networking

## Connection Flow

```
GenAI OS (port 8000) → Grace/Alex Agents (ports 8001/8002) → Your FamilyConnect App (port 5000)
```

## Dashboard Access

- **GenAI OS Dashboard**: http://localhost:3000
- **Your FamilyConnect App**: http://localhost:5000
- **Grace Agent**: http://localhost:8001
- **Alex Agent**: http://localhost:8002

This configuration maintains all original GenAI OS functionality while adding FamilyConnect agents.