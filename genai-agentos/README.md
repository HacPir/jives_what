# W.H.A.T. (We Have Another Time)
## LeadWithAI Hackathon 2025 Submission

A professional multi-agent AI system that reconnects families across generations through intelligent care coordination, featuring Grace (elderly companion) and Alex (family coordinator) agents with integrated voice interfaces, sleep scheduling, and digital picture frames.

[Watch the video](https://youtu.be/cpmVossJ_bA?feature=shared)

## 🎯 Project Overview

W.H.A.T.T (When Home Asks To Talk) bridges the gap between elderly users and their families through intelligent AI agents that provide emotional support, coordinate care, and facilitate meaningful connections. Built for the LeadWithAI Hackathon 2025.

### Core Features
- **Grace Agent**: Warm, patient AI companion designed for elderly users with voice-first interaction
- **Alex Agent**: Family coordinator focused on caregivers and care planning
- **Voice Interface**: Browser-based speech recognition and synthesis for accessibility
- **Care Coordination**: Automatic family notifications for medical appointments and assistance needs
- **Sleep Schedule**: Personalized bedtime routines with binaural beats for brain stimulation
- **Digital Picture Frame**: Family photo sharing to connected devices with auto-rotation
- **Inter-Agent Communication**: Sophisticated agent-to-agent messaging for coordinated care
- **PostgreSQL Database**: Full data persistence for conversations, family connections, and care records

### Technology Stack
- **Frontend**: React 18 + TypeScript + Tailwind CSS
- **Backend**: Node.js + Express + WebSocket support
- **Database**: PostgreSQL with Drizzle ORM
- **AI Integration**: OpenAI GPT-4 with local fallback system
- **Voice**: Browser Web Speech API
- **Real-time**: WebSocket for live family updates

## 🚀 Quick Start (Hackathon Demo)

### Prerequisites
- Node.js 18+ 
- Modern web browser with microphone access (required for voice features)
- OpenAI API key (for full AI functionality)

### Installation & Demo

1. **Clone and install**
   ```bash
   git clone <repository-url>
   cd whatt-ai
   npm install
   ```

2. **Environment setup**
   ```bash
   # Optional: Add OpenAI API key for enhanced AI responses
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   # System works with local AI fallback if no API key provided
   ```

3. **Start the application**
   ```bash
   npm run dev
   ```

4. **Demo the system**
   - **Main Landing**: `http://localhost:5000` - Professional brand showcase
   - **Grace Interface**: `http://localhost:5000/grace` - Elderly companion demo
   - **Alex Dashboard**: `http://localhost:5000/alex` - Family coordinator demo
   - **Calendar View**: `http://localhost:5000/calendar` - Family scheduling system

### Demo Features
- **Voice Interaction**: Click microphone buttons and speak naturally
- **Agent Communication**: See real-time inter-agent messaging
- **Care Coordination**: Demo medical appointment scheduling
- **Sleep Schedules**: Test binaural beats and music preferences
- **Digital Picture Frame**: Family photo sharing demonstration
- **Sample Data**: Pre-populated family connections and conversations for immediate testing

## 🏗️ Technical Architecture

### Development Philosophy
This project prioritizes **rapid prototyping** and **user experience** over complex deployment infrastructure. While Docker configurations exist in the repository (`familyconnect-agents/` directory), the current implementation focuses on a **streamlined single-server architecture** that's ideal for hackathon demonstrations and development.

### Current Architecture (Hackathon-Optimized)

#### Frontend (React + TypeScript)
- **Framework**: React 18 with TypeScript for type safety
- **Routing**: Wouter for lightweight client-side routing  
- **State Management**: TanStack Query for server state, React Context for UI state
- **UI Components**: Radix UI primitives with shadcn/ui design system
- **Styling**: Tailwind CSS with custom themes optimized for elderly users
- **Voice**: Browser Web Speech API for recognition and synthesis
- **Real-time**: WebSocket client for live family updates
- **Build Tool**: Vite for fast development and production builds

#### Backend (Node.js + Express)
- **Runtime**: Node.js with Express.js server
- **Language**: TypeScript with ES modules for full-stack type safety
- **API**: RESTful endpoints with TypeScript validation using Zod
- **Database**: PostgreSQL with Drizzle ORM for type-safe queries
- **AI Integration**: OpenAI GPT-4 with intelligent local fallback system
- **WebSocket**: Real-time communication for family status updates
- **Voice Processing**: Browser-based audio processing (no server dependencies)

### Key Features

#### 🤖 AI Agent System
- **Grace Agent**: Elderly companion with warm, patient personality
- **Alex Agent**: Family coordinator for caregivers and planning
- **Inter-Agent Communication**: Coordinated messaging between agents
- **Emotional State Tracking**: AI monitors and responds to emotional context
- **Memory Formation**: Conversations create lasting family memories

#### 🏥 Care Coordination
- **Medical Appointments**: Automatic family notifications
- **Assistance Coordination**: Transportation and support needs
- **Priority Levels**: Urgency classification (low, normal, high, emergency)
- **Care Provider Integration**: Facility details and provider information
- **Real-time Notifications**: Immediate family updates

#### 😴 Sleep Schedule & Brain Stimulation
- **Personalized Schedules**: Customizable bedtime with duration settings
- **Binaural Beats**: Real-time audio generation using Web Audio API
- **Brain Wave Frequencies**: Delta (4Hz), Theta (8Hz), Alpha (10Hz), Beta (14Hz), Gamma (40Hz)
- **Music Integration**: Nature sounds, classical, instrumental playlists
- **Sleep Goals**: Deep sleep, memory consolidation, relaxation
- **Volume Control**: Adjustable audio with real-time preview

#### 📸 Digital Picture Frame
- **Auto-Rotating Display**: Customizable timing (5-120 seconds per photo)
- **Smart Controls**: Play/pause, manual navigation, photo counter
- **Brightness Control**: Adjustable brightness for optimal viewing
- **Smooth Transitions**: Fade effects with caption overlays
- **Real-time Sync**: WebSocket notifications for instant updates
- **Family Engagement**: Easy photo sharing tools

## 📁 Project Structure

```
whatt-ai/
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── hooks/          # Custom React hooks  
│   │   ├── lib/            # Utility functions
│   │   ├── pages/          # Route components
│   │   └── App.tsx         # Main app component
│   └── index.html          # HTML template
├── server/                 # Express backend
│   ├── services/           # Business logic
│   ├── index.ts           # Server entry point
│   ├── routes.ts          # API routes
│   ├── storage.ts         # Data storage layer
│   └── vite.ts            # Vite integration
├── shared/                 # Shared types and schemas
│   └── schema.ts          # Database schema and types
├── familyconnect-agents/   # Docker agents (reference only)
│   ├── standalone_grace_agent.py
│   ├── standalone_alex_agent.py
│   └── docker-compose.familyconnect.yml
├── components.json         # shadcn/ui configuration
├── package.json           # Dependencies and scripts
├── README.md              # This file
└── replit.md              # Project context and architecture
```

## 🐳 Docker Configuration (Reference Only)

The `familyconnect-agents/` directory contains Docker configurations for deploying Grace and Alex as standalone agents with GenAI OS integration. **These files are maintained for reference** but the current hackathon implementation prioritizes a **streamlined single-server architecture** for faster development and demonstration.

### Why We Moved Away from Docker
- **Hackathon Speed**: Single-server setup allows for rapid iteration and testing
- **Simplified Deployment**: No container orchestration complexity for demos
- **Development Focus**: Easier debugging and feature development
- **Resource Efficiency**: Lower resource usage for demonstration purposes

### Docker Files Available
- `standalone_grace_agent.py` - Grace agent with GenAI protocol compatibility
- `standalone_alex_agent.py` - Alex agent with GenAI protocol compatibility  
- `docker-compose.familyconnect.yml` - Container orchestration configuration
- Integration scripts for GenAI OS dashboard connectivity

## 🏆 Hackathon Highlights

### Innovation Points
- **Multi-Agent AI System**: Sophisticated inter-agent communication with priority routing
- **Voice-First Design**: Accessible interface designed specifically for elderly users
- **Real-time Care Coordination**: Automatic family notifications for medical appointments
- **Binaural Beats Integration**: Brain stimulation technology for sleep improvement
- **Professional Branding**: W.H.A.T.T brand identity designed for healthcare market

### Technical Achievements
- **Full-Stack TypeScript**: End-to-end type safety for reliable development
- **OpenAI Integration**: GPT-4 powered conversations with intelligent fallback
- **PostgreSQL Database**: Production-ready data persistence with Drizzle ORM
- **WebSocket Real-time**: Live family updates and agent communications
- **Responsive Design**: Mobile-friendly interface with elderly accessibility features

### Demo Readiness
- **Immediate Setup**: One-command installation and startup
- **Sample Data**: Pre-populated family connections and conversations
- **Voice Interaction**: Working speech recognition and synthesis
- **Live Features**: Real-time agent communication and family updates
- **Professional Presentation**: Production-quality UI with W.H.A.T.T branding

## 🚀 Deployment

### Current Status
The application is optimized for **development deployment** with Replit or similar platforms. The single-server architecture makes it ideal for hackathon demonstrations and rapid prototyping.

### Production Considerations
For production deployment, consider:
- **Database**: PostgreSQL connection (already configured)
- **API Keys**: OpenAI API key for full AI functionality
- **Environment Variables**: Proper secret management
- **Scaling**: Docker configurations available for microservices architecture

### Hackathon Demo
The current implementation is **demo-ready** with:
- Immediate startup on any Node.js environment
- Sample data for instant testing
- Local AI fallback for offline demonstrations
- Professional branding and UI ready for presentation

## 🤝 Contributing

This project was built for the LeadWithAI Hackathon 2025. For questions or collaboration opportunities, please reach out through the hackathon platform.

## 📄 License

Built for LeadWithAI Hackathon 2025. All rights reserved.

---

**W.H.A.T. (We Have Another Time)** - *Connecting families through intelligent AI conversation*
