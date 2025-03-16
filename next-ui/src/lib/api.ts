import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080/api';

export interface Chat {
  id: string;
  name: string;
  created_at: string;
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatWithMessages extends Chat {
  messages: Message[];
}

// API client for interacting with the backend
const api = {
  // Get all chat sessions
  getChats: async (): Promise<Chat[]> => {
    const response = await axios.get(`${API_BASE_URL}/chats`);
    return response.data;
  },

  // Get a single chat with messages
  getChat: async (chatId: string): Promise<ChatWithMessages> => {
    const response = await axios.get(`${API_BASE_URL}/chats/${chatId}`);
    return response.data;
  },

  // Create a new chat
  createChat: async (name: string = 'New Chat'): Promise<Chat> => {
    const response = await axios.post(`${API_BASE_URL}/chats`, { name });
    return response.data;
  },

  // Send a message in a chat
  sendMessage: async (chatId: string, content: string): Promise<Message> => {
    const response = await axios.post(`${API_BASE_URL}/chats/${chatId}/messages`, { content });
    return response.data;
  },

  // Get all messages for a chat
  getMessages: async (chatId: string): Promise<Message[]> => {
    const response = await axios.get(`${API_BASE_URL}/chats/${chatId}/messages`);
    return response.data;
  },

  // Delete a chat
  deleteChat: async (chatId: string): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/chats/${chatId}`);
  }
};

export default api;
