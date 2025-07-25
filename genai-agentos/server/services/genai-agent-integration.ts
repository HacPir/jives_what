import { spawn, ChildProcess } from 'child_process';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
// Use native fetch (Node.js 18+)
const fetch = globalThis.fetch;

// ES module compatibility
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export interface GenAIAgentConfig {
  name: string;
  role: string;
  port: number;
  script: string;
  status: 'starting' | 'running' | 'stopped' | 'error';
  process?: ChildProcess;
}

export interface GenAIMessage {
  model: string;
  messages: Array<{
    role: 'system' | 'user' | 'assistant';
    content: string;
  }>;
  temperature?: number;
  max_tokens?: number;
}

export interface GenAIResponse {
  id: string;
  object: string;
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: string;
      content: string;
    };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

export class GenAIAgentService {
  private agents: Map<string, GenAIAgentConfig> = new Map();
  private isStarting = false;
  private useGenAI = false;

  constructor() {
    this.agents.set('grace', {
      name: 'Grace',
      role: 'elderly_companion',
      port: 8001,
      script: 'grace_agent.py',
      status: 'stopped'
    });

    this.agents.set('alex', {
      name: 'Alex',
      role: 'family_coordinator',
      port: 8002,
      script: 'alex_agent.py',
      status: 'stopped'
    });

    // Check if GenAI AgentOS is available
    this.checkGenAIAvailability();
  }

  private async checkGenAIAvailability(): Promise<void> {
    try {
      const response = await fetch('http://localhost:3000/health', {
        signal: AbortSignal.timeout(5000)
      });
      
      if (response.ok) {
        console.log('✅ GenAI AgentOS detected - using GenAI integration');
        this.useGenAI = true;
      } else {
        console.log('🔧 GenAI AgentOS not available - using local agents');
        this.useGenAI = false;
      }
    } catch (error) {
      console.log('🔧 GenAI AgentOS not available - using local agents');
      this.useGenAI = false;
    }
  }

  async startAgents(): Promise<void> {
    if (this.isStarting) return;
    this.isStarting = true;

    try {
      console.log('Starting genai-protocol agents...');
      
      for (const [agentId, config] of this.agents) {
        await this.startAgent(agentId, config);
      }
      
      // Wait for agents to be ready
      await this.waitForAgentsReady();
      
      console.log('All genai-protocol agents started successfully');
    } catch (error) {
      console.error('Error starting agents:', error);
    } finally {
      this.isStarting = false;
    }
  }

  private async startAgent(agentId: string, config: GenAIAgentConfig): Promise<void> {
    if (config.status === 'running') return;

    const agentPath = join(__dirname, '..', 'agents', config.script);
    
    console.log(`Starting ${config.name} agent on port ${config.port}...`);
    
    const agentProcess = spawn('python3', [agentPath], {
      env: {
        ...process.env,
        PORT: config.port.toString(),
        PYTHONPATH: join(__dirname, '..', 'agents')
      },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    config.process = agentProcess;
    config.status = 'starting';

    agentProcess.stdout?.on('data', (data) => {
      console.log(`[${config.name}] ${data.toString()}`);
    });

    agentProcess.stderr?.on('data', (data) => {
      console.error(`[${config.name}] ${data.toString()}`);
    });

    agentProcess.on('exit', (code) => {
      console.log(`${config.name} agent exited with code ${code}`);
      config.status = 'stopped';
    });

    agentProcess.on('error', (error) => {
      console.error(`${config.name} agent error:`, error);
      config.status = 'error';
    });

    this.agents.set(agentId, config);
  }

  private async waitForAgentsReady(): Promise<void> {
    const maxAttempts = 30;
    const delay = 1000;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      let allReady = true;

      for (const [agentId, config] of this.agents) {
        try {
          const response = await fetch(`http://localhost:${config.port}/health`, {
            method: 'GET',
            timeout: 5000
          });

          if (response.ok) {
            config.status = 'running';
            console.log(`${config.name} agent is ready`);
          } else {
            allReady = false;
          }
        } catch (error) {
          allReady = false;
        }
      }

      if (allReady) {
        return;
      }

      await new Promise(resolve => setTimeout(resolve, delay));
    }

    throw new Error('Timeout waiting for agents to be ready');
  }

  async sendMessage(agentId: string, message: string, context?: any): Promise<string> {
    // If GenAI AgentOS is available, use it
    if (this.useGenAI) {
      return await this.sendMessageViaGenAI(agentId, message, context);
    }

    // Otherwise use local agents
    const config = this.agents.get(agentId);
    if (!config) {
      throw new Error(`Agent ${agentId} not found`);
    }

    if (config.status !== 'running') {
      throw new Error(`Agent ${agentId} is not running`);
    }

    const genaiMessage: GenAIMessage = {
      model: `${agentId}-agent`,
      messages: [
        { role: 'user', content: message }
      ],
      temperature: 0.7,
      max_tokens: 400
    };

    if (context) {
      genaiMessage.messages.unshift({
        role: 'system',
        content: `Context: ${JSON.stringify(context)}`
      });
    }

    try {
      const response = await fetch(`http://localhost:${config.port}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(genaiMessage),
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        throw new Error(`Agent ${agentId} responded with status ${response.status}`);
      }

      const result = await response.json() as GenAIResponse;
      return result.choices[0].message.content;
    } catch (error) {
      console.error(`Error communicating with ${agentId}:`, error);
      throw error;
    }
  }

  async facilitateInterAgentCommunication(
    fromAgent: string,
    toAgent: string,
    message: string,
    priority: string = 'medium',
    context?: any
  ): Promise<{
    from_agent: string;
    to_agent: string;
    message: string;
    response: string;
    priority: string;
    timestamp: number;
  }> {
    const agentContext = {
      inter_agent_communication: true,
      from_agent: fromAgent,
      priority: priority,
      original_context: context
    };

    const response = await this.sendMessage(toAgent, message, agentContext);

    return {
      from_agent: fromAgent,
      to_agent: toAgent,
      message: message,
      response: response,
      priority: priority,
      timestamp: Date.now()
    };
  }

  async getAgentStatus(): Promise<Record<string, any>> {
    const status: Record<string, any> = {};

    for (const [agentId, config] of this.agents) {
      try {
        if (config.status === 'running') {
          const response = await fetch(`http://localhost:${config.port}/agent/info`, {
            signal: AbortSignal.timeout(5000)
          });
          
          if (response.ok) {
            status[agentId] = await response.json();
          } else {
            status[agentId] = { status: 'error', name: config.name };
          }
        } else {
          status[agentId] = { status: config.status, name: config.name };
        }
      } catch (error) {
        status[agentId] = { status: 'error', name: config.name, error: error.message };
      }
    }

    return status;
  }

  async stopAgents(): Promise<void> {
    console.log('Stopping genai-protocol agents...');

    for (const [agentId, config] of this.agents) {
      if (config.process) {
        config.process.kill();
        config.status = 'stopped';
      }
    }
  }

  getAgentConfig(agentId: string): GenAIAgentConfig | undefined {
    return this.agents.get(agentId);
  }

  getAllAgents(): Map<string, GenAIAgentConfig> {
    return new Map(this.agents);
  }

  private async sendMessageViaGenAI(agentId: string, message: string, context?: any): Promise<string> {
    // Send message through GenAI AgentOS
    try {
      const response = await fetch('http://localhost:3000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          agent_id: agentId,
          message: message,
          context: context || {},
          source: 'familyconnect'
        }),
        signal: AbortSignal.timeout(30000)
      });

      if (!response.ok) {
        throw new Error(`GenAI communication failed: ${response.status}`);
      }

      const result = await response.json();
      return result.response || 'No response received';
    } catch (error) {
      console.error(`GenAI communication error for ${agentId}:`, error);
      throw error;
    }
  }

  async deployToGenAI(): Promise<boolean> {
    // Deploy agents to GenAI AgentOS
    try {
      const graceConfig = {
        name: 'Grace',
        type: 'elderly_companion',
        url: 'http://localhost:8001',
        capabilities: ['emotional_support', 'health_monitoring', 'companionship'],
        metadata: {
          personality: 'warm_grandmother',
          target_audience: 'elderly_users',
          communication_style: 'patient_caring'
        }
      };

      const alexConfig = {
        name: 'Alex',
        type: 'family_coordinator', 
        url: 'http://localhost:8002',
        capabilities: ['care_coordination', 'family_management', 'health_tracking'],
        metadata: {
          personality: 'professional_coordinator',
          target_audience: 'caregivers_family',
          communication_style: 'efficient_organized'
        }
      };

      const graceResponse = await fetch('http://localhost:3000/api/agents/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(graceConfig),
        signal: AbortSignal.timeout(30000)
      });

      const alexResponse = await fetch('http://localhost:3000/api/agents/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(alexConfig),
        signal: AbortSignal.timeout(30000)
      });

      return graceResponse.ok && alexResponse.ok;
    } catch (error) {
      console.error('Error deploying to GenAI:', error);
      return false;
    }
  }
}

export const genaiAgentService = new GenAIAgentService();

// Auto-start agents when the service is imported (disabled by default)
// if (process.env.NODE_ENV === 'development') {
//   genaiAgentService.startAgents().catch(console.error);
// }

// Cleanup on exit
process.on('exit', () => {
  genaiAgentService.stopAgents();
});

process.on('SIGINT', () => {
  genaiAgentService.stopAgents();
  process.exit(0);
});

process.on('SIGTERM', () => {
  genaiAgentService.stopAgents();
  process.exit(0);
});