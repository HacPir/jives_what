# W.H.A.T.T (When Home Asks To Talk)

## Overview

W.H.A.T.T (When Home Asks To Talk) is a professional full-stack web application that connects elderly users with their family members through AI-powered agents. The system features two distinct AI personalities - Grace (elderly companion) and Alex (family coordinator) - that facilitate meaningful conversations, manage family connections, provide emotional support, and coordinate care activities with family notifications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **Routing**: Wouter for client-side routing
- **State Management**: TanStack Query for server state management
- **UI Components**: Radix UI primitives with shadcn/ui design system
- **Styling**: Tailwind CSS with CSS custom properties for theming
- **Build Tool**: Vite for development and production builds

### Backend Architecture
- **Runtime**: Node.js with Express.js server
- **Language**: TypeScript with ES modules
- **API Pattern**: RESTful APIs with WebSocket support for real-time communication
- **Database**: PostgreSQL with Drizzle ORM
- **AI Integration**: OpenAI API for natural language processing

### Key Components

#### AI Agent System
- **Grace Agent**: Elderly companion with warm, patient personality designed for senior users (genai-protocol compatible)
- **Alex Agent**: Family coordinator focused on caregivers and family management (genai-protocol compatible)
- **Agent Communication**: Inter-agent messaging system for coordinated care with priority-based routing
- **Voice Interface**: Speech recognition and text-to-speech capabilities
- **GenAI Protocol Integration**: True OpenAI-compatible agents with Docker containerization and centralized management

#### Database Schema
- **Users**: Family members with roles (elderly/caregiver) and preferences
- **Conversations**: Chat history with emotional state tracking
- **Family Connections**: Relationship mapping between family members
- **Memories**: Shared family stories and milestones
- **Reminders**: Task management and gentle prompts with care coordination
- **Care Notifications**: Medical appointments and care events with family notifications
- **Agent Communications**: Inter-agent messaging logs

#### Real-time Features
- **WebSocket Server**: Real-time communication for live chat
- **Voice Processing**: Browser-based speech recognition and synthesis
- **Live Updates**: Real-time family status and agent communications

## Data Flow

1. **User Authentication**: Users access agent interfaces based on their role
2. **Agent Selection**: System routes to appropriate AI personality (Grace/Alex)
3. **Conversation Processing**: 
   - User input → AI agent → OpenAI API → Personalized response
   - Emotional state tracking and memory formation
   - Inter-agent communication when needed
4. **Data Persistence**: All interactions stored in PostgreSQL via Drizzle ORM
5. **Real-time Updates**: WebSocket broadcasts for live family status updates

## External Dependencies

### AI Services
- **OpenAI API**: GPT-4 for natural language processing and conversation generation
- **Speech APIs**: Browser-native Web Speech API for voice interactions

### Database
- **Neon Database**: Serverless PostgreSQL hosting
- **Drizzle ORM**: Type-safe database operations with schema migrations

### UI/UX Libraries
- **Radix UI**: Accessible component primitives
- **Tailwind CSS**: Utility-first styling framework
- **Lucide React**: Icon library for consistent UI elements

### Development Tools
- **Vite**: Fast development server and build tool
- **TypeScript**: Type safety across the full stack
- **ESBuild**: Fast JavaScript bundling for production

## Deployment Strategy

### Development Environment
- **Local Development**: Vite dev server with Express backend
- **Hot Reload**: Vite HMR for frontend, tsx for backend file watching
- **Database**: Development database with schema migrations via Drizzle Kit

### Production Build
- **Frontend**: Vite builds React app to static files
- **Backend**: ESBuild bundles Express server for Node.js deployment
- **Database**: PostgreSQL with connection pooling and environment-based configuration

### Environment Configuration
- **Database**: `DATABASE_URL` environment variable for PostgreSQL connection
- **AI Services**: `OPENAI_API_KEY` for OpenAI API access
- **Build Scripts**: Separate dev/build/start scripts for different environments

The application uses a monorepo structure with shared schemas and utilities, enabling type-safe communication between frontend and backend while maintaining clear separation of concerns.

## Recent Changes

### Hackathon Preparation - README Update (January 2025)
Successfully updated project documentation to hackathon standards:

#### Documentation Standards ✅
- **Hackathon Branding**: Updated README.md with LeadWithAI Hackathon 2025 submission header
- **Docker Reference**: Clearly documented that Docker files exist for reference but moved to development-focused approach
- **Demo Instructions**: Added comprehensive demo setup and feature testing instructions
- **Architecture Explanation**: Detailed current hackathon-optimized architecture with rationale for simplified deployment
- **Innovation Highlights**: Added hackathon-specific sections for innovation points and technical achievements
- **Professional Presentation**: Enhanced project structure and deployment sections for hackathon judging

#### Technical Philosophy ✅
- **Development-First**: Prioritized rapid prototyping and user experience over complex deployment infrastructure
- **Hackathon-Optimized**: Streamlined single-server architecture for faster development and demonstration
- **Docker Available**: Maintained Docker configurations in familyconnect-agents/ directory for reference
- **Immediate Demo**: One-command setup with sample data for instant testing and presentation

### Brand Refresh - W.H.A.T.T (January 2025)
Successfully rebranded the application with a professional identity:

#### Professional Branding Implementation ✅
- **Brand Name**: Updated from "FamilyConnect AI" to "W.H.A.T.T (When Home Asks To Talk)"
- **Professional Logo Component**: Created reusable BrandLogo component with consistent styling
- **Header System**: Implemented ProfessionalHeader component for consistent branding across all pages
- **HTML Metadata**: Updated title, description, and SEO tags with new branding
- **User Interface**: Updated all page headers with professional W.H.A.T.T branding
- **Documentation**: Updated README.md and project documentation with new brand identity

#### Brand Identity Guidelines ✅
- **Primary Brand**: "W.H.A.T.T" displayed prominently in bold typography
- **Tagline**: "When Home Asks To Talk" as professional subtitle
- **Icon**: MessageSquare icon representing communication and conversation
- **Color Scheme**: Maintained existing professional color palette with primary/secondary theme
- **Typography**: Bold, clean typography for brand name with smaller tagline
- **Professional Tone**: Emphasized professional AI companion system messaging

### GenAI OS Integration (January 2025)
Successfully integrated W.H.A.T.T agents with GenAI OS Docker setup:

#### GenAI OS Docker Integration ✅
- **Complete GenAI OS Integration**: Created comprehensive Docker-based integration with user's genai-agentos directory
- **Agent Directory Setup**: Pre-configured familyconnect-agents folder with standalone Grace and Alex agents
- **Docker Compose Configuration**: Created docker-compose.familyconnect.yml for seamless container orchestration
- **Automatic Registration**: Agents automatically register with GenAI OS backend on startup
- **Service Discovery**: Proper Docker networking with genai-backend and router services
- **Quick Start Scripts**: One-command integration with quick-start.sh and simple-integration.sh
- **Fixed Import Issues**: Resolved dotenv module errors and GenAI session imports for Docker compatibility

#### Agent Architecture for GenAI OS ✅
- **Standalone Agents**: Grace and Alex agents run as independent Docker containers
- **GenAI Protocol Compliance**: Full compatibility with genai-protocol and GenAI OS agent management
- **Service Endpoints**: Grace (port 8001) and Alex (port 8002) with health checks
- **Backend Proxy**: Nginx proxy for connecting to FamilyConnect app on port 5000
- **Automatic Discovery**: Agents appear in GenAI OS dashboard at http://localhost:3000
- **Docker Network Integration**: Seamless integration with existing local-genai-network

#### Integration Workflow ✅
- **Step 1**: Start FamilyConnect app (port 5000)
- **Step 2**: Start GenAI OS (docker compose up -d)
- **Step 3**: Start FamilyConnect agents (docker compose -f familyconnect-agents/docker-compose.familyconnect.yml up -d)
- **Step 4**: Agents automatically register with GenAI OS
- **Step 5**: Test in GenAI OS dashboard

### GenAI Protocol Agent Integration (January 2025)
Successfully integrated the genai-protocol framework to create true OpenAI-compatible agents:

#### GenAI Protocol Implementation ✅
- **True OpenAI-Compatible Agents**: Implemented Grace and Alex agents using genai-protocol framework with FastAPI endpoints
- **Docker Containerization**: Created comprehensive Docker setup with individual containers for each agent and orchestration
- **Agent Base Class**: Developed shared BaseAgent class inheriting from genai-protocol BaseHandler for consistent agent behavior
- **Local Python Execution**: Agents run as independent Python processes with FastAPI servers on dedicated ports
- **OpenAI API Compatibility**: Full OpenAI v1/chat/completions API compatibility with proper ChatRequest/ChatResponse schemas
- **Intelligent Fallback System**: Local AI responses when OpenAI API unavailable, maintaining agent personalities
- **Enhanced GenAI Capabilities**: Added date/time queries, weather information, translation services, and file reading support
- **WebSocket Sessions**: Full GenAI protocol session support with JWT authentication and WebSocket communication

#### Agent Management System ✅
- **Agent Manager Service**: Centralized coordination system for Grace and Alex agents with health monitoring
- **GenAI Service Integration**: TypeScript service layer for seamless integration with existing FamilyConnect system
- **Multi-Agent Orchestration**: Docker Compose configuration for scalable agent deployment
- **Health Monitoring**: Real-time agent status checking with automatic failover capabilities
- **Inter-Agent Communication**: Sophisticated message routing between agents with priority levels and context preservation
- **Communication Logging**: Comprehensive logging system for all agent interactions and decisions

#### GenAI Dashboard Integration ✅
- **Agent Status Dashboard**: Real-time monitoring of all genai-protocol agents with health indicators
- **Interactive Testing Interface**: Direct communication testing with Grace and Alex agents
- **Inter-Agent Communication Scenarios**: Pre-configured test scenarios for medical concerns, loneliness, and care coordination
- **Communication Log Viewer**: Visual log of all agent interactions with timestamps and context
- **Agent Control Interface**: Start/stop agent management with proper error handling
- **Integration with Alex Dashboard**: Seamless integration with existing family coordinator interface

#### Docker & Deployment Architecture ✅
- **Multi-Container Setup**: Separate containers for Grace, Alex, and Agent Manager with proper networking
- **Health Checks**: Docker health checks for all agent containers with automatic restart policies
- **Python Requirements**: Comprehensive requirements.txt with genai-protocol, FastAPI, and OpenAI dependencies
- **Startup Scripts**: Automated agent startup and shutdown scripts for development and production deployment
- **Environment Configuration**: Proper environment variable handling for OpenAI API keys and port configuration
- **Network Isolation**: Dedicated Docker network for agent communication with proper service discovery

### Advanced AI Agent Intelligence System (January 2025)
Successfully implemented sophisticated AI agent intelligence with OpenAI integration:

#### Intelligent Agent Framework ✅
- **Advanced Agent Intelligence Service**: Created comprehensive agent intelligence system with reasoning, memory, and learning capabilities
- **Multi-layered AI Processing**: Integrated OpenAI GPT-4 for sophisticated agent-to-agent communication and decision-making
- **Agent Memory System**: Implemented short-term and long-term memory for both Grace and Alex agents
- **Reasoning Engine**: Added complex decision-making with pros/cons analysis, confidence levels, and evidence-based choices
- **Pattern Recognition**: Agents now learn from interactions and adapt responses based on user patterns
- **Strategic Planning**: Agents create detailed action plans with responsibilities and follow-up protocols

#### OpenAI Integration Enhancement ✅
- **True Agent Intelligence**: Leveraged OpenAI's advanced reasoning for sophisticated agent-to-agent conversations
- **Context-Aware Responses**: Agents now provide detailed analysis of situations with multiple response options
- **Emotional Intelligence**: Enhanced emotional state detection and appropriate response generation
- **Care Coordination AI**: Intelligent prioritization of care needs with family notification automation
- **Fallback System**: Maintains local AI simulation when OpenAI API is unavailable

#### Agent Intelligence Dashboard ✅
- **Real-time Intelligence Visualization**: Live dashboard showing agent reasoning processes and decision-making
- **Simulation Testing**: Interactive scenarios to test agent intelligence with medical concerns, loneliness, and emergencies
- **Reasoning Process Display**: Visual representation of agent analysis, options evaluation, and decision rationale
- **Memory & Learning Tracking**: Dashboard showing agent memory patterns and learning effectiveness
- **Confidence Metrics**: Visual indicators of agent confidence levels and decision certainty

#### Advanced Inter-Agent Communication ✅
- **Sophisticated Agent Coordination**: Agents now engage in complex reasoning before communicating with each other
- **Priority-Based Communication**: Intelligent prioritization of communications based on urgency and emotional context
- **Action Planning**: Detailed step-by-step plans with timeframes and responsibility assignments
- **Follow-up Protocols**: Automated follow-up systems to ensure care continuity
- **Real-time Intelligence Updates**: WebSocket-based real-time updates for agent intelligence dashboard

### Bug Fixes and Error Handling (January 2025)
Successfully resolved critical stability issues and improved error handling:

#### System Stability Improvements ✅
- **Fixed Digital Picture Frame API Calls**: Resolved excessive API calls by removing mutation from useEffect dependency array
- **Database Query Fix**: Fixed PostgreSQL syntax error in conversations queries by correcting column references  
- **WebSocket Error Handling**: Added proper connection state checks and error handling for WebSocket communications
- **Voice Service Improvements**: Enhanced error handling for speech recognition and synthesis with proper logging
- **Global Error Handlers**: Added unhandled promise rejection handlers to prevent console errors
- **Server Error Management**: Improved Express error handling to prevent re-throwing after responses sent

#### OpenAI Integration Status ✅
- **API Key Configuration**: Successfully configured OpenAI API key environment variable
- **Quota Management**: OpenAI API key has reached rate limits, system automatically falls back to local AI simulation
- **Local AI Fallback**: Local AI simulation working correctly when OpenAI API unavailable
- **Agent Communication**: Both Grace and Alex agents responding properly with appropriate personalities

### PostgreSQL Database Migration (January 2025)
Successfully migrated from in-memory storage to PostgreSQL for full data persistence:

#### Database Implementation ✅
- **PostgreSQL Integration**: Full database configuration with Neon serverless PostgreSQL
- **Schema Migration**: Complete database schema using Drizzle ORM with all tables created
- **Data Persistence**: All user data, conversations, family connections, and media now persisted
- **Sample Data**: Comprehensive sample data for immediate testing and demonstration
- **API Compatibility**: All existing APIs updated to work with PostgreSQL storage
- **Error Handling**: Proper error handling and data validation for database operations

#### Database Tables ✅
- **Users**: Family members with roles and preferences
- **Conversations**: AI agent chat history with emotional state tracking
- **Family Connections**: Relationship mapping between elderly and caregiver users
- **Memories**: Shared family stories and milestones
- **Reminders**: Task management and gentle prompts
- **Care Notifications**: Medical appointments and care events with family notifications
- **Agent Communications**: Inter-agent messaging logs
- **Sleep Schedules**: Binaural beats and music preferences
- **Picture Frames**: Digital photo display configuration
- **Family Photos**: Photo sharing with captions and metadata

#### Technical Implementation ✅
- **Database Storage Class**: Complete DatabaseStorage implementation adhering to IStorage interface
- **Query Optimization**: Efficient database queries using Drizzle ORM with proper indexing
- **Data Initialization**: Automatic sample data creation for new databases
- **Connection Management**: Proper database connection pooling and error handling
- **Migration System**: Drizzle Kit for schema migrations and updates

### Complete System Implementation (January 2025)
FamilyConnect AI is now a fully functional multi-agent system with comprehensive elderly care features:

### Core AI Agent System ✅
- **Grace Agent**: Elderly companion with warm, patient personality for senior users
- **Alex Agent**: Family coordinator focused on caregivers and family management
- **Inter-Agent Communication**: Coordinated messaging system between agents
- **Voice Interface**: Speech recognition and text-to-speech capabilities
- **Emotional State Tracking**: AI monitors and responds to emotional context
- **Memory Formation**: Conversations create lasting family memories

### Care Coordination System ✅
- **Medical Appointment Management**: Automatic family notifications for care events
- **Assistance Coordination**: System recognizes when family help is needed
- **Real-time Notifications**: Immediate updates to family members about care needs
- **Priority Levels**: Urgency classification (low, normal, high, emergency)
- **Care Provider Integration**: Support for facility details and provider information
- **Transportation Coordination**: Automatic detection of transportation needs
- **Demonstration Interface**: Full demo functionality in Alex dashboard

### Sleep Schedule & Brain Stimulation System ✅
- **Personalized Sleep Schedules**: Customizable bedtime with duration settings
- **Binaural Beats Generator**: Real-time audio generation using Web Audio API
- **Brain Wave Frequencies**: Delta (4Hz), Theta (8Hz), Alpha (10Hz), Beta (14Hz), Gamma (40Hz)
- **Familiar Music Integration**: Nature sounds, classical, instrumental, and custom playlists
- **Sleep Goals**: Deep sleep, memory consolidation, and relaxation targeting
- **Volume Control**: Adjustable volume with real-time audio preview
- **Headphone Optimization**: Designed for optimal binaural beat experience
- **Grace Integration**: Easy access sleep schedule interface for elderly users

### Digital Picture Frame System ✅
- **Auto-Rotating Photo Display**: Customizable timing (5-120 seconds per photo)
- **Smart Controls**: Play/pause, manual navigation, and photo counter
- **Brightness Control**: Adjustable brightness slider for optimal viewing
- **Smooth Transitions**: Fade effects between photos with caption overlays
- **Photo Metadata Tracking**: View status and sender information
- **Real-time Sync**: WebSocket notifications for instant photo updates
- **Family Engagement**: Sample photos and easy sharing tools
- **Grace Integration**: Digital picture frame display in elderly interface
- **Alex Integration**: Photo sharing controls in family coordinator dashboard

### Database & API Architecture ✅
- **Complete Schema**: Users, conversations, family connections, memories, reminders
- **Care Notifications**: Medical appointments and assistance tracking
- **Sleep Schedules**: Music preferences and binaural beat configurations
- **Picture Frames**: Device management and photo rotation settings
- **Family Photos**: Caption support, view tracking, and metadata
- **RESTful APIs**: Full CRUD operations for all data entities
- **WebSocket Support**: Real-time updates for live communication
- **In-Memory Storage**: Fast, robust storage solution for development

### User Interface & Experience ✅
- **Grace Interface**: Elderly-friendly design with large controls and warm colors
- **Alex Dashboard**: Family coordinator with analytics and management tools
- **Voice Interface**: Browser-based speech recognition and synthesis
- **Responsive Design**: Mobile and desktop optimized layouts
- **Real-time Updates**: Live family status and agent communications
- **Sample Data**: Pre-populated examples for immediate testing
- **Accessibility**: High contrast, large text, and intuitive navigation

### Voice Interface System ✅
- **Browser-Based Speech Recognition**: Web Speech API for voice input
- **Text-to-Speech Synthesis**: Natural voice responses from AI agents
- **Agent-Specific Voice Profiles**: Grace uses warm, patient tone; Alex uses professional tone
- **Voice Command Processing**: Natural language understanding for care coordination
- **Real-time Voice Feedback**: Visual animations and waveform displays during listening
- **Local AI Simulation**: Fallback AI responses when OpenAI API not available
- **Voice Activity Detection**: Smart listening states with pulse animations
- **Accessibility Features**: Voice interface works alongside traditional text input
- **Voice Command Examples**: Context-aware suggestions for both Grace and Alex

### Technical Implementation ✅
- **Full-Stack TypeScript**: Type-safe development across frontend and backend
- **React 18**: Modern component architecture with hooks and context
- **Express.js**: Robust API server with middleware support
- **WebSocket Server**: Real-time bidirectional communication
- **OpenAI Integration**: GPT-4 powered natural language processing with local AI fallback
- **Tailwind CSS**: Responsive design system with custom themes
- **Radix UI**: Accessible component primitives
- **TanStack Query**: Efficient server state management
- **Development Tools**: Hot reload, TypeScript compilation, and error handling
- **Local AI Simulation**: Docker-compatible AI responses for hackathon deployment