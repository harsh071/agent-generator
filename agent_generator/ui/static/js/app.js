// DOM Elements
const chatList = document.getElementById('chat-list');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const newChatBtn = document.getElementById('new-chat-btn');

// State
let currentChatId = null;
let chats = [];

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    fetchChats();
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    newChatBtn.addEventListener('click', createNewChat);
});

// Fetch all chats
async function fetchChats() {
    try {
        const response = await fetch('/api/chats');
        chats = await response.json();
        renderChatList();
        
        // Select the first chat if available
        if (chats.length > 0 && !currentChatId) {
            selectChat(chats[0].id);
        }
    } catch (error) {
        console.error('Error fetching chats:', error);
    }
}

// Render the chat list
function renderChatList() {
    chatList.innerHTML = '';
    
    chats.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
        chatItem.textContent = chat.name;
        chatItem.addEventListener('click', () => selectChat(chat.id));
        
        // Add delete button
        const deleteBtn = document.createElement('span');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '&times;';
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            deleteChat(chat.id);
        });
        
        chatItem.appendChild(deleteBtn);
        chatList.appendChild(chatItem);
    });
}

// Select a chat
async function selectChat(chatId) {
    currentChatId = chatId;
    renderChatList();
    
    try {
        const response = await fetch(`/api/chats/${chatId}`);
        const chat = await response.json();
        renderMessages(chat.messages);
    } catch (error) {
        console.error('Error fetching chat:', error);
    }
}

// Render messages
function renderMessages(messages) {
    chatMessages.innerHTML = '';
    
    messages.forEach(message => {
        const messageEl = document.createElement('div');
        messageEl.className = `message ${message.role}`;
        messageEl.textContent = message.content;
        chatMessages.appendChild(messageEl);
    });
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send a message
async function sendMessage() {
    const content = chatInput.value.trim();
    if (!content) return;
    
    // Clear input
    chatInput.value = '';
    
    // Create a new chat if none is selected
    if (!currentChatId) {
        await createNewChat();
    }
    
    // Add user message to UI immediately
    const userMessage = {
        id: Date.now().toString(),
        role: 'user',
        content: content,
        timestamp: new Date().toISOString()
    };
    
    addMessageToUI(userMessage);
    
    try {
        // Send message to server
        const response = await fetch(`/api/chats/${currentChatId}/messages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });
        
        const assistantMessage = await response.json();
        addMessageToUI(assistantMessage);
    } catch (error) {
        console.error('Error sending message:', error);
    }
}

// Add a message to the UI
function addMessageToUI(message) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${message.role}`;
    messageEl.textContent = message.content;
    chatMessages.appendChild(messageEl);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Create a new chat
async function createNewChat() {
    try {
        const response = await fetch('/api/chats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: 'New Chat' })
        });
        
        const newChat = await response.json();
        chats.unshift(newChat);
        renderChatList();
        selectChat(newChat.id);
    } catch (error) {
        console.error('Error creating new chat:', error);
    }
}

// Delete a chat
async function deleteChat(chatId) {
    if (!confirm('Are you sure you want to delete this chat?')) return;
    
    try {
        await fetch(`/api/chats/${chatId}`, {
            method: 'DELETE'
        });
        
        chats = chats.filter(chat => chat.id !== chatId);
        
        if (currentChatId === chatId) {
            currentChatId = chats.length > 0 ? chats[0].id : null;
        }
        
        renderChatList();
        
        if (currentChatId) {
            selectChat(currentChatId);
        } else {
            chatMessages.innerHTML = '';
        }
    } catch (error) {
        console.error('Error deleting chat:', error);
    }
}