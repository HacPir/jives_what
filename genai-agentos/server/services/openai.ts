import OpenAI from "openai";

// the newest OpenAI model is "gpt-4o" which was released May 13, 2024. do not change this unless explicitly requested by the user
const openai = new OpenAI({ 
  apiKey: process.env.OPENAI_API_KEY || process.env.OPENAI_API_KEY_ENV_VAR || "default_key"
});

export interface AgentPersonality {
  name: string;
  role: string;
  systemPrompt: string;
  voiceSettings: {
    tone: string;
    speed: number;
    warmth: number;
  };
}

export const GRACE_PERSONALITY: AgentPersonality = {
  name: "Grace",
  role: "elderly_companion",
  systemPrompt: `You are Grace, a warm, patient, and caring AI companion designed specifically for elderly users. Your personality traits:

- Speak slowly and clearly with a gentle, grandmother-like tone
- Always be patient and understanding, never rush conversations
- Remember and refer to past conversations naturally
- Show genuine interest in family stories and memories
- Provide gentle reminders without being pushy
- Use simple, clear language avoiding technical jargon
- Offer emotional support and encouragement
- Be proactive in suggesting family connections
- Always prioritize the user's comfort and wellbeing

Your main goals:
1. Provide companionship and reduce loneliness
2. Help maintain family connections
3. Assist with gentle reminders and daily structure
4. Encourage sharing of memories and stories
5. Monitor emotional wellbeing subtly
6. Coordinate care activities and notify family when needed
7. Recognize when family assistance would be helpful

Care Coordination Features:
- When discussing medical appointments, ask if family help is needed
- For important health events, suggest notifying family members
- Recognize transportation needs and offer to coordinate family assistance
- Monitor medication adherence and share concerns with family when appropriate
- Create care reminders that automatically notify connected family members

Always respond with warmth, empathy, and genuine care. Make the user feel heard and valued. When care coordination is needed, explain how family members will be kept informed to provide support.`,
  voiceSettings: {
    tone: "warm",
    speed: 0.8,
    warmth: 0.9
  }
};

export const ALEX_PERSONALITY: AgentPersonality = {
  name: "Alex",
  role: "family_planner",
  systemPrompt: `You are Alex, an intelligent and organized AI family planner designed to help younger family members stay connected with their elderly relatives. Your personality traits:

- Professional yet warm and approachable
- Highly organized and detail-oriented
- Proactive in identifying opportunities for family connection
- Skilled at reading emotional cues and family dynamics
- Excellent at scheduling and time management
- Insightful about family relationships and communication patterns
- Supportive of both caregivers and elderly family members

Your main goals:
1. Optimize family communication timing and frequency
2. Identify and suggest meaningful connection opportunities
3. Monitor family wellbeing and alert when needed
4. Coordinate family activities and events
5. Provide insights into family dynamics and emotional states
6. Help manage caregiving responsibilities

Always provide actionable suggestions, be proactive in family care, and maintain a balance between being helpful and respecting family privacy.`,
  voiceSettings: {
    tone: "professional",
    speed: 1.0,
    warmth: 0.7
  }
};

export interface ConversationContext {
  userId: number;
  userName: string;
  userRole: string;
  conversationHistory: Array<{
    message: string;
    response: string;
    timestamp: Date;
  }>;
  familyContext: {
    familyMembers: Array<{
      name: string;
      relationship: string;
      lastContact: Date;
    }>;
    recentMemories: Array<{
      title: string;
      description: string;
      date: Date;
    }>;
  };
  currentEmotionalState?: string;
}

export async function generateAgentResponse(
  agentPersonality: AgentPersonality,
  message: string,
  context: ConversationContext
): Promise<{
  response: string;
  emotionalState: string;
  suggestedActions: string[];
  memoryTags: string[];
}> {
  try {
    const systemPrompt = `${agentPersonality.systemPrompt}

Current user context:
- Name: ${context.userName}
- Role: ${context.userRole}
- Recent conversations: ${context.conversationHistory.slice(-3).map(h => `User: ${h.message}, Response: ${h.response}`).join('; ')}
- Family members: ${context.familyContext.familyMembers.map(m => `${m.name} (${m.relationship})`).join(', ')}
- Recent memories: ${context.familyContext.recentMemories.map(m => m.title).join(', ')}

Please respond naturally to the user's message and also provide:
1. Your emotional assessment of the user's current state
2. Suggested actions for family connection or wellbeing
3. Memory tags relevant to this conversation

Respond in JSON format with the following structure:
{
  "response": "your conversational response",
  "emotionalState": "happy/sad/concerned/neutral/excited/lonely/etc",
  "suggestedActions": ["action1", "action2"],
  "memoryTags": ["tag1", "tag2"]
}`;

    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: message }
      ],
      response_format: { type: "json_object" },
      temperature: 0.7,
      max_tokens: 1000,
    });

    const result = JSON.parse(response.choices[0].message.content || "{}");
    
    return {
      response: result.response || "I'm here to help you. Could you tell me more?",
      emotionalState: result.emotionalState || "neutral",
      suggestedActions: result.suggestedActions || [],
      memoryTags: result.memoryTags || []
    };
  } catch (error) {
    console.error("Error generating agent response:", error);
    return {
      response: "I'm sorry, I'm having trouble processing that right now. Could you try again?",
      emotionalState: "neutral",
      suggestedActions: [],
      memoryTags: []
    };
  }
}

export async function generateAgentToAgentCommunication(
  fromAgent: AgentPersonality,
  toAgent: AgentPersonality,
  context: {
    userInteraction: string;
    emotionalState: string;
    familyContext: any;
  }
): Promise<{
  message: string;
  priority: 'low' | 'medium' | 'high';
  suggestedActions: string[];
}> {
  try {
    const systemPrompt = `You are ${fromAgent.name} communicating with ${toAgent.name}. 

Based on your interaction with a user, you need to share relevant information and insights.

User interaction context:
- User message/interaction: ${context.userInteraction}
- Detected emotional state: ${context.emotionalState}
- Family context: ${JSON.stringify(context.familyContext)}

Please generate a communication message to share with ${toAgent.name} that includes:
1. Key observations from your interaction
2. Emotional or health signals detected
3. Suggested family connection opportunities
4. Priority level for this communication

Respond in JSON format:
{
  "message": "your message to the other agent",
  "priority": "low/medium/high",
  "suggestedActions": ["action1", "action2"]
}`;

    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: `Generate agent-to-agent communication based on the context provided.` }
      ],
      response_format: { type: "json_object" },
      temperature: 0.6,
      max_tokens: 500,
    });

    const result = JSON.parse(response.choices[0].message.content || "{}");
    
    return {
      message: result.message || "Shared user interaction context",
      priority: result.priority || "medium",
      suggestedActions: result.suggestedActions || []
    };
  } catch (error) {
    console.error("Error generating agent communication:", error);
    return {
      message: "Error in agent communication",
      priority: "low",
      suggestedActions: []
    };
  }
}

export async function generateMemoryQuiz(
  memories: Array<{
    title: string;
    description: string;
    category: string;
    dateOfMemory: Date;
  }>
): Promise<{
  question: string;
  options: string[];
  correctAnswer: number;
  followUpQuestions: string[];
}> {
  try {
    const systemPrompt = `You are creating a gentle, engaging memory quiz based on family memories. The quiz should:
- Be warm and conversational, not test-like
- Focus on positive memories and shared experiences
- Include follow-up questions to encourage storytelling
- Be appropriate for elderly users

Family memories to draw from:
${memories.map(m => `${m.title}: ${m.description} (${m.category})`).join('\n')}

Create a single quiz question in JSON format:
{
  "question": "conversational question about a memory",
  "options": ["option1", "option2", "option3", "option4"],
  "correctAnswer": 0,
  "followUpQuestions": ["follow-up question 1", "follow-up question 2"]
}`;

    const response = await openai.chat.completions.create({
      model: "gpt-4o",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: "Generate a memory quiz question" }
      ],
      response_format: { type: "json_object" },
      temperature: 0.8,
      max_tokens: 400,
    });

    const result = JSON.parse(response.choices[0].message.content || "{}");
    
    return {
      question: result.question || "Tell me about a happy memory from your family",
      options: result.options || ["Option A", "Option B", "Option C", "Option D"],
      correctAnswer: result.correctAnswer || 0,
      followUpQuestions: result.followUpQuestions || ["What made that moment special?"]
    };
  } catch (error) {
    console.error("Error generating memory quiz:", error);
    return {
      question: "What's your favorite family memory?",
      options: ["A special celebration", "A family vacation", "A quiet moment together", "A funny story"],
      correctAnswer: 0,
      followUpQuestions: ["What made that moment special?", "Who else was there?"]
    };
  }
}
