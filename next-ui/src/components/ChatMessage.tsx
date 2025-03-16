import React from 'react';
import { Message } from '@/lib/api';
import CodeBlock from './CodeBlock';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  message: Message;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  // Function to detect and parse code blocks in markdown format
  const parseContent = (content: string) => {
    // Regular expression to match markdown code blocks with language
    const codeBlockRegex = /```(\w+)?\n([\s\S]*?)```/g;
    
    // Split the content by code blocks
    const parts = [];
    let lastIndex = 0;
    let match;
    
    while ((match = codeBlockRegex.exec(content)) !== null) {
      // Add text before the code block
      if (match.index > lastIndex) {
        parts.push({
          type: 'text',
          content: content.slice(lastIndex, match.index)
        });
      }
      
      // Add the code block
      parts.push({
        type: 'code',
        language: match[1] || 'text',
        content: match[2].trim(),
        filename: match[1] === 'filename' ? match[2].split('\n')[0].trim() : undefined
      });
      
      lastIndex = match.index + match[0].length;
    }
    
    // Add remaining text
    if (lastIndex < content.length) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex)
      });
    }
    
    return parts;
  };

  const parts = parseContent(message.content);
  const timestamp = new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
      <div 
        className={`max-w-[80%] p-3 rounded-lg ${
          message.role === 'user' 
            ? 'bg-blue-600 text-white' 
            : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100'
        }`}
      >
        <div className="flex items-center mb-1">
          <span className="font-medium">
            {message.role === 'user' ? 'You' : 'Assistant'}
          </span>
          <span className="text-xs opacity-70 ml-2">{timestamp}</span>
        </div>
        
        {parts.map((part, index) => (
          <React.Fragment key={index}>
            {part.type === 'text' && (
              <div className="whitespace-pre-wrap markdown-content">
                <ReactMarkdown>
                  {part.content}
                </ReactMarkdown>
              </div>
            )}
            {part.type === 'code' && (
              <CodeBlock 
                code={part.content} 
                language={part.language!}
                filename={part.filename}
              />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default ChatMessage;
