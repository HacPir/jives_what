// Local AI simulation for hackathon demo without OpenAI API
import { AgentPersonality, ConversationContext } from './openai';

export interface LocalAIResponse {
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

export class LocalAI {
  private graceResponses = [
    "I'm so glad you're here! How are you feeling today?",
    "That sounds wonderful, dear. Tell me more about that.",
    "I understand how you're feeling. You're doing great.",
    "Would you like me to help you call your family?",
    "Let's look at some beautiful family photos together.",
    "It's time for your medication reminder. Shall I help you with that?",
    "Your family loves you very much. They've been thinking about you.",
    "How about we set up a relaxing sleep schedule for tonight?",
    "I'm here whenever you need to talk. You're never alone.",
    "Your granddaughter sent you a lovely new photo today!"
  ];

  private alexResponses = [
    "I've updated the family status. Everyone is doing well.",
    "I'll coordinate with Grace to ensure optimal care timing.",
    "The wellbeing metrics show positive trends this week.",
    "I've scheduled a family call for the optimal time window.",
    "New care appointment scheduled with family notifications sent.",
    "Photo sharing is active. Your family member will see it soon.",
    "Grace reports good engagement levels with the elderly user.",
    "I recommend increased family contact based on emotional patterns.",
    "Care coordination is running smoothly across all family members.",
    "The sleep schedule optimization has shown positive results."
  ];

  private careTopics = [
    "medication", "appointment", "family", "call", "photo", "sleep", 
    "health", "reminder", "visit", "care", "help", "lonely", "tired"
  ];

  private emotionalStates = [
    "cheerful", "content", "nostalgic", "worried", "excited", 
    "peaceful", "grateful", "reflective", "hopeful", "loving"
  ];

  generateResponse(
    agentType: 'grace' | 'alex',
    message: string,
    context: ConversationContext
  ): LocalAIResponse {
    const isGrace = agentType === 'grace';
    const responses = isGrace ? this.graceResponses : this.alexResponses;
    
    // Analyze message for keywords
    const lowerMessage = message.toLowerCase();
    let selectedResponse: string;
    let emotionalState: string;
    let suggestedActions: string[] = [];
    let memoryTags: string[] = [];
    let agentCommunication: any = null;

    // Smart response selection based on keywords
    if (lowerMessage.includes('family') || lowerMessage.includes('daughter') || lowerMessage.includes('son')) {
      selectedResponse = isGrace ? 
        "Your family loves you so much. Would you like me to help you call them?" :
        "I'll coordinate optimal family contact times and send updates to Grace.";
      memoryTags = ['family_connection'];
      suggestedActions = isGrace ? ['call_family', 'view_photos'] : ['schedule_call', 'send_notification'];
    } else if (lowerMessage.includes('photo') || lowerMessage.includes('picture')) {
      selectedResponse = isGrace ?
        "Let's look at those beautiful family photos together!" :
        "I'll ensure the new photos are sent to the picture frame immediately.";
      memoryTags = ['photo_sharing'];
      suggestedActions = isGrace ? ['view_photos', 'share_memories'] : ['send_photo', 'update_frame'];
    } else if (lowerMessage.includes('sleep') || lowerMessage.includes('tired') || lowerMessage.includes('rest')) {
      selectedResponse = isGrace ?
        "Let's set up a peaceful sleep schedule with some calming music." :
        "I'll optimize the sleep schedule and coordinate with Grace for better rest.";
      memoryTags = ['sleep_schedule'];
      suggestedActions = isGrace ? ['setup_sleep', 'play_music'] : ['optimize_schedule', 'monitor_sleep'];
    } else if (lowerMessage.includes('appointment') || lowerMessage.includes('doctor') || lowerMessage.includes('medical')) {
      selectedResponse = isGrace ?
        "I see you have an appointment coming up. I'll make sure your family knows if you need help." :
        "I'll coordinate the medical appointment and ensure family members are notified.";
      memoryTags = ['medical_care'];
      suggestedActions = isGrace ? ['view_appointments', 'call_family'] : ['schedule_appointment', 'notify_family'];
      
      // Trigger inter-agent communication for medical appointments
      if (isGrace) {
        agentCommunication = {
          toAgent: 'alex',
          message: `${context.userName} mentioned a medical appointment. Please coordinate family support.`,
          priority: 'medium' as const
        };
      }
    } else if (lowerMessage.includes('lonely') || lowerMessage.includes('sad') || lowerMessage.includes('miss')) {
      selectedResponse = isGrace ?
        "I understand, dear. You're not alone. Your family thinks about you every day." :
        "Grace reports emotional support needs. I'll increase family engagement activities.";
      emotionalState = 'lonely';
      memoryTags = ['emotional_support'];
      suggestedActions = isGrace ? ['call_family', 'view_photos', 'share_memories'] : ['increase_contact', 'plan_visit'];
      
      // High priority communication for emotional support
      if (isGrace) {
        agentCommunication = {
          toAgent: 'alex',
          message: `${context.userName} is feeling lonely. Recommend increased family contact.`,
          priority: 'high' as const
        };
      }
    } else if (lowerMessage.includes('help') || lowerMessage.includes('assistance')) {
      selectedResponse = isGrace ?
        "Of course! I'm here to help. What would you like assistance with?" :
        "I'll coordinate the needed assistance and notify relevant family members.";
      memoryTags = ['assistance_needed'];
      suggestedActions = isGrace ? ['provide_help', 'call_family'] : ['coordinate_help', 'notify_caregivers'];
    } else {
      // Default responses
      selectedResponse = responses[Math.floor(Math.random() * responses.length)];
    }

    // Set emotional state if not already set
    if (!emotionalState) {
      emotionalState = this.emotionalStates[Math.floor(Math.random() * this.emotionalStates.length)];
    }

    // Add context-based memory tags
    if (context.familyContext.familyMembers.length > 0) {
      memoryTags.push('family_context');
    }

    return {
      message: selectedResponse,
      emotionalState,
      suggestedActions,
      memoryTags,
      agentCommunication
    };
  }

  generateFamilyInsights(userId: number): any {
    return {
      wellbeingScore: Math.floor(Math.random() * 20) + 75, // 75-95 range
      engagementLevel: Math.floor(Math.random() * 30) + 70, // 70-100 range
      lastInteraction: new Date(Date.now() - Math.random() * 24 * 60 * 60 * 1000),
      recommendations: [
        "Family call scheduled for optimal time",
        "Photo sharing showing positive engagement",
        "Sleep schedule improvements recommended",
        "Medication reminders are effective"
      ],
      trends: {
        mood: "improving",
        activity: "stable",
        social: "increasing"
      }
    };
  }

  generateContactSuggestion(userId: number): any {
    const now = new Date();
    const suggestedTime = new Date(now.getTime() + (Math.random() * 6 + 1) * 60 * 60 * 1000); // 1-7 hours from now
    
    return {
      suggestedTime,
      reason: "Based on activity patterns and mood analysis",
      confidence: Math.floor(Math.random() * 20) + 80, // 80-100% confidence
      alternatives: [
        new Date(suggestedTime.getTime() + 60 * 60 * 1000), // +1 hour
        new Date(suggestedTime.getTime() + 2 * 60 * 60 * 1000), // +2 hours
      ]
    };
  }

  generateMemoryQuiz(familyId: number): any {
    const questions = [
      "What was your favorite family vacation destination?",
      "Who taught you to cook your favorite recipe?",
      "What was the name of your first pet?",
      "Where did you meet your spouse?",
      "What was your favorite song to dance to?"
    ];

    return {
      questions: questions.slice(0, 3),
      difficulty: "easy",
      category: "family_memories",
      estimatedTime: "5-10 minutes"
    };
  }
}

export const localAI = new LocalAI();