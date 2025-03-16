"use client";

import { useEffect, useState } from 'react';
import api, { Chat, Message } from '@/lib/api';
import Sidebar from '@/components/Sidebar';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  const [chats, setChats] = useState<Chat[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch all chats on component mount
  useEffect(() => {
    const fetchChats = async () => {
      try {
        const chatsData = await api.getChats();
        setChats(chatsData);
        
        // If there are chats, select the first one
        if (chatsData.length > 0 && !currentChatId) {
          setCurrentChatId(chatsData[0].id);
        }
      } catch (error) {
        console.error('Error fetching chats:', error);
      }
    };
    
    fetchChats();
  }, [currentChatId]);

  // Fetch messages when current chat changes
  useEffect(() => {
    if (currentChatId) {
      const fetchMessages = async () => {
        try {
          const chatData = await api.getChat(currentChatId);
          setMessages(chatData.messages);
        } catch (error) {
          console.error('Error fetching messages:', error);
        }
      };
      
      fetchMessages();
    } else {
      setMessages([]);
    }
  }, [currentChatId]);

  // Handle creating a new chat
  const handleCreateChat = async () => {
    try {
      const newChat = await api.createChat();
      setChats([...chats, newChat]);
      setCurrentChatId(newChat.id);
    } catch (error) {
      console.error('Error creating chat:', error);
    }
  };

  // Handle selecting a chat
  const handleSelectChat = (chatId: string) => {
    setCurrentChatId(chatId);
  };

  // Handle deleting a chat
  const handleDeleteChat = async (chatId: string) => {
    try {
      await api.deleteChat(chatId);
      setChats(chats.filter(chat => chat.id !== chatId));
      
      // If the deleted chat was the current one, select another chat or set to null
      if (currentChatId === chatId) {
        const remainingChats = chats.filter(chat => chat.id !== chatId);
        setCurrentChatId(remainingChats.length > 0 ? remainingChats[0].id : null);
      }
    } catch (error) {
      console.error('Error deleting chat:', error);
    }
  };

  // Handle sending a message
  const handleSendMessage = async (content: string) => {
    if (!currentChatId) return;
    
    // Optimistically add user message to UI
    const tempUserMessage: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date().toISOString()
    };
    
    setMessages([...messages, tempUserMessage]);
    setIsLoading(true);
    
    try {
      // Send message to API
      const userMessage = await api.sendMessage(currentChatId, content);
      
      // Replace temp message with actual message from API
      setMessages(prevMessages => 
        prevMessages.map(msg => 
          msg.id === tempUserMessage.id ? userMessage : msg
        )
      );
      
      // Fetch the assistant's response
      const updatedMessages = await api.getMessages(currentChatId);
      setMessages(updatedMessages);
    } catch (error) {
      console.error('Error sending message:', error);
      // Remove the temp message if there was an error
      setMessages(messages => messages.filter(msg => msg.id !== tempUserMessage.id));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100 dark:bg-gray-950">
      <Sidebar
        chats={chats}
        currentChatId={currentChatId}
        onSelectChat={handleSelectChat}
        onCreateChat={handleCreateChat}
        onDeleteChat={handleDeleteChat}
      />
      <div className="flex-1 flex flex-col">
        <ChatInterface
          currentChatId={currentChatId}
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}
