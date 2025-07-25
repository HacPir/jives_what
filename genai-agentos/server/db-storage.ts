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
  type InsertFamilyPhoto
} from "@shared/schema";
import { db } from "./db";
import { eq, desc, and, or, lte } from "drizzle-orm";
import { IStorage } from "./storage";

export class DatabaseStorage implements IStorage {
  // Initialize with sample data
  async initialize() {
    // Check if we already have data
    const existingUsers = await db.select().from(users).limit(1);
    if (existingUsers.length > 0) {
      return; // Data already exists
    }

    // Create sample users
    const elderlyUser = await db.insert(users).values({
      username: "margaret_smith",
      email: "margaret.smith@example.com",
      name: "Margaret Smith",
      role: "elderly",
      preferences: {
        fontSize: "large",
        voiceEnabled: true,
        theme: "light"
      }
    }).returning();

    const caregiverUser = await db.insert(users).values({
      username: "sarah_johnson",
      email: "sarah.johnson@example.com",
      name: "Sarah Johnson",
      role: "caregiver",
      preferences: {
        notifications: true,
        theme: "light"
      }
    }).returning();

    const elderlyUserId = elderlyUser[0].id;
    const caregiverUserId = caregiverUser[0].id;

    // Create family connection
    await db.insert(familyConnections).values({
      elderlyUserId,
      caregiverUserId,
      relationshipType: "daughter",
      contactFrequency: "daily",
      lastContactDate: new Date()
    });

    // Create sample memory
    await db.insert(memories).values({
      familyId: 1,
      title: "Summer Vacation 2023",
      description: "Family trip to the beach where we built sandcastles and collected seashells",
      category: "family",
      dateOfMemory: new Date("2023-07-15"),
      createdBy: elderlyUserId
    });

    // Create sample reminder
    await db.insert(reminders).values({
      userId: elderlyUserId,
      title: "Doctor Appointment",
      description: "Annual checkup with Dr. Wilson",
      reminderType: "medical",
      scheduledTime: new Date(Date.now() + 24 * 60 * 60 * 1000),
      completed: false
    });

    // Create sample care notification
    await db.insert(careNotifications).values({
      elderlyUserId,
      notificationType: "appointment",
      title: "Physical Therapy Session",
      description: "Weekly physical therapy session at City Wellness Center",
      scheduledTime: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000),
      careProvider: "City Wellness Center",
      familyInvited: false,
      assistanceNeeded: true,
      urgencyLevel: "normal"
    });

    // Create picture frame
    const pictureFrame = await db.insert(pictureFrames).values({
      elderlyUserId,
      deviceId: "frame_001",
      deviceName: "Living Room Frame",
      displayDuration: 10,
      brightness: 80,
      isActive: true,
      transitionEffect: "fade"
    }).returning();

    // Add sample family photos
    await db.insert(familyPhotos).values([
      {
        pictureFrameId: pictureFrame[0].id,
        senderUserId: caregiverUserId,
        photoUrl: "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=800&h=600&fit=crop",
        caption: "Family gathering last weekend",
        uploadedAt: new Date()
      },
      {
        pictureFrameId: pictureFrame[0].id,
        senderUserId: caregiverUserId,
        photoUrl: "https://images.unsplash.com/photo-1609220136736-443140cffec6?w=800&h=600&fit=crop",
        caption: "Beautiful sunset from the garden",
        uploadedAt: new Date(Date.now() - 24 * 60 * 60 * 1000)
      }
    ]);
  }

  // Users
  async getUser(id: number): Promise<User | undefined> {
    await this.initialize();
    const [user] = await db.select().from(users).where(eq(users.id, id));
    return user || undefined;
  }

  async getUserByEmail(email: string): Promise<User | undefined> {
    await this.initialize();
    const [user] = await db.select().from(users).where(eq(users.email, email));
    return user || undefined;
  }

  async createUser(insertUser: InsertUser): Promise<User> {
    const [user] = await db.insert(users).values(insertUser).returning();
    return user;
  }

  async updateUser(id: number, updates: Partial<User>): Promise<User> {
    const [user] = await db.update(users).set(updates).where(eq(users.id, id)).returning();
    return user;
  }

  // Conversations
  async getConversations(userId: number, limit: number = 50): Promise<Conversation[]> {
    try {
      console.log('Executing getConversations query for userId:', userId);
      const result = await db
        .select()
        .from(conversations)
        .where(eq(conversations.userId, userId))
        .orderBy(desc(conversations.timestamp))
        .limit(limit);
      console.log('Query result:', result);
      return result;
    } catch (error) {
      console.error('Database query error in getConversations:', error);
      throw error;
    }
  }

  async createConversation(insertConversation: InsertConversation): Promise<Conversation> {
    const [conversation] = await db.insert(conversations).values(insertConversation).returning();
    return conversation;
  }

  async getConversationsByAgent(agentId: string, limit: number = 50): Promise<Conversation[]> {
    return await db
      .select()
      .from(conversations)
      .where(eq(conversations.agentId, agentId))
      .orderBy(desc(conversations.timestamp))
      .limit(limit);
  }

  // Family Connections
  async getFamilyConnections(userId: number): Promise<FamilyConnection[]> {
    return await db
      .select()
      .from(familyConnections)
      .where(
        or(
          eq(familyConnections.elderlyUserId, userId),
          eq(familyConnections.caregiverUserId, userId)
        )
      );
  }

  async createFamilyConnection(insertConnection: InsertFamilyConnection): Promise<FamilyConnection> {
    const [connection] = await db.insert(familyConnections).values(insertConnection).returning();
    return connection;
  }

  async updateLastContact(connectionId: number): Promise<void> {
    await db
      .update(familyConnections)
      .set({ lastContactDate: new Date() })
      .where(eq(familyConnections.id, connectionId));
  }

  // Memories
  async getMemories(familyId: number): Promise<Memory[]> {
    return await db
      .select()
      .from(memories)
      .where(eq(memories.familyId, familyId))
      .orderBy(desc(memories.dateOfMemory));
  }

  async createMemory(insertMemory: InsertMemory): Promise<Memory> {
    const [memory] = await db.insert(memories).values(insertMemory).returning();
    return memory;
  }

  async getMemoriesByCategory(familyId: number, category: string): Promise<Memory[]> {
    return await db
      .select()
      .from(memories)
      .where(
        and(
          eq(memories.familyId, familyId),
          eq(memories.category, category)
        )
      )
      .orderBy(desc(memories.dateOfMemory));
  }

  // Reminders
  async getReminders(userId: number): Promise<Reminder[]> {
    return await db
      .select()
      .from(reminders)
      .where(eq(reminders.userId, userId))
      .orderBy(desc(reminders.scheduledTime));
  }

  async getPendingReminders(userId: number): Promise<Reminder[]> {
    return await db
      .select()
      .from(reminders)
      .where(
        and(
          eq(reminders.userId, userId),
          eq(reminders.completed, false),
          lte(reminders.scheduledTime, new Date())
        )
      )
      .orderBy(desc(reminders.scheduledTime));
  }

  async createReminder(insertReminder: InsertReminder): Promise<Reminder> {
    const [reminder] = await db.insert(reminders).values(insertReminder).returning();
    return reminder;
  }

  async completeReminder(id: number): Promise<void> {
    await db
      .update(reminders)
      .set({ completed: true })
      .where(eq(reminders.id, id));
  }

  // Care Notifications
  async getCareNotifications(elderlyUserId: number): Promise<CareNotification[]> {
    return await db
      .select()
      .from(careNotifications)
      .where(eq(careNotifications.elderlyUserId, elderlyUserId))
      .orderBy(desc(careNotifications.createdAt));
  }

  async createCareNotification(insertNotification: InsertCareNotification): Promise<CareNotification> {
    const [notification] = await db.insert(careNotifications).values(insertNotification).returning();
    return notification;
  }

  async updateCareNotificationFamilyNotified(id: number, familyMemberIds: number[]): Promise<void> {
    await db
      .update(careNotifications)
      .set({ notifiedFamilyMembers: familyMemberIds.map(String) })
      .where(eq(careNotifications.id, id));
  }

  // Agent Communications
  async getAgentCommunications(limit: number = 50): Promise<AgentCommunication[]> {
    return await db
      .select()
      .from(agentCommunications)
      .orderBy(desc(agentCommunications.timestamp))
      .limit(limit);
  }

  async createAgentCommunication(insertCommunication: InsertAgentCommunication): Promise<AgentCommunication> {
    const [communication] = await db.insert(agentCommunications).values(insertCommunication).returning();
    return communication;
  }

  // Sleep Schedules
  async getSleepSchedule(userId: number): Promise<SleepSchedule | undefined> {
    const [schedule] = await db
      .select()
      .from(sleepSchedules)
      .where(eq(sleepSchedules.userId, userId));
    return schedule || undefined;
  }

  async createSleepSchedule(insertSchedule: InsertSleepSchedule): Promise<SleepSchedule> {
    const [schedule] = await db.insert(sleepSchedules).values(insertSchedule).returning();
    return schedule;
  }

  async updateSleepSchedule(id: number, updates: Partial<SleepSchedule>): Promise<SleepSchedule> {
    const [schedule] = await db.update(sleepSchedules).set(updates).where(eq(sleepSchedules.id, id)).returning();
    return schedule;
  }

  async activateSleepSchedule(userId: number): Promise<SleepSchedule | undefined> {
    const [schedule] = await db
      .update(sleepSchedules)
      .set({ isActive: true })
      .where(eq(sleepSchedules.userId, userId))
      .returning();
    return schedule || undefined;
  }

  // Picture Frames
  async getPictureFrame(elderlyUserId: number): Promise<PictureFrame | undefined> {
    const [frame] = await db
      .select()
      .from(pictureFrames)
      .where(eq(pictureFrames.elderlyUserId, elderlyUserId));
    return frame || undefined;
  }

  async createPictureFrame(insertFrame: InsertPictureFrame): Promise<PictureFrame> {
    const [frame] = await db.insert(pictureFrames).values(insertFrame).returning();
    return frame;
  }

  async updatePictureFrame(id: number, updates: Partial<PictureFrame>): Promise<PictureFrame> {
    const [frame] = await db.update(pictureFrames).set(updates).where(eq(pictureFrames.id, id)).returning();
    return frame;
  }

  // Family Photos
  async getFamilyPhotos(pictureFrameId: number): Promise<FamilyPhoto[]> {
    return await db
      .select()
      .from(familyPhotos)
      .where(eq(familyPhotos.pictureFrameId, pictureFrameId))
      .orderBy(desc(familyPhotos.uploadedAt));
  }

  async createFamilyPhoto(insertPhoto: InsertFamilyPhoto): Promise<FamilyPhoto> {
    const [photo] = await db.insert(familyPhotos).values(insertPhoto).returning();
    return photo;
  }

  async deleteFamilyPhoto(id: number): Promise<void> {
    await db.delete(familyPhotos).where(eq(familyPhotos.id, id));
  }

  async markPhotoAsViewed(id: number): Promise<void> {
    await db
      .update(familyPhotos)
      .set({ viewedAt: new Date() })
      .where(eq(familyPhotos.id, id));
  }

  async getRecentPhotos(elderlyUserId: number, limit: number = 10): Promise<FamilyPhoto[]> {
    // First get the picture frame for this elderly user
    const frame = await this.getPictureFrame(elderlyUserId);
    if (!frame) return [];

    return await db
      .select()
      .from(familyPhotos)
      .where(eq(familyPhotos.pictureFrameId, frame.id))
      .orderBy(desc(familyPhotos.uploadedAt))
      .limit(limit);
  }
}