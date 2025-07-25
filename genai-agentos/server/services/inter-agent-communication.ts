import { storage } from "../storage";
import { generateAgentToAgentCommunication, GRACE_PERSONALITY, ALEX_PERSONALITY } from "./openai";
import { localAI } from './local-ai';
import { agentIntelligence } from './agent-intelligence';
import type { User } from "@shared/schema";

export interface InterAgentMessage {
  fromAgent: 'grace' | 'alex';
  toAgent: 'grace' | 'alex';
  message: string;
  context: {
    userId: number;
    triggerType: 'user_concern' | 'care_needed' | 'family_update' | 'emergency' | 'routine_check';
    priority: 'low' | 'medium' | 'high' | 'urgent';
    originalUserMessage?: string;
    emotionalState?: string;
    suggestedActions?: string[];
  };
  timestamp: Date;
}

export interface AgentResponseToAgent {
  message: string;
  actions: string[];
  followUpRequired: boolean;
  userNotificationNeeded: boolean;
  careCoordination?: {
    appointmentSuggested: boolean;
    familyNotificationNeeded: boolean;
    urgencyLevel: 'low' | 'medium' | 'high' | 'urgent';
  };
}

export class InterAgentCommunicationService {
  
  /**
   * Determines if agent communication should be triggered based on user interaction
   */
  shouldTriggerAgentCommunication(
    agentId: 'grace' | 'alex',
    userMessage: string,
    emotionalState: string,
    suggestedActions: string[]
  ): { shouldTrigger: boolean; triggerType: string; priority: string } {
    
    // Keywords that trigger inter-agent communication
    const careKeywords = ['doctor', 'appointment', 'medication', 'pain', 'sick', 'hospital', 'emergency'];
    const emotionalKeywords = ['sad', 'lonely', 'worried', 'scared', 'confused', 'frustrated'];
    const familyKeywords = ['family', 'visit', 'call', 'children', 'grandchildren', 'daughter', 'son'];
    
    const lowerMessage = userMessage.toLowerCase();
    
    // High priority triggers
    if (careKeywords.some(keyword => lowerMessage.includes(keyword))) {
      return { shouldTrigger: true, triggerType: 'care_needed', priority: 'high' };
    }
    
    if (emotionalState === 'distressed' || emotionalState === 'anxious') {
      return { shouldTrigger: true, triggerType: 'user_concern', priority: 'high' };
    }
    
    // Medium priority triggers
    if (emotionalKeywords.some(keyword => lowerMessage.includes(keyword))) {
      return { shouldTrigger: true, triggerType: 'user_concern', priority: 'medium' };
    }
    
    if (familyKeywords.some(keyword => lowerMessage.includes(keyword))) {
      return { shouldTrigger: true, triggerType: 'family_update', priority: 'medium' };
    }
    
    // Low priority - routine check for Grace only
    if (agentId === 'grace' && suggestedActions.includes('routine_check')) {
      return { shouldTrigger: true, triggerType: 'routine_check', priority: 'low' };
    }
    
    return { shouldTrigger: false, triggerType: '', priority: '' };
  }

  /**
   * Sends a message from one agent to another
   */
  async sendAgentMessage(
    fromAgent: 'grace' | 'alex',
    toAgent: 'grace' | 'alex',
    context: InterAgentMessage['context']
  ): Promise<InterAgentMessage> {
    
    const user = await storage.getUser(context.userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Build context for agent communication
    const communicationContext = await this.buildInterAgentContext(context.userId, user, context);
    
    // Generate the inter-agent message
    const fromPersonality = fromAgent === 'grace' ? GRACE_PERSONALITY : ALEX_PERSONALITY;
    const toPersonality = toAgent === 'grace' ? GRACE_PERSONALITY : ALEX_PERSONALITY;
    
    let agentMessage;
    if (!process.env.OPENAI_API_KEY) {
      // Use local AI for agent communication
      agentMessage = this.generateLocalInterAgentMessage(fromAgent, toAgent, context, communicationContext);
    } else {
      try {
        // Use intelligent agent system for sophisticated communication
        agentMessage = await agentIntelligence.generateAgentToAgentCommunication(
          fromPersonality,
          toPersonality,
          {
            userInteraction: context.originalUserMessage || '',
            emotionalState: context.emotionalState || '',
            familyContext: communicationContext,
            triggerType: context.triggerType,
            priority: context.priority
          }
        );
      } catch (error) {
        console.log('Falling back to standard agent communication');
        agentMessage = await generateAgentToAgentCommunication(
          fromPersonality,
          toPersonality,
          {
            userInteraction: context.originalUserMessage || '',
            emotionalState: context.emotionalState || '',
            familyContext: communicationContext
          }
        );
      }
    }

    // Store the communication
    const interAgentMessage: InterAgentMessage = {
      fromAgent,
      toAgent,
      message: agentMessage.message,
      context,
      timestamp: new Date()
    };

    await storage.createAgentCommunication({
      fromAgent,
      toAgent,
      message: agentMessage.message,
      context: {
        priority: context.priority,
        triggerType: context.triggerType,
        originalUserMessage: context.originalUserMessage,
        emotionalState: context.emotionalState,
        suggestedActions: context.suggestedActions
      }
    });

    return interAgentMessage;
  }

  /**
   * Processes a message received by an agent from another agent
   */
  async processAgentMessage(
    receivingAgent: 'grace' | 'alex',
    message: InterAgentMessage
  ): Promise<AgentResponseToAgent> {
    
    const user = await storage.getUser(message.context.userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Build context for response
    const responseContext = await this.buildInterAgentContext(
      message.context.userId, 
      user, 
      message.context
    );

    // Generate response based on receiving agent
    const receivingPersonality = receivingAgent === 'grace' ? GRACE_PERSONALITY : ALEX_PERSONALITY;
    
    let response;
    if (!process.env.OPENAI_API_KEY) {
      response = this.generateLocalAgentResponse(receivingAgent, message, responseContext);
    } else {
      // Use OpenAI to generate thoughtful response
      response = await this.generateAgentResponse(receivingPersonality, message, responseContext);
    }

    // Determine if follow-up actions are needed
    const followUpRequired = message.context.priority === 'high' || message.context.priority === 'urgent';
    const userNotificationNeeded = message.context.triggerType === 'care_needed' || 
                                   message.context.triggerType === 'emergency';

    return {
      message: response.message,
      actions: response.actions || [],
      followUpRequired,
      userNotificationNeeded,
      careCoordination: response.careCoordination
    };
  }

  /**
   * Local AI fallback for inter-agent communication
   */
  private generateLocalInterAgentMessage(
    fromAgent: 'grace' | 'alex',
    toAgent: 'grace' | 'alex',
    context: InterAgentMessage['context'],
    communicationContext: any
  ) {
    const templates = {
      grace_to_alex: {
        care_needed: `Alex, I'm concerned about our family member. They mentioned ${context.originalUserMessage}. Could you help coordinate care?`,
        user_concern: `Alex, I noticed some emotional distress during our conversation. Family support might be helpful.`,
        family_update: `Alex, there's been a family interaction you should know about. They're asking about family connections.`,
        routine_check: `Alex, just a routine update - everything seems well during our conversation.`
      },
      alex_to_grace: {
        care_needed: `Grace, I've set up care coordination. Please reassure them that family support is in place.`,
        user_concern: `Grace, I've notified the family about the concern. Please provide extra emotional support.`,
        family_update: `Grace, I've updated the family coordination. You can share this update with them.`,
        routine_check: `Grace, thanks for the update. Continue providing wonderful support.`
      }
    };

    const direction = `${fromAgent}_to_${toAgent}` as keyof typeof templates;
    const template = templates[direction]?.[context.triggerType as keyof typeof templates[typeof direction]];

    return {
      message: template || `Message from ${fromAgent} to ${toAgent} regarding ${context.triggerType}`,
      priority: context.priority,
      suggestedActions: [`${toAgent}_follow_up`]
    };
  }

  /**
   * Local AI fallback for agent response
   */
  private generateLocalAgentResponse(
    receivingAgent: 'grace' | 'alex',
    message: InterAgentMessage,
    context: any
  ) {
    const responses = {
      grace: {
        care_needed: "I'll provide extra comfort and reassurance. Thank you for coordinating the care.",
        user_concern: "I'll be especially attentive to their emotional needs and provide support.",
        family_update: "I'll share this positive update to help them feel more connected.",
        routine_check: "Thank you for the coordination. I'll continue our caring conversations."
      },
      alex: {
        care_needed: "I've initiated care coordination and will notify the family immediately.",
        user_concern: "I'm reaching out to family members to provide additional support.",
        family_update: "I've updated the family coordination system with this information.",
        routine_check: "Noted. I'll continue monitoring the family coordination aspects."
      }
    };

    const response = responses[receivingAgent][message.context.triggerType as keyof typeof responses[typeof receivingAgent]];

    return {
      message: response || `Acknowledged by ${receivingAgent}`,
      actions: [`${receivingAgent}_response_action`],
      careCoordination: message.context.triggerType === 'care_needed' ? {
        appointmentSuggested: true,
        familyNotificationNeeded: true,
        urgencyLevel: message.context.priority as 'low' | 'medium' | 'high' | 'urgent'
      } : undefined
    };
  }

  /**
   * Builds context for inter-agent communication
   */
  private async buildInterAgentContext(
    userId: number,
    user: User,
    context: InterAgentMessage['context']
  ) {
    const familyConnections = await storage.getFamilyConnections(userId);
    const recentConversations = await storage.getConversations(userId, 5);
    const careNotifications = await storage.getCareNotifications(userId);

    return {
      user: {
        name: user.name,
        role: user.role,
        preferences: user.preferences
      },
      familyConnections: familyConnections.length,
      recentEmotionalState: context.emotionalState,
      careHistory: careNotifications.length,
      conversationHistory: recentConversations.slice(0, 3).map(c => ({
        message: c.message,
        response: c.response,
        emotionalState: c.emotionalState
      }))
    };
  }

  /**
   * Generates agent response using OpenAI
   */
  private async generateAgentResponse(
    personality: any,
    message: InterAgentMessage,
    context: any
  ) {
    // This would use OpenAI to generate a contextual response
    // For now, return a structured response
    return {
      message: `I understand the ${message.context.triggerType} situation and will respond appropriately.`,
      actions: ['follow_up_action'],
      careCoordination: message.context.triggerType === 'care_needed' ? {
        appointmentSuggested: true,
        familyNotificationNeeded: true,
        urgencyLevel: message.context.priority as 'low' | 'medium' | 'high' | 'urgent'
      } : undefined
    };
  }

  /**
   * Gets all agent communications for a user
   */
  async getAgentCommunications(userId: number): Promise<InterAgentMessage[]> {
    const communications = await storage.getAgentCommunications();
    return communications
      .filter(comm => comm.context && comm.context.userId === userId)
      .map(comm => ({
        fromAgent: comm.fromAgent as 'grace' | 'alex',
        toAgent: comm.toAgent as 'grace' | 'alex',
        message: comm.message,
        context: comm.context as InterAgentMessage['context'],
        timestamp: comm.timestamp || new Date()
      }));
  }
}

export const interAgentService = new InterAgentCommunicationService();