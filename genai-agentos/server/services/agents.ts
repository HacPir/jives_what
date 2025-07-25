import { storage } from "../storage";
import { 
  generateAgentResponse, 
  generateAgentToAgentCommunication,
  generateMemoryQuiz,
  GRACE_PERSONALITY,
  ALEX_PERSONALITY,
  type ConversationContext 
} from "./openai";
import { localAI } from './local-ai';
import { interAgentService } from './inter-agent-communication';
import { agentIntelligence } from './agent-intelligence';
import { genaiAgentService } from './genai-agent-integration';
import type { 
  User, 
  InsertConversation, 
  InsertAgentCommunication,
  CareNotification,
  FamilyConnection
} from "@shared/schema";

export interface AgentMessage {
  type: 'text' | 'voice' | 'action';
  content: string;
  metadata?: any;
}

export interface AgentResponse {
  message: string;
  emotionalState: string;
  suggestedActions: string[];
  memoryTags: string[];
  agentCommunication?: {
    toAgent: string;
    message: string;
    priority: 'low' | 'medium' | 'high';
  };
}

export class AgentService {
  async processUserMessage(
    userId: number,
    agentId: string,
    message: string
  ): Promise<AgentResponse> {
    // Get user and context
    const user = await storage.getUser(userId);
    if (!user) {
      throw new Error("User not found");
    }

    const context = await this.buildConversationContext(userId, user);
    
    // Select appropriate agent personality
    const agentPersonality = agentId === 'grace' ? GRACE_PERSONALITY : ALEX_PERSONALITY;
    
    // Generate response using genai-protocol agents, intelligent agent system, OpenAI, or local AI
    let aiResponse;
    
    // First try genai-protocol agents
    try {
      console.log('Using genai-protocol agent system');
      const genaiResponse = await genaiAgentService.sendMessage(agentId, message, context);
      aiResponse = {
        response: genaiResponse,
        emotionalState: 'neutral',
        suggestedActions: [],
        memoryTags: []
      };
    } catch (genaiError) {
      console.log('GenAI agent not available, falling back to other systems');
      
      // Fall back to existing systems
      if (!process.env.OPENAI_API_KEY) {
        console.log('Using local AI simulation for agent response');
        aiResponse = localAI.generateResponse(agentId as 'grace' | 'alex', message, context);
      } else {
        try {
          console.log('Using intelligent agent system with OpenAI');
          aiResponse = await agentIntelligence.generateIntelligentResponse(agentPersonality, message, context);
        } catch (error) {
          console.log('Falling back to standard OpenAI response');
          aiResponse = await generateAgentResponse(agentPersonality, message, context);
        }
      }
    }
    
    // Store conversation
    await storage.createConversation({
      userId,
      agentId,
      message,
      response: aiResponse.response || aiResponse.message,
      emotionalState: aiResponse.emotionalState,
      metadata: {
        suggestedActions: aiResponse.suggestedActions,
        memoryTags: aiResponse.memoryTags
      }
    });

    // Generate agent-to-agent communication if needed
    let agentCommunication;
    const communicationCheck = interAgentService.shouldTriggerAgentCommunication(
      agentId as 'grace' | 'alex',
      message,
      aiResponse.emotionalState,
      aiResponse.suggestedActions
    );
    
    if (communicationCheck.shouldTrigger) {
      const targetAgent = agentId === 'grace' ? 'alex' : 'grace';
      
      // Send message to the other agent
      const interAgentMessage = await interAgentService.sendAgentMessage(
        agentId as 'grace' | 'alex',
        targetAgent as 'grace' | 'alex',
        {
          userId,
          triggerType: communicationCheck.triggerType as any,
          priority: communicationCheck.priority as any,
          originalUserMessage: message,
          emotionalState: aiResponse.emotionalState,
          suggestedActions: aiResponse.suggestedActions
        }
      );

      // Process the message with the receiving agent
      const agentResponse = await interAgentService.processAgentMessage(
        targetAgent as 'grace' | 'alex',
        interAgentMessage
      );

      agentCommunication = {
        toAgent: targetAgent,
        message: interAgentMessage.message,
        priority: communicationCheck.priority,
        response: agentResponse.message,
        actionsRequired: agentResponse.actions,
        followUpRequired: agentResponse.followUpRequired
      };
    }

    return {
      message: aiResponse.response || aiResponse.message,
      emotionalState: aiResponse.emotionalState,
      suggestedActions: aiResponse.suggestedActions,
      memoryTags: aiResponse.memoryTags,
      agentCommunication
    };
  }

  private async buildConversationContext(userId: number, user: User): Promise<ConversationContext> {
    // Get recent conversations
    const conversations = await storage.getConversations(userId, 10);
    const conversationHistory = conversations.map(c => ({
      message: c.message,
      response: c.response || "",
      timestamp: c.timestamp || new Date()
    }));

    // Get family connections
    const familyConnections = await storage.getFamilyConnections(userId);
    const familyMembers = await Promise.all(
      familyConnections.map(async (conn) => {
        const familyMemberId = conn.elderlyUserId === userId ? conn.caregiverUserId : conn.elderlyUserId;
        const familyMember = await storage.getUser(familyMemberId);
        return {
          name: familyMember?.name || "Unknown",
          relationship: conn.relationshipType,
          lastContact: conn.lastContactDate || new Date()
        };
      })
    );

    // Get recent memories
    const recentMemories = [];
    for (const connection of familyConnections) {
      const memories = await storage.getMemories(connection.id);
      recentMemories.push(...memories.slice(0, 3).map(m => ({
        title: m.title,
        description: m.description,
        date: m.dateOfMemory || new Date()
      })));
    }

    return {
      userId,
      userName: user.name,
      userRole: user.role,
      conversationHistory,
      familyContext: {
        familyMembers,
        recentMemories
      }
    };
  }

  private shouldTriggerAgentCommunication(
    emotionalState: string,
    suggestedActions: string[]
  ): boolean {
    // Trigger communication for concerning emotional states
    const concerningStates = ['sad', 'lonely', 'anxious', 'confused', 'worried'];
    if (concerningStates.includes(emotionalState.toLowerCase())) {
      return true;
    }

    // Trigger for specific action types
    const communicationTriggers = [
      'contact family',
      'schedule call',
      'check wellbeing',
      'medical concern',
      'emotional support'
    ];
    
    return suggestedActions.some(action => 
      communicationTriggers.some(trigger => 
        action.toLowerCase().includes(trigger)
      )
    );
  }

  // Care coordination methods
  async createCareNotification(
    elderlyUserId: number,
    notificationType: 'appointment' | 'medication' | 'emergency' | 'care_update',
    title: string,
    description: string,
    scheduledTime?: Date,
    careProvider?: string,
    assistanceNeeded: boolean = false
  ): Promise<CareNotification> {
    const notification = await storage.createCareNotification({
      elderlyUserId,
      notificationType,
      title,
      description,
      scheduledTime,
      careProvider,
      assistanceNeeded,
      familyInvited: true,
      urgencyLevel: assistanceNeeded ? 'high' : 'normal'
    });

    // Notify connected family members
    await this.notifyFamilyMembers(elderlyUserId, notification);
    
    return notification;
  }

  async notifyFamilyMembers(elderlyUserId: number, notification: CareNotification): Promise<void> {
    const familyConnections = await storage.getFamilyConnections(elderlyUserId);
    const familyMemberIds: number[] = [];

    for (const connection of familyConnections) {
      const familyMemberId = connection.caregiverUserId === elderlyUserId 
        ? connection.elderlyUserId 
        : connection.caregiverUserId;
      
      if (familyMemberId) {
        familyMemberIds.push(familyMemberId);
        
        // Create agent communication to notify family
        await storage.createAgentCommunication({
          fromAgent: 'grace',
          toAgent: 'alex',
          message: `Care notification for ${notification.title}: ${notification.description}`,
          context: {
            notificationId: notification.id,
            elderlyUserId,
            familyMemberId,
            urgencyLevel: notification.urgencyLevel,
            assistanceNeeded: notification.assistanceNeeded,
            scheduledTime: notification.scheduledTime
          }
        });
      }
    }

    // Update notification with family members who were notified
    await storage.updateCareNotificationFamilyNotified(notification.id, familyMemberIds);
  }

  async processCareReminder(
    userId: number,
    reminderType: 'appointment' | 'medication' | 'care_facility',
    title: string,
    description: string,
    scheduledTime: Date,
    careCoordination?: any
  ): Promise<void> {
    // Create reminder
    await storage.createReminder({
      userId,
      title,
      description,
      reminderType,
      scheduledTime,
      priority: 'high',
      careCoordination
    });

    // If it's a care facility event, create care notification
    if (reminderType === 'care_facility' || reminderType === 'appointment') {
      await this.createCareNotification(
        userId,
        'appointment',
        title,
        description,
        scheduledTime,
        careCoordination?.careProvider,
        careCoordination?.assistanceNeeded || false
      );
    }
  }

  async generateFamilyInsights(userId: number): Promise<{
    wellbeingScore: number;
    recentActivity: string;
    suggestions: string[];
    alerts: string[];
  }> {
    const user = await storage.getUser(userId);
    if (!user) {
      throw new Error("User not found");
    }

    // Get recent conversations to analyze patterns
    const conversations = await storage.getConversations(userId, 20);
    const familyConnections = await storage.getFamilyConnections(userId);
    const pendingReminders = await storage.getPendingReminders(userId);

    // Simple scoring based on recent activity and emotional states
    let wellbeingScore = 70; // Base score
    
    // Adjust based on recent conversations
    const recentEmotionalStates = conversations
      .filter(c => c.emotionalState)
      .slice(0, 5)
      .map(c => c.emotionalState);

    const positiveStates = ['happy', 'excited', 'content', 'cheerful'];
    const negativeStates = ['sad', 'lonely', 'anxious', 'worried', 'confused'];

    const positiveCount = recentEmotionalStates.filter(state => 
      positiveStates.includes(state?.toLowerCase() || '')
    ).length;

    const negativeCount = recentEmotionalStates.filter(state => 
      negativeStates.includes(state?.toLowerCase() || '')
    ).length;

    wellbeingScore += (positiveCount * 5) - (negativeCount * 10);
    wellbeingScore = Math.max(0, Math.min(100, wellbeingScore));

    // Generate suggestions based on patterns
    const suggestions = [];
    if (negativeCount > 2) {
      suggestions.push("Consider scheduling more frequent check-ins");
    }
    if (conversations.length < 3) {
      suggestions.push("Encourage more regular conversations");
    }
    if (pendingReminders.length > 3) {
      suggestions.push("Help with reminder management");
    }

    // Generate alerts
    const alerts = [];
    if (wellbeingScore < 40) {
      alerts.push("Wellbeing score is low - consider immediate contact");
    }
    if (pendingReminders.length > 5) {
      alerts.push("Multiple pending reminders - assistance may be needed");
    }

    const lastContact = familyConnections[0]?.lastContactDate;
    if (lastContact && Date.now() - lastContact.getTime() > 7 * 24 * 60 * 60 * 1000) {
      alerts.push("No contact in over a week");
    }

    return {
      wellbeingScore,
      recentActivity: conversations.length > 0 ? 
        `${conversations.length} conversations in recent days` : 
        "Limited recent activity",
      suggestions,
      alerts
    };
  }

  async createMemoryQuiz(familyId: number): Promise<{
    question: string;
    options: string[];
    correctAnswer: number;
    followUpQuestions: string[];
  }> {
    const memories = await storage.getMemories(familyId);
    
    if (memories.length === 0) {
      return {
        question: "What's your favorite family memory?",
        options: ["A special celebration", "A family vacation", "A quiet moment together", "A funny story"],
        correctAnswer: 0,
        followUpQuestions: ["What made that moment special?", "Who else was there?"]
      };
    }

    return generateMemoryQuiz(memories.map(m => ({
      title: m.title,
      description: m.description,
      category: m.category,
      dateOfMemory: m.dateOfMemory || new Date()
    })));
  }

  async getAgentCommunications(limit: number = 10): Promise<any[]> {
    return storage.getAgentCommunications(limit);
  }

  async suggestOptimalContactTime(userId: number): Promise<{
    suggestedTime: Date;
    reason: string;
    confidence: number;
  }> {
    const conversations = await storage.getConversations(userId, 50);
    
    // Analyze conversation patterns to suggest optimal times
    const hourCounts = new Map<number, number>();
    const dayOfWeekCounts = new Map<number, number>();

    conversations.forEach(conv => {
      if (conv.timestamp) {
        const hour = conv.timestamp.getHours();
        const dayOfWeek = conv.timestamp.getDay();
        
        hourCounts.set(hour, (hourCounts.get(hour) || 0) + 1);
        dayOfWeekCounts.set(dayOfWeek, (dayOfWeekCounts.get(dayOfWeek) || 0) + 1);
      }
    });

    // Find most common hour and day
    const bestHour = Array.from(hourCounts.entries())
      .sort((a, b) => b[1] - a[1])[0]?.[0] || 15; // Default to 3 PM

    const bestDay = Array.from(dayOfWeekCounts.entries())
      .sort((a, b) => b[1] - a[1])[0]?.[0] || 0; // Default to Sunday

    // Calculate next occurrence
    const now = new Date();
    const suggestedTime = new Date();
    
    // Set to next occurrence of best day and hour
    const daysUntilBestDay = (bestDay - now.getDay() + 7) % 7;
    suggestedTime.setDate(now.getDate() + daysUntilBestDay);
    suggestedTime.setHours(bestHour, 0, 0, 0);

    // If that time has passed today and it's the same day, move to next week
    if (suggestedTime <= now) {
      suggestedTime.setDate(suggestedTime.getDate() + 7);
    }

    const confidence = Math.min(0.9, (conversations.length / 20) * 0.8 + 0.1);
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const reason = `Based on conversation patterns, ${dayNames[bestDay]} at ${bestHour}:00 is typically a good time`;

    return {
      suggestedTime,
      reason,
      confidence
    };
  }
}

export const agentService = new AgentService();
