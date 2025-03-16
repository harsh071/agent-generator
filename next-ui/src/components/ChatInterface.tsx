import React, { useState, useEffect, useRef } from 'react';
import { Message } from '@/lib/api';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

interface ChatInterfaceProps {
  currentChatId: string | null;
  messages: Message[];
  onSendMessage: (content: string) => Promise<void>;
  isLoading: boolean;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  currentChatId,
  messages,
  onSendMessage,
  isLoading,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messageContainerRef = useRef<HTMLDivElement>(null);
  const [autoScroll, setAutoScroll] = useState(true);
  const [showScrollButton, setShowScrollButton] = useState(false);

  // Handle scrolling and show/hide scroll button
  const handleScroll = () => {
    if (!messageContainerRef.current) return;
    
    const { scrollTop, scrollHeight, clientHeight } = messageContainerRef.current;
    const isScrolledUp = scrollHeight - scrollTop - clientHeight > 100;
    
    setAutoScroll(!isScrolledUp);
    setShowScrollButton(isScrolledUp);
  };

  // Scroll to bottom when messages change if autoScroll is enabled
  useEffect(() => {
    if (autoScroll && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, autoScroll]);

  // Scroll to bottom manually
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    setAutoScroll(true);
    setShowScrollButton(false);
  };

  return (
    <div className="flex flex-col h-full relative">
      {currentChatId ? (
        <>
          {/* Chat header */}
          <div className="sticky top-0 z-10 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 p-4 md:px-6">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100 truncate">
                Chat Session
              </h2>
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {messages.length} message{messages.length !== 1 ? 's' : ''}
                </span>
              </div>
            </div>
          </div>
          
          {/* Messages container */}
          <div 
            ref={messageContainerRef}
            className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 scroll-smooth"
            onScroll={handleScroll}
          >
            {messages.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center text-gray-500 max-w-md p-6 rounded-lg bg-gray-50 dark:bg-gray-800/50">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-12 w-12 mx-auto mb-4 text-gray-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                  <h3 className="text-xl font-semibold mb-2">Start a conversation</h3>
                  <p className="mb-4">Ask about agent generation or code examples</p>
                  <div className="text-sm bg-gray-100 dark:bg-gray-700 p-3 rounded-md text-left">
                    <p className="font-medium mb-2">Example questions:</p>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>How do I create a new agent?</li>
                      <li>Show me an example of a Python agent</li>
                      <li>What are the best practices for agent development?</li>
                    </ul>
                  </div>
                </div>
              </div>
            ) : (
              <>
                <div className="pb-2 mb-4 border-b border-gray-200 dark:border-gray-700">
                  <p className="text-xs text-center text-gray-500">
                    Beginning of conversation
                  </p>
                </div>
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                <div ref={messagesEndRef} className="h-4" />
              </>
            )}
          </div>
          
          {/* Scroll to bottom button */}
          {showScrollButton && (
            <button
              onClick={scrollToBottom}
              className="absolute bottom-20 right-4 p-2 bg-gray-800 dark:bg-gray-700 text-white rounded-full shadow-lg z-10 hover:bg-gray-700 dark:hover:bg-gray-600 transition-all"
              aria-label="Scroll to bottom"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 14l-7 7m0 0l-7-7m7 7V3"
                />
              </svg>
            </button>
          )}
          
          {/* Chat input */}
          <ChatInput onSendMessage={onSendMessage} isLoading={isLoading} />
        </>
      ) : (
        <div className="flex items-center justify-center h-full p-4">
          <div className="text-center text-gray-500 max-w-md p-8 rounded-lg bg-gray-50 dark:bg-gray-800/50">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-16 w-16 mx-auto mb-4 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
            <h3 className="text-xl font-semibold mb-2">No chat selected</h3>
            <p className="mb-4">Select a chat from the sidebar or create a new one</p>
            <div className="text-sm bg-gray-100 dark:bg-gray-700 p-3 rounded-md text-left">
              <p>Click the <strong>New Chat</strong> button in the sidebar to start a new conversation.</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatInterface;
