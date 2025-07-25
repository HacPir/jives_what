import {
  users,
  conversations,
  familyConnections,
  memories,
  reminders,
  careNotifications,
  agentCommunications,
  sleepSchedules,
  pictureFrames,
  familyPhotos,
  type User,
  type InsertUser,
  type Conversation,
  type InsertConversation,
  type FamilyConnection,
  type InsertFamilyConnection,
  type Memory,
  type InsertMemory,
  type Reminder,
  type InsertReminder,
  type CareNotification,
  type InsertCareNotification,
  type AgentCommunication,
  type InsertAgentCommunication,
  type SleepSchedule,
  type InsertSleepSchedule,
  type PictureFrame,
  type InsertPictureFrame,
  type FamilyPhoto,
  type InsertFamilyPhoto,
} from "@shared/schema";

export interface IStorage {
  // Users
  getUser(id: number): Promise<User | undefined>;
  getUserByEmail(email: string): Promise<User | undefined>;
  createUser(user: InsertUser): Promise<User>;
  updateUser(id: number, updates: Partial<User>): Promise<User>;
  
  // Conversations
  getConversations(userId: number, limit?: number): Promise<Conversation[]>;
  createConversation(conversation: InsertConversation): Promise<Conversation>;
  getConversationsByAgent(agentId: string, limit?: number): Promise<Conversation[]>;
  
  // Family Connections
  getFamilyConnections(userId: number): Promise<FamilyConnection[]>;
  createFamilyConnection(connection: InsertFamilyConnection): Promise<FamilyConnection>;
  updateLastContact(connectionId: number): Promise<void>;
  
  // Memories
  getMemories(familyId: number): Promise<Memory[]>;
  createMemory(memory: InsertMemory): Promise<Memory>;
  getMemoriesByCategory(familyId: number, category: string): Promise<Memory[]>;
  
  // Reminders
  getReminders(userId: number): Promise<Reminder[]>;
  getPendingReminders(userId: number): Promise<Reminder[]>;
  createReminder(reminder: InsertReminder): Promise<Reminder>;
  completeReminder(id: number): Promise<void>;
  
  // Care Notifications
  getCareNotifications(elderlyUserId: number): Promise<CareNotification[]>;
  createCareNotification(notification: InsertCareNotification): Promise<CareNotification>;
  updateCareNotificationFamilyNotified(id: number, familyMemberIds: number[]): Promise<void>;
  
  // Agent Communications
  getAgentCommunications(limit?: number): Promise<AgentCommunication[]>;
  createAgentCommunication(communication: InsertAgentCommunication): Promise<AgentCommunication>;
  
  // Sleep Schedules
  getSleepSchedule(userId: number): Promise<SleepSchedule | undefined>;
  createSleepSchedule(schedule: InsertSleepSchedule): Promise<SleepSchedule>;
  updateSleepSchedule(id: number, updates: Partial<SleepSchedule>): Promise<SleepSchedule>;
  activateSleepSchedule(userId: number): Promise<SleepSchedule | undefined>;
  
  // Picture Frames
  getPictureFrame(elderlyUserId: number): Promise<PictureFrame | undefined>;
  createPictureFrame(frame: InsertPictureFrame): Promise<PictureFrame>;
  updatePictureFrame(id: number, updates: Partial<PictureFrame>): Promise<PictureFrame>;
  
  // Family Photos
  getFamilyPhotos(pictureFrameId: number): Promise<FamilyPhoto[]>;
  createFamilyPhoto(photo: InsertFamilyPhoto): Promise<FamilyPhoto>;
  deleteFamilyPhoto(id: number): Promise<void>;
  markPhotoAsViewed(id: number): Promise<void>;
  getRecentPhotos(elderlyUserId: number, limit?: number): Promise<FamilyPhoto[]>;
}

export class MemStorage implements IStorage {
  private users: Map<number, User> = new Map();
  private conversations: Map<number, Conversation> = new Map();
  private familyConnections: Map<number, FamilyConnection> = new Map();
  private memories: Map<number, Memory> = new Map();
  private reminders: Map<number, Reminder> = new Map();
  private careNotifications: Map<number, CareNotification> = new Map();
  private agentCommunications: Map<number, AgentCommunication> = new Map();
  private sleepSchedules: Map<number, SleepSchedule> = new Map();
  private pictureFrames: Map<number, PictureFrame> = new Map();
  private familyPhotos: Map<number, FamilyPhoto> = new Map();
  
  private currentUserId = 1;
  private currentConversationId = 1;
  private currentFamilyConnectionId = 1;
  private currentMemoryId = 1;
  private currentReminderId = 1;
  private currentCareNotificationId = 1;
  private currentAgentCommunicationId = 1;
  private currentSleepScheduleId = 1;
  private currentPictureFrameId = 1;
  private currentFamilyPhotoId = 1;

  constructor() {
    // Initialize with sample data
    this.initializeSampleData();
  }

  private initializeSampleData() {
    // Create sample users
    const elderlyUser: User = {
      id: this.currentUserId++,
      username: "margaret_smith",
      email: "margaret@example.com",
      name: "Margaret Smith",
      role: "elderly",
      preferredAgent: "grace",
      voiceEnabled: true,
      createdAt: new Date(),
    };

    const caregiverUser: User = {
      id: this.currentUserId++,
      username: "sarah_johnson",
      email: "sarah@example.com",
      name: "Sarah Johnson",
      role: "caregiver",
      preferredAgent: "alex",
      voiceEnabled: true,
      createdAt: new Date(),
    };

    this.users.set(elderlyUser.id, elderlyUser);
    this.users.set(caregiverUser.id, caregiverUser);

    // Create family connection
    const familyConnection: FamilyConnection = {
      id: this.currentFamilyConnectionId++,
      elderlyUserId: elderlyUser.id,
      caregiverUserId: caregiverUser.id,
      relationshipType: "child",
      lastContactDate: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      contactFrequency: "weekly",
      createdAt: new Date(),
    };

    this.familyConnections.set(familyConnection.id, familyConnection);

    // Create sample memories
    const memory: Memory = {
      id: this.currentMemoryId++,
      familyId: familyConnection.id,
      title: "Tommy's Soccer Game",
      description: "Grandson's first soccer game of the season. He scored the winning goal!",
      category: "sports",
      participants: [elderlyUser.id.toString(), caregiverUser.id.toString()],
      dateOfMemory: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 1 week ago
      createdAt: new Date(),
    };

    this.memories.set(memory.id, memory);

    // Create sample reminders
    const reminder: Reminder = {
      id: this.currentReminderId++,
      userId: elderlyUser.id,
      title: "Doctor Appointment",
      description: "Annual checkup with Dr. Williams",
      reminderType: "appointment",
      scheduledTime: new Date(Date.now() + 24 * 60 * 60 * 1000), // Tomorrow
      completed: false,
      priority: "medium",
      careCoordination: null,
      createdAt: new Date(),
    };

    this.reminders.set(reminder.id, reminder);

    // Create sample care notification
    const careNotification: CareNotification = {
      id: this.currentCareNotificationId++,
      elderlyUserId: elderlyUser.id,
      notificationType: "appointment",
      title: "Physical Therapy Session",
      description: "Weekly physical therapy at Sunshine Care Center. Family assistance may be helpful for transportation.",
      scheduledTime: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000), // 3 days from now
      careProvider: "Sunshine Care Center",
      familyInvited: true,
      assistanceNeeded: true,
      urgencyLevel: "normal",
      metadata: {
        therapistName: "Dr. Sarah Kim",
        duration: "45 minutes",
        location: "Room 203",
        transportationNeeded: true
      },
      notifiedFamilyMembers: [],
      createdAt: new Date(),
    };

    this.careNotifications.set(careNotification.id, careNotification);

    // Create sample picture frame
    const pictureFrame: PictureFrame = {
      id: this.currentPictureFrameId++,
      elderlyUserId: elderlyUser.id,
      deviceId: 'frame_001',
      deviceName: 'Living Room Frame',
      isActive: true,
      displayDuration: 30,
      brightness: 80,
      transitionEffect: 'fade',
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    // Create sample family photos
    const familyPhotos = [
      {
        id: this.currentFamilyPhotoId++,
        pictureFrameId: pictureFrame.id,
        senderUserId: caregiverUser.id,
        photoUrl: 'https://images.unsplash.com/photo-1511895426328-dc8714191300?w=400&h=300&fit=crop',
        caption: 'Family dinner last Sunday - we missed you!',
        isApproved: true,
        displayOrder: 1,
        uploadedAt: new Date(),
        sentAt: new Date(),
        viewedAt: null,
        metadata: { width: 400, height: 300, fileSize: 45000 },
      },
      {
        id: this.currentFamilyPhotoId++,
        pictureFrameId: pictureFrame.id,
        senderUserId: caregiverUser.id,
        photoUrl: 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400&h=300&fit=crop',
        caption: 'Beautiful sunset from our vacation',
        isApproved: true,
        displayOrder: 2,
        uploadedAt: new Date(),
        sentAt: new Date(),
        viewedAt: null,
        metadata: { width: 400, height: 300, fileSize: 52000 },
      },
      {
        id: this.currentFamilyPhotoId++,
        pictureFrameId: pictureFrame.id,
        senderUserId: caregiverUser.id,
        photoUrl: 'https://images.unsplash.com/photo-1542037104857-ffbb0972142d?w=400&h=300&fit=crop',
        caption: 'The grandkids at the park today',
        isApproved: true,
        displayOrder: 3,
        uploadedAt: new Date(),
        sentAt: new Date(),
        viewedAt: null,
        metadata: { width: 400, height: 300, fileSize: 48000 },
      },
    ];

    this.pictureFrames.set(pictureFrame.id, pictureFrame);
    
    familyPhotos.forEach(photo => {
      this.familyPhotos.set(photo.id, photo);
    });
  }

  // Users
  async getUser(id: number): Promise<User | undefined> {
    return this.users.get(id);
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    return Array.from(this.users.values()).find(user => user.email === email);
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const user: User = {
      ...insertUser,
      id: this.currentUserId++,
      preferredAgent: insertUser.preferredAgent || null,
      voiceEnabled: insertUser.voiceEnabled ?? true,
      createdAt: new Date(),
    };
    this.users.set(user.id, user);
    return user;
  }

  async updateUser(id: number, updates: Partial<User>): Promise<User> {
    const user = this.users.get(id);
    if (!user) throw new Error("User not found");
    
    const updatedUser = { ...user, ...updates };
    this.users.set(id, updatedUser);
    return updatedUser;
  }

  // Conversations
  async getConversations(userId: number, limit: number = 50): Promise<Conversation[]> {
    return Array.from(this.conversations.values())
      .filter(conv => conv.userId === userId)
      .sort((a, b) => (b.timestamp?.getTime() || 0) - (a.timestamp?.getTime() || 0))
      .slice(0, limit);
  }

  async createConversation(insertConversation: InsertConversation): Promise<Conversation> {
    const conversation: Conversation = {
      ...insertConversation,
      id: this.currentConversationId++,
      userId: insertConversation.userId || null,
      response: insertConversation.response || null,
      emotionalState: insertConversation.emotionalState || null,
      metadata: insertConversation.metadata || null,
      timestamp: new Date(),
    };
    this.conversations.set(conversation.id, conversation);
    return conversation;
  }

  async getConversationsByAgent(agentId: string, limit: number = 50): Promise<Conversation[]> {
    return Array.from(this.conversations.values())
      .filter(conv => conv.agentId === agentId)
      .sort((a, b) => (b.timestamp?.getTime() || 0) - (a.timestamp?.getTime() || 0))
      .slice(0, limit);
  }

  // Family Connections
  async getFamilyConnections(userId: number): Promise<FamilyConnection[]> {
    return Array.from(this.familyConnections.values())
      .filter(conn => conn.elderlyUserId === userId || conn.caregiverUserId === userId);
  }

  async createFamilyConnection(insertConnection: InsertFamilyConnection): Promise<FamilyConnection> {
    const connection: FamilyConnection = {
      ...insertConnection,
      id: this.currentFamilyConnectionId++,
      elderlyUserId: insertConnection.elderlyUserId || null,
      caregiverUserId: insertConnection.caregiverUserId || null,
      lastContactDate: insertConnection.lastContactDate || null,
      contactFrequency: insertConnection.contactFrequency || null,
      createdAt: new Date(),
    };
    this.familyConnections.set(connection.id, connection);
    return connection;
  }

  async updateLastContact(connectionId: number): Promise<void> {
    const connection = this.familyConnections.get(connectionId);
    if (connection) {
      connection.lastContactDate = new Date();
      this.familyConnections.set(connectionId, connection);
    }
  }

  // Memories
  async getMemories(familyId: number): Promise<Memory[]> {
    return Array.from(this.memories.values())
      .filter(memory => memory.familyId === familyId)
      .sort((a, b) => (b.dateOfMemory?.getTime() || 0) - (a.dateOfMemory?.getTime() || 0));
  }

  async createMemory(insertMemory: InsertMemory): Promise<Memory> {
    const memory: Memory = {
      ...insertMemory,
      id: this.currentMemoryId++,
      familyId: insertMemory.familyId || null,
      participants: insertMemory.participants || null,
      dateOfMemory: insertMemory.dateOfMemory || null,
      createdAt: new Date(),
    };
    this.memories.set(memory.id, memory);
    return memory;
  }

  async getMemoriesByCategory(familyId: number, category: string): Promise<Memory[]> {
    return Array.from(this.memories.values())
      .filter(memory => memory.familyId === familyId && memory.category === category);
  }

  // Reminders
  async getReminders(userId: number): Promise<Reminder[]> {
    return Array.from(this.reminders.values())
      .filter(reminder => reminder.userId === userId)
      .sort((a, b) => (a.scheduledTime?.getTime() || 0) - (b.scheduledTime?.getTime() || 0));
  }

  async getPendingReminders(userId: number): Promise<Reminder[]> {
    return Array.from(this.reminders.values())
      .filter(reminder => 
        reminder.userId === userId && 
        !reminder.completed &&
        (reminder.scheduledTime?.getTime() || 0) <= Date.now()
      );
  }

  async createReminder(insertReminder: InsertReminder): Promise<Reminder> {
    const reminder: Reminder = {
      ...insertReminder,
      id: this.currentReminderId++,
      userId: insertReminder.userId || null,
      description: insertReminder.description || null,
      completed: insertReminder.completed ?? false,
      priority: insertReminder.priority || "medium",
      careCoordination: insertReminder.careCoordination || null,
      createdAt: new Date(),
    };
    this.reminders.set(reminder.id, reminder);
    return reminder;
  }

  async completeReminder(id: number): Promise<void> {
    const reminder = this.reminders.get(id);
    if (reminder) {
      reminder.completed = true;
      this.reminders.set(id, reminder);
    }
  }

  // Care Notifications
  async getCareNotifications(elderlyUserId: number): Promise<CareNotification[]> {
    return Array.from(this.careNotifications.values())
      .filter(notification => notification.elderlyUserId === elderlyUserId)
      .sort((a, b) => (a.scheduledTime?.getTime() || 0) - (b.scheduledTime?.getTime() || 0));
  }

  async createCareNotification(insertNotification: InsertCareNotification): Promise<CareNotification> {
    const notification: CareNotification = {
      ...insertNotification,
      id: this.currentCareNotificationId++,
      elderlyUserId: insertNotification.elderlyUserId || null,
      scheduledTime: insertNotification.scheduledTime || null,
      careProvider: insertNotification.careProvider || null,
      familyInvited: insertNotification.familyInvited ?? true,
      assistanceNeeded: insertNotification.assistanceNeeded ?? false,
      urgencyLevel: insertNotification.urgencyLevel || "normal",
      metadata: insertNotification.metadata || null,
      notifiedFamilyMembers: insertNotification.notifiedFamilyMembers || [],
      createdAt: new Date(),
    };
    this.careNotifications.set(notification.id, notification);
    return notification;
  }

  async updateCareNotificationFamilyNotified(id: number, familyMemberIds: number[]): Promise<void> {
    const notification = this.careNotifications.get(id);
    if (notification) {
      notification.notifiedFamilyMembers = familyMemberIds.map(id => id.toString());
      this.careNotifications.set(id, notification);
    }
  }

  // Agent Communications
  async getAgentCommunications(limit: number = 50): Promise<AgentCommunication[]> {
    return Array.from(this.agentCommunications.values())
      .sort((a, b) => (b.timestamp?.getTime() || 0) - (a.timestamp?.getTime() || 0))
      .slice(0, limit);
  }

  async createAgentCommunication(insertCommunication: InsertAgentCommunication): Promise<AgentCommunication> {
    const communication: AgentCommunication = {
      ...insertCommunication,
      id: this.currentAgentCommunicationId++,
      context: insertCommunication.context || null,
      timestamp: new Date(),
    };
    this.agentCommunications.set(communication.id, communication);
    return communication;
  }

  // Sleep Schedules
  async getSleepSchedule(userId: number): Promise<SleepSchedule | undefined> {
    return Array.from(this.sleepSchedules.values()).find(schedule => schedule.userId === userId);
  }

  async createSleepSchedule(insertSchedule: InsertSleepSchedule): Promise<SleepSchedule> {
    const schedule: SleepSchedule = {
      ...insertSchedule,
      id: this.currentSleepScheduleId++,
      volume: insertSchedule.volume ?? 50,
      isActive: insertSchedule.isActive ?? true,
      musicPreferences: insertSchedule.musicPreferences ?? null,
      sleepGoals: insertSchedule.sleepGoals ?? null,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.sleepSchedules.set(schedule.id, schedule);
    return schedule;
  }

  async updateSleepSchedule(id: number, updates: Partial<SleepSchedule>): Promise<SleepSchedule> {
    const schedule = this.sleepSchedules.get(id);
    if (!schedule) {
      throw new Error(`Sleep schedule with id ${id} not found`);
    }
    const updatedSchedule = { ...schedule, ...updates, updatedAt: new Date() };
    this.sleepSchedules.set(id, updatedSchedule);
    return updatedSchedule;
  }

  async activateSleepSchedule(userId: number): Promise<SleepSchedule | undefined> {
    const schedule = await this.getSleepSchedule(userId);
    if (schedule) {
      return this.updateSleepSchedule(schedule.id, { isActive: true });
    }
    return undefined;
  }

  // Picture Frames
  async getPictureFrame(elderlyUserId: number): Promise<PictureFrame | undefined> {
    return Array.from(this.pictureFrames.values()).find(frame => frame.elderlyUserId === elderlyUserId);
  }

  async createPictureFrame(insertFrame: InsertPictureFrame): Promise<PictureFrame> {
    const frame: PictureFrame = {
      ...insertFrame,
      id: this.currentPictureFrameId++,
      isActive: insertFrame.isActive ?? true,
      displayDuration: insertFrame.displayDuration ?? 30,
      brightness: insertFrame.brightness ?? 80,
      transitionEffect: insertFrame.transitionEffect ?? 'fade',
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    this.pictureFrames.set(frame.id, frame);
    return frame;
  }

  async updatePictureFrame(id: number, updates: Partial<PictureFrame>): Promise<PictureFrame> {
    const frame = this.pictureFrames.get(id);
    if (!frame) {
      throw new Error(`Picture frame with id ${id} not found`);
    }
    const updatedFrame = { ...frame, ...updates, updatedAt: new Date() };
    this.pictureFrames.set(id, updatedFrame);
    return updatedFrame;
  }

  // Family Photos
  async getFamilyPhotos(pictureFrameId: number): Promise<FamilyPhoto[]> {
    return Array.from(this.familyPhotos.values())
      .filter(photo => photo.pictureFrameId === pictureFrameId)
      .sort((a, b) => (b.sentAt?.getTime() || 0) - (a.sentAt?.getTime() || 0));
  }

  async createFamilyPhoto(insertPhoto: InsertFamilyPhoto): Promise<FamilyPhoto> {
    const photo: FamilyPhoto = {
      ...insertPhoto,
      id: this.currentFamilyPhotoId++,
      caption: insertPhoto.caption ?? null,
      isApproved: insertPhoto.isApproved ?? true,
      displayOrder: insertPhoto.displayOrder ?? 0,
      uploadedAt: new Date(),
      sentAt: new Date(),
      viewedAt: insertPhoto.viewedAt ?? null,
      metadata: insertPhoto.metadata ?? null,
    };
    this.familyPhotos.set(photo.id, photo);
    return photo;
  }

  async deleteFamilyPhoto(id: number): Promise<void> {
    this.familyPhotos.delete(id);
  }

  async markPhotoAsViewed(id: number): Promise<void> {
    const photo = this.familyPhotos.get(id);
    if (photo) {
      photo.viewedAt = new Date();
      this.familyPhotos.set(id, photo);
    }
  }

  async getRecentPhotos(elderlyUserId: number, limit: number = 10): Promise<FamilyPhoto[]> {
    const frame = await this.getPictureFrame(elderlyUserId);
    if (!frame) return [];
    
    const photos = await this.getFamilyPhotos(frame.id);
    return photos.slice(0, limit);
  }
}

import { DatabaseStorage } from "./db-storage";

export const storage = new DatabaseStorage();
