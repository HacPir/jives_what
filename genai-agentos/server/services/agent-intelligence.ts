import OpenAI from "openai";
import { AgentPersonality } from "./openai";

const openai = new OpenAI({ 
  apiKey: process.env.OPENAI_API_KEY || "default_key"
});

export interface AgentMemory {
  shortTerm: Array<{
    interaction: string;
    timestamp: Date;
    emotionalContext: string;
    actionsTaken: string[];
  }>;
  longTerm: Array<{
    pattern: string;
    frequency: number;
    importance: 'low' | 'medium' | 'high';
    lastUpdate: Date;
  }>;
  familyContext: {
    relationships: Array<{
      name: string;
      relationship: string;
      lastContact: Date;
      preferences: string[];
    }>;
    careNeeds: Array<{
      type: string;
      frequency: string;
      priority: 'low' | 'medium' | 'high';
    }>;
    emotionalPatterns: Array<{
      trigger: string;
      response: string;
      effectiveness: number;
    }>;
  };
}

export interface AgentReasoning {
  situation: string;
  analysis: string;
  options: Array<{
    action: string;
    pros: string[];
    cons: string[];
    probability: number;
  }>;
  decision: string;
  reasoning: string;
  confidence: number;
}

export interface AgentCommunication {
  message: string;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  reasoning: AgentReasoning;
  suggestedActions: string[];
  actionPlan: Array<{
    step: string;
    timeframe: string;
    responsibility: 'grace' | 'alex' | 'family' | 'user';
  }>;
  followUp: {
    required: boolean;
    timeframe: string;
    checkpoints: string[];
  };
}

export class AgentIntelligence {
  private agentMemories: Map<string, AgentMemory> = new Map();

  async generateIntelligentResponse(
    agent: AgentPersonality,
    userMessage: string,
    context: any
  ): Promise<{
    message: string;
    emotionalState: string;
    reasoning: AgentReasoning;
    suggestedActions: string[];
    memoryTags: string[];
    agentCommunication?: AgentCommunication;
  }> {
    try {
      const memory = this.getAgentMemory(agent.name);
      const systemPrompt = this.buildIntelligentSystemPrompt(agent, memory, context);

      const response = await openai.chat.completions.create({
        model: "gpt-4o",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userMessage }
        ],
        response_format: { type: "json_object" },
        temperature: 0.7,
        max_tokens: 1000,
      });

      const result = JSON.parse(response.choices[0].message.content || "{}");
      
      // Update agent memory
      this.updateAgentMemory(agent.name, {
        interaction: userMessage,
        timestamp: new Date(),
        emotionalContext: result.emotionalState,
        actionsTaken: result.suggestedActions || []
      });

      return {
        message: result.message || "I understand your concern and I'm here to help.",
        emotionalState: result.emotionalState || "neutral",
        reasoning: result.reasoning || this.createDefaultReasoning(),
        suggestedActions: result.suggestedActions || [],
        memoryTags: result.memoryTags || [],
        agentCommunication: result.agentCommunication
      };
    } catch (error) {
      console.error("Error in intelligent response generation:", error);
      return this.createFallbackResponse(agent, userMessage);
    }
  }

  async generateAgentToAgentCommunication(
    fromAgent: AgentPersonality,
    toAgent: AgentPersonality,
    context: {
      userInteraction: string;
      emotionalState: string;
      familyContext: any;
      triggerType?: string;
      priority?: string;
    }
  ): Promise<AgentCommunication> {
    try {
      const fromMemory = this.getAgentMemory(fromAgent.name);
      const toMemory = this.getAgentMemory(toAgent.name);

      const systemPrompt = `You are an advanced AI agent coordination system facilitating intelligent communication between two specialized family care agents.

AGENT PROFILES:
FROM: ${fromAgent.name} (${fromAgent.role})
Core mission: ${fromAgent.systemPrompt.substring(0, 300)}...

TO: ${toAgent.name} (${toAgent.role})
Core mission: ${toAgent.systemPrompt.substring(0, 300)}...

CURRENT SITUATION:
- User interaction: "${context.userInteraction}"
- Emotional state: ${context.emotionalState}
- Trigger type: ${context.triggerType || 'general'}
- Family context: ${JSON.stringify(context.familyContext)}

AGENT MEMORY CONTEXT:
${fromAgent.name} recent interactions: ${JSON.stringify(fromMemory.shortTerm.slice(-3))}
${toAgent.name} capabilities: ${JSON.stringify(toMemory.familyContext.careNeeds)}

ADVANCED REASONING REQUIREMENTS:
1. Analyze the situation from multiple perspectives
2. Consider short-term and long-term implications
3. Evaluate available options with pros/cons
4. Make evidence-based decisions with confidence levels
5. Create actionable plans with clear responsibilities
6. Establish follow-up protocols for continuity

Generate sophisticated inter-agent communication with full reasoning:

{
  "message": "Professional message from ${fromAgent.name} to ${toAgent.name}",
  "priority": "low|medium|high|urgent",
  "reasoning": {
    "situation": "Clear description of current situation",
    "analysis": "Deep analysis of context and implications",
    "options": [
      {
        "action": "Option 1",
        "pros": ["benefit1", "benefit2"],
        "cons": ["drawback1", "drawback2"],
        "probability": 0.8
      }
    ],
    "decision": "Chosen course of action",
    "reasoning": "Why this decision was made",
    "confidence": 0.9
  },
  "suggestedActions": ["specific_action_1", "specific_action_2"],
  "actionPlan": [
    {
      "step": "First action step",
      "timeframe": "immediate/short/medium/long",
      "responsibility": "grace|alex|family|user"
    }
  ],
  "followUp": {
    "required": true,
    "timeframe": "24 hours",
    "checkpoints": ["checkpoint1", "checkpoint2"]
  }
}`;

      const response = await openai.chat.completions.create({
        model: "gpt-4o",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: "Generate intelligent inter-agent communication with full reasoning" }
        ],
        response_format: { type: "json_object" },
        temperature: 0.8,
        max_tokens: 1200,
      });

      const result = JSON.parse(response.choices[0].message.content || "{}");
      
      return {
        message: result.message || "Agent communication message",
        priority: result.priority || "medium",
        reasoning: result.reasoning || this.createDefaultReasoning(),
        suggestedActions: result.suggestedActions || [],
        actionPlan: result.actionPlan || [],
        followUp: result.followUp || { required: false, timeframe: "", checkpoints: [] }
      };
    } catch (error) {
      console.error("Error generating intelligent agent communication:", error);
      return this.createFallbackCommunication();
    }
  }

  private buildIntelligentSystemPrompt(
    agent: AgentPersonality,
    memory: AgentMemory,
    context: any
  ): string {
    return `${agent.systemPrompt}

ADVANCED CAPABILITIES:
- Deep reasoning and analysis
- Pattern recognition from past interactions
- Emotional intelligence and empathy
- Strategic planning and coordination
- Adaptive communication based on context

MEMORY CONTEXT:
Recent interactions: ${JSON.stringify(memory.shortTerm.slice(-5))}
Family relationships: ${JSON.stringify(memory.familyContext.relationships)}
Care patterns: ${JSON.stringify(memory.familyContext.careNeeds)}

RESPONSE REQUIREMENTS:
Provide a comprehensive response in JSON format:
{
  "message": "Your thoughtful response message",
  "emotionalState": "detected emotional state",
  "reasoning": {
    "situation": "What you understand about the situation",
    "analysis": "Your analysis of needs and context",
    "options": [{"action": "option", "pros": [], "cons": [], "probability": 0.8}],
    "decision": "Your chosen response approach",
    "reasoning": "Why you chose this approach",
    "confidence": 0.9
  },
  "suggestedActions": ["action1", "action2"],
  "memoryTags": ["tag1", "tag2"],
  "agentCommunication": {
    "message": "Message to other agent if needed",
    "priority": "low|medium|high|urgent",
    "reasoning": {...},
    "suggestedActions": [],
    "actionPlan": [],
    "followUp": {...}
  }
}`;
  }

  private getAgentMemory(agentName: string): AgentMemory {
    if (!this.agentMemories.has(agentName)) {
      this.agentMemories.set(agentName, {
        shortTerm: [],
        longTerm: [],
        familyContext: {
          relationships: [],
          careNeeds: [],
          emotionalPatterns: []
        }
      });
    }
    return this.agentMemories.get(agentName)!;
  }

  private updateAgentMemory(agentName: string, interaction: AgentMemory['shortTerm'][0]): void {
    const memory = this.getAgentMemory(agentName);
    memory.shortTerm.push(interaction);
    
    // Keep only last 20 interactions
    if (memory.shortTerm.length > 20) {
      memory.shortTerm = memory.shortTerm.slice(-20);
    }
  }

  private createDefaultReasoning(): AgentReasoning {
    return {
      situation: "User interaction requiring response",
      analysis: "Standard conversational response needed",
      options: [
        {
          action: "Provide supportive response",
          pros: ["Maintains engagement", "Shows care"],
          cons: ["May not address specific needs"],
          probability: 0.8
        }
      ],
      decision: "Provide supportive response",
      reasoning: "Best option for maintaining positive interaction",
      confidence: 0.7
    };
  }

  private createFallbackResponse(agent: AgentPersonality, userMessage: string) {
    return {
      message: agent.name === "Grace" ? 
        "I'm here for you, dear. How can I help you today?" :
        "I'm analyzing the situation and will coordinate the best response.",
      emotionalState: "neutral",
      reasoning: this.createDefaultReasoning(),
      suggestedActions: ["continue_conversation"],
      memoryTags: ["fallback_response"]
    };
  }

  private createFallbackCommunication(): AgentCommunication {
    return {
      message: "Agent coordination needed",
      priority: "medium",
      reasoning: this.createDefaultReasoning(),
      suggestedActions: ["coordinate_care"],
      actionPlan: [
        {
          step: "Assess situation",
          timeframe: "immediate",
          responsibility: "grace"
        }
      ],
      followUp: {
        required: true,
        timeframe: "1 hour",
        checkpoints: ["Check user status"]
      }
    };
  }
}

export const agentIntelligence = new AgentIntelligence();