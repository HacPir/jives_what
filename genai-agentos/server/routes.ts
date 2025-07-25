import type { Express } from "express";
import { createServer, type Server } from "http";
import { WebSocketServer, WebSocket } from "ws";
import { storage } from "./storage";
import { agentService } from "./services/agents";
import { interAgentService } from "./services/inter-agent-communication";
import { genaiAgentService } from "./services/genai-agent-integration";
import { insertConversationSchema, insertUserSchema, insertReminderSchema, insertCareNotificationSchema, insertSleepScheduleSchema, insertPictureFrameSchema, insertFamilyPhotoSchema } from "@shared/schema";

export async function registerRoutes(app: Express): Promise<Server> {
  // Create HTTP server
  const httpServer = createServer(app);

  // Create WebSocket server for real-time communication
  const wss = new WebSocketServer({ server: httpServer, path: '/ws' });

  // Store WebSocket connections
  const connections = new Map<string, WebSocket>();

  // WebSocket connection handler
  wss.on('connection', (ws, req) => {
    const connectionId = Math.random().toString(36).substring(7);
    connections.set(connectionId, ws);

    ws.on('message', async (message) => {
      try {
        const data = JSON.parse(message.toString());
        
        switch (data.type) {
          case 'user_message':
            const response = await agentService.processUserMessage(
              data.userId,
              data.agentId,
              data.message
            );
            
            // Send response back to client
            if (ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({
                type: 'agent_response',
                response
              }));
            }

            // If there's agent communication, broadcast to other connections
            if (response.agentCommunication) {
              const agentMessage = {
                type: 'agent_communication',
                fromAgent: data.agentId,
                toAgent: response.agentCommunication.toAgent,
                message: response.agentCommunication.message,
                priority: response.agentCommunication.priority,
                response: response.agentCommunication.response,
                actions: response.agentCommunication.actionsRequired,
                followUpRequired: response.agentCommunication.followUpRequired,
                userId: data.userId,
                timestamp: new Date().toISOString()
              };

              // Broadcast to all connected clients
              connections.forEach((client, clientId) => {
                if (client !== ws && client.readyState === WebSocket.OPEN) {
                  try {
                    client.send(JSON.stringify(agentMessage));
                  } catch (error) {
                    console.error('Failed to send message to client:', error);
                    connections.delete(clientId);
                  }
                }
              });
            }
            break;

          case 'ping':
            if (ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({ type: 'pong' }));
            }
            break;

          case 'direct_agent_message':
            const directMessage = await interAgentService.sendAgentMessage(
              data.fromAgent,
              data.toAgent,
              {
                userId: data.userId,
                triggerType: 'direct_message',
                priority: data.priority || 'medium',
                originalUserMessage: data.message
              }
            );

            const directResponse = await interAgentService.processAgentMessage(
              data.toAgent,
              directMessage
            );

            // Send response back to sender
            if (ws.readyState === WebSocket.OPEN) {
              ws.send(JSON.stringify({
                type: 'direct_agent_response',
                message: directMessage.message,
                response: directResponse.message,
                actions: directResponse.actions,
                followUpRequired: directResponse.followUpRequired
              }));
            }

            // Broadcast to all other clients
            const broadcastMessage = {
              type: 'agent_communication',
              fromAgent: data.fromAgent,
              toAgent: data.toAgent,
              message: directMessage.message,
              response: directResponse.message,
              priority: data.priority || 'medium',
              userId: data.userId,
              timestamp: new Date().toISOString()
            };

            connections.forEach((client, clientId) => {
              if (client !== ws && client.readyState === WebSocket.OPEN) {
                try {
                  client.send(JSON.stringify(broadcastMessage));
                } catch (error) {
                  console.error('Failed to send direct message to client:', error);
                  connections.delete(clientId);
                }
              }
            });
            break;
        }
      } catch (error) {
        console.error('WebSocket message error:', error);
        if (ws.readyState === WebSocket.OPEN) {
          try {
            ws.send(JSON.stringify({
              type: 'error',
              message: 'Failed to process message'
            }));
          } catch (sendError) {
            console.error('Failed to send error message:', sendError);
          }
        }
      }
    });

    ws.on('close', () => {
      connections.delete(connectionId);
    });

    ws.on('error', (error) => {
      console.error('WebSocket error:', error);
      connections.delete(connectionId);
    });
  });

  // REST API routes
  
  // Users
  app.get('/api/users/:id', async (req, res) => {
    try {
      const user = await storage.getUser(parseInt(req.params.id));
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get user' });
    }
  });

  app.post('/api/users', async (req, res) => {
    try {
      const validatedData = insertUserSchema.parse(req.body);
      const user = await storage.createUser(validatedData);
      res.status(201).json(user);
    } catch (error) {
      res.status(400).json({ message: 'Invalid user data' });
    }
  });

  app.get('/api/users/email/:email', async (req, res) => {
    try {
      const user = await storage.getUserByEmail(req.params.email);
      if (!user) {
        return res.status(404).json({ message: 'User not found' });
      }
      res.json(user);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get user' });
    }
  });

  // Conversations
  app.get('/api/conversations/:userId', async (req, res) => {
    try {
      const conversations = await storage.getConversations(
        parseInt(req.params.userId),
        parseInt(req.query.limit as string) || 50
      );
      res.json(conversations);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get conversations' });
    }
  });

  app.post('/api/conversations', async (req, res) => {
    try {
      const validatedData = insertConversationSchema.parse(req.body);
      const conversation = await storage.createConversation(validatedData);
      res.status(201).json(conversation);
    } catch (error) {
      res.status(400).json({ message: 'Invalid conversation data' });
    }
  });

  app.get('/api/conversations/agent/:agentId', async (req, res) => {
    try {
      const conversations = await storage.getConversationsByAgent(
        req.params.agentId,
        parseInt(req.query.limit as string) || 50
      );
      res.json(conversations);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get agent conversations' });
    }
  });

  // Family connections
  app.get('/api/family/:userId', async (req, res) => {
    try {
      const connections = await storage.getFamilyConnections(parseInt(req.params.userId));
      res.json(connections);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get family connections' });
    }
  });

  // Memories
  app.get('/api/memories/:familyId', async (req, res) => {
    try {
      const memories = await storage.getMemories(parseInt(req.params.familyId));
      res.json(memories);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get memories' });
    }
  });

  app.get('/api/memories/:familyId/quiz', async (req, res) => {
    try {
      const quiz = await agentService.createMemoryQuiz(parseInt(req.params.familyId));
      res.json(quiz);
    } catch (error) {
      res.status(500).json({ message: 'Failed to create memory quiz' });
    }
  });

  // Reminders
  app.get('/api/reminders/:userId', async (req, res) => {
    try {
      const reminders = await storage.getReminders(parseInt(req.params.userId));
      res.json(reminders);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get reminders' });
    }
  });

  app.get('/api/reminders/:userId/pending', async (req, res) => {
    try {
      const reminders = await storage.getPendingReminders(parseInt(req.params.userId));
      res.json(reminders);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get pending reminders' });
    }
  });

  app.post('/api/reminders', async (req, res) => {
    try {
      const validatedData = insertReminderSchema.parse(req.body);
      const reminder = await storage.createReminder(validatedData);
      res.status(201).json(reminder);
    } catch (error) {
      res.status(400).json({ message: 'Invalid reminder data' });
    }
  });

  app.patch('/api/reminders/:id/complete', async (req, res) => {
    try {
      await storage.completeReminder(parseInt(req.params.id));
      res.json({ message: 'Reminder completed' });
    } catch (error) {
      res.status(500).json({ message: 'Failed to complete reminder' });
    }
  });

  // Agent services
  app.post('/api/agents/message', async (req, res) => {
    try {
      const { userId, agentId, message } = req.body;
      console.log('Processing agent message:', { userId, agentId, message });
      const response = await agentService.processUserMessage(userId, agentId, message);
      res.json(response);
    } catch (error) {
      console.error('Agent message processing error:', error);
      res.status(500).json({ message: 'Failed to process message', error: error.message });
    }
  });

  app.get('/api/agents/communications', async (req, res) => {
    try {
      const communications = await agentService.getAgentCommunications(
        parseInt(req.query.limit as string) || 10
      );
      res.json(communications);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get agent communications' });
    }
  });

  // Inter-agent communication endpoints
  app.get('/api/agents/communications/:userId', async (req, res) => {
    try {
      const communications = await interAgentService.getAgentCommunications(
        parseInt(req.params.userId)
      );
      res.json(communications);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get user agent communications' });
    }
  });

  app.post('/api/agents/direct-message', async (req, res) => {
    try {
      const { fromAgent, toAgent, userId, message, priority } = req.body;
      
      const interAgentMessage = await interAgentService.sendAgentMessage(
        fromAgent,
        toAgent,
        {
          userId,
          triggerType: 'direct_message',
          priority: priority || 'medium',
          originalUserMessage: message
        }
      );

      // Process the message with the receiving agent
      const agentResponse = await interAgentService.processAgentMessage(
        toAgent,
        interAgentMessage
      );

      res.json({
        message: interAgentMessage.message,
        response: agentResponse.message,
        actions: agentResponse.actions,
        followUpRequired: agentResponse.followUpRequired
      });
    } catch (error) {
      console.error('Direct agent message error:', error);
      res.status(500).json({ message: 'Failed to send direct agent message' });
    }
  });

  app.get('/api/agents/insights/:userId', async (req, res) => {
    try {
      const insights = await agentService.generateFamilyInsights(parseInt(req.params.userId));
      res.json(insights);
    } catch (error) {
      res.status(500).json({ message: 'Failed to generate insights' });
    }
  });

  app.get('/api/agents/contact-time/:userId', async (req, res) => {
    try {
      const suggestion = await agentService.suggestOptimalContactTime(parseInt(req.params.userId));
      res.json(suggestion);
    } catch (error) {
      res.status(500).json({ message: 'Failed to suggest contact time' });
    }
  });

  // Care Notifications
  app.get('/api/care-notifications/:elderlyUserId', async (req, res) => {
    try {
      const notifications = await storage.getCareNotifications(parseInt(req.params.elderlyUserId));
      res.json(notifications);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get care notifications' });
    }
  });

  app.post('/api/care-notifications', async (req, res) => {
    try {
      const validatedData = insertCareNotificationSchema.parse(req.body);
      const notification = await storage.createCareNotification(validatedData);
      
      // Notify family members through agent service
      if (notification.elderlyUserId) {
        await agentService.notifyFamilyMembers(notification.elderlyUserId, notification);
      }
      
      res.status(201).json(notification);
    } catch (error) {
      res.status(400).json({ message: 'Invalid care notification data' });
    }
  });

  // Care coordination endpoint for creating appointment with family notification
  app.post('/api/care-coordination/appointment', async (req, res) => {
    try {
      const { elderlyUserId, title, description, scheduledTime, careProvider, assistanceNeeded } = req.body;
      
      const notification = await agentService.createCareNotification(
        elderlyUserId,
        'appointment',
        title,
        description,
        new Date(scheduledTime),
        careProvider,
        assistanceNeeded
      );
      
      res.status(201).json(notification);
    } catch (error) {
      res.status(400).json({ message: 'Failed to create care appointment' });
    }
  });

  // Care coordination endpoint for processing reminders
  app.post('/api/care-coordination/reminder', async (req, res) => {
    try {
      const { userId, reminderType, title, description, scheduledTime, careCoordination } = req.body;
      
      await agentService.processCareReminder(
        userId,
        reminderType,
        title,
        description,
        new Date(scheduledTime),
        careCoordination
      );
      
      res.status(201).json({ message: 'Care reminder processed and family notified' });
    } catch (error) {
      res.status(400).json({ message: 'Failed to process care reminder' });
    }
  });

  // Sleep Schedules
  app.get('/api/sleep-schedule/:userId', async (req, res) => {
    try {
      const schedule = await storage.getSleepSchedule(parseInt(req.params.userId));
      if (!schedule) {
        return res.status(404).json({ message: 'Sleep schedule not found' });
      }
      res.json(schedule);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get sleep schedule' });
    }
  });

  app.post('/api/sleep-schedule', async (req, res) => {
    try {
      const validatedData = insertSleepScheduleSchema.parse(req.body);
      const schedule = await storage.createSleepSchedule(validatedData);
      res.status(201).json(schedule);
    } catch (error) {
      res.status(400).json({ message: 'Invalid sleep schedule data' });
    }
  });

  app.patch('/api/sleep-schedule/:id', async (req, res) => {
    try {
      const schedule = await storage.updateSleepSchedule(parseInt(req.params.id), req.body);
      res.json(schedule);
    } catch (error) {
      res.status(500).json({ message: 'Failed to update sleep schedule' });
    }
  });

  app.post('/api/sleep-schedule/:userId/activate', async (req, res) => {
    try {
      const schedule = await storage.activateSleepSchedule(parseInt(req.params.userId));
      if (!schedule) {
        return res.status(404).json({ message: 'Sleep schedule not found' });
      }
      res.json(schedule);
    } catch (error) {
      res.status(500).json({ message: 'Failed to activate sleep schedule' });
    }
  });

  // Picture Frame Management
  app.get('/api/picture-frame/:elderlyUserId', async (req, res) => {
    try {
      const frame = await storage.getPictureFrame(parseInt(req.params.elderlyUserId));
      if (!frame) {
        return res.status(404).json({ message: 'Picture frame not found' });
      }
      res.json(frame);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get picture frame' });
    }
  });

  app.post('/api/picture-frame', async (req, res) => {
    try {
      const validatedData = insertPictureFrameSchema.parse(req.body);
      const frame = await storage.createPictureFrame(validatedData);
      res.status(201).json(frame);
    } catch (error) {
      res.status(400).json({ message: 'Invalid picture frame data' });
    }
  });

  app.patch('/api/picture-frame/:id', async (req, res) => {
    try {
      const frame = await storage.updatePictureFrame(parseInt(req.params.id), req.body);
      res.json(frame);
    } catch (error) {
      res.status(500).json({ message: 'Failed to update picture frame' });
    }
  });

  // Family Photo Management
  app.get('/api/family-photos/:pictureFrameId', async (req, res) => {
    try {
      const photos = await storage.getFamilyPhotos(parseInt(req.params.pictureFrameId));
      res.json(photos);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get family photos' });
    }
  });

  app.get('/api/recent-photos/:elderlyUserId', async (req, res) => {
    try {
      const limit = parseInt(req.query.limit as string) || 10;
      const photos = await storage.getRecentPhotos(parseInt(req.params.elderlyUserId), limit);
      res.json(photos);
    } catch (error) {
      res.status(500).json({ message: 'Failed to get recent photos' });
    }
  });

  app.post('/api/family-photos', async (req, res) => {
    try {
      const validatedData = insertFamilyPhotoSchema.parse(req.body);
      const photo = await storage.createFamilyPhoto(validatedData);
      
      // Broadcast photo update to connected picture frames
      const frame = await storage.getPictureFrame(photo.pictureFrameId);
      if (frame) {
        const photoUpdate = {
          type: 'new_photo',
          frameId: frame.id,
          photo: photo
        };
        
        // Broadcast to all connected clients
        connections.forEach((client) => {
          if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(photoUpdate));
          }
        });
      }
      
      res.status(201).json(photo);
    } catch (error) {
      res.status(400).json({ message: 'Invalid family photo data' });
    }
  });

  app.delete('/api/family-photos/:id', async (req, res) => {
    try {
      await storage.deleteFamilyPhoto(parseInt(req.params.id));
      res.json({ message: 'Photo deleted successfully' });
    } catch (error) {
      res.status(500).json({ message: 'Failed to delete photo' });
    }
  });

  app.patch('/api/family-photos/:id/viewed', async (req, res) => {
    try {
      await storage.markPhotoAsViewed(parseInt(req.params.id));
      res.json({ message: 'Photo marked as viewed' });
    } catch (error) {
      res.status(500).json({ message: 'Failed to mark photo as viewed' });
    }
  });

  // GenAI Protocol Agent Routes
  app.post('/api/genai/agent/message', async (req, res) => {
    try {
      const { agentId, message, context } = req.body;
      const response = await genaiAgentService.sendMessage(agentId, message, context);
      res.json({ response });
    } catch (error) {
      console.error('GenAI agent message error:', error);
      res.status(500).json({ error: 'Agent communication failed' });
    }
  });

  app.post('/api/genai/agent/communicate', async (req, res) => {
    try {
      const { fromAgent, toAgent, message, priority, context } = req.body;
      const result = await genaiAgentService.facilitateInterAgentCommunication(
        fromAgent, toAgent, message, priority, context
      );
      res.json(result);
    } catch (error) {
      console.error('GenAI inter-agent communication error:', error);
      res.status(500).json({ error: 'Inter-agent communication failed' });
    }
  });

  app.get('/api/genai/agent/status', async (req, res) => {
    try {
      const status = await genaiAgentService.getAgentStatus();
      res.json(status);
    } catch (error) {
      console.error('GenAI agent status error:', error);
      res.status(500).json({ error: 'Failed to get agent status' });
    }
  });

  app.post('/api/genai/agent/start', async (req, res) => {
    try {
      await genaiAgentService.startAgents();
      res.json({ message: 'Agents started successfully' });
    } catch (error) {
      console.error('GenAI agent start error:', error);
      res.status(500).json({ error: 'Failed to start agents' });
    }
  });

  app.post('/api/genai/agent/stop', async (req, res) => {
    try {
      await genaiAgentService.stopAgents();
      res.json({ message: 'Agents stopped successfully' });
    } catch (error) {
      console.error('GenAI agent stop error:', error);
      res.status(500).json({ error: 'Failed to stop agents' });
    }
  });

  app.post('/api/genai/agent/deploy', async (req, res) => {
    try {
      const success = await genaiAgentService.deployToGenAI();
      if (success) {
        res.json({ message: 'Agents deployed to GenAI successfully' });
      } else {
        res.status(500).json({ error: 'Failed to deploy agents to GenAI' });
      }
    } catch (error) {
      console.error('GenAI agent deploy error:', error);
      res.status(500).json({ error: 'Failed to deploy agents to GenAI' });
    }
  });

  // GenAI Protocol Compatible Endpoints
  
  // Grace Agent - GenAI Protocol Endpoint
  app.post('/api/agents/grace/v1/chat/completions', async (req, res) => {
    try {
      const { messages, model, temperature, max_tokens } = req.body;
      
      // Get the last user message
      const userMessage = messages.find((m: any) => m.role === 'user')?.content || '';
      
      // Call the agent service
      const response = await agentService.processUserMessage(1, 'grace', userMessage);
      
      // Format as GenAI protocol response
      const genaiResponse = {
        id: `chatcmpl-${Date.now()}`,
        object: 'chat.completion',
        created: Math.floor(Date.now() / 1000),
        model: 'grace-familyconnect',
        choices: [{
          index: 0,
          message: {
            role: 'assistant',
            content: response.message
          },
          finish_reason: 'stop'
        }],
        usage: {
          prompt_tokens: userMessage.split(' ').length,
          completion_tokens: response.message.split(' ').length,
          total_tokens: userMessage.split(' ').length + response.message.split(' ').length
        }
      };
      
      res.json(genaiResponse);
    } catch (error) {
      console.error('Grace GenAI endpoint error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  // Alex Agent - GenAI Protocol Endpoint
  app.post('/api/agents/alex/v1/chat/completions', async (req, res) => {
    try {
      const { messages, model, temperature, max_tokens } = req.body;
      
      // Get the last user message
      const userMessage = messages.find((m: any) => m.role === 'user')?.content || '';
      
      // Call the agent service
      const response = await agentService.processUserMessage(2, 'alex', userMessage);
      
      // Format as GenAI protocol response
      const genaiResponse = {
        id: `chatcmpl-${Date.now()}`,
        object: 'chat.completion',
        created: Math.floor(Date.now() / 1000),
        model: 'alex-familyconnect',
        choices: [{
          index: 0,
          message: {
            role: 'assistant',
            content: response.message
          },
          finish_reason: 'stop'
        }],
        usage: {
          prompt_tokens: userMessage.split(' ').length,
          completion_tokens: response.message.split(' ').length,
          total_tokens: userMessage.split(' ').length + response.message.split(' ').length
        }
      };
      
      res.json(genaiResponse);
    } catch (error) {
      console.error('Alex GenAI endpoint error:', error);
      res.status(500).json({ error: 'Internal server error' });
    }
  });

  // Agent Models Endpoint
  app.get('/api/agents/v1/models', async (req, res) => {
    res.json({
      object: 'list',
      data: [
        {
          id: 'grace-familyconnect',
          object: 'model',
          created: Math.floor(Date.now() / 1000),
          owned_by: 'familyconnect',
          permission: [],
          root: 'grace-familyconnect',
          parent: null
        },
        {
          id: 'alex-familyconnect',
          object: 'model', 
          created: Math.floor(Date.now() / 1000),
          owned_by: 'familyconnect',
          permission: [],
          root: 'alex-familyconnect',
          parent: null
        }
      ]
    });
  });

  return httpServer;
}
