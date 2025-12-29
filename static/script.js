console.log('Script.js loaded successfully!');

const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

console.log('DOM Elements loaded:', {
    chatMessages: chatMessages ? 'Found' : 'Not Found',
    chatInput: chatInput ? 'Found' : 'Not Found',
    sendButton: sendButton ? 'Found' : 'Not Found',
    typingIndicator: typingIndicator ? 'Found' : 'Not Found'
});

// Auto-resize textarea
chatInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 150) + 'px';
});

// Handle Enter key (Shift+Enter for new line)
chatInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        console.log('✓ Enter key pressed - sending message');
        sendMessage();
    } else if (e.key === 'Enter' && e.shiftKey) {
        console.log('✓ Shift+Enter pressed - new line');
    }
});

// Send button click
sendButton.addEventListener('click', function() {
    console.log('✓ Send button clicked');
    sendMessage();
});

function sendMessage() {
    const message = chatInput.value.trim();
    
    console.log('=== sendMessage() called ===');
    console.log('Message content:', message);
    console.log('Message length:', message.length);
    
    if (!message) {
        console.log('⚠ Empty message - not sending');
        return;
    }
    
    console.log('✓ Valid message - proceeding to send');
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    chatInput.value = '';
    chatInput.style.height = 'auto';
    console.log('✓ Input cleared');
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to backend
    console.log('→ Sending POST request to /ask endpoint...');
    console.log('🤔 Thinking....');
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: message })
    })
    .then(response => {
        console.log('← Response received from server');
        console.log('✅ Done thinking!');
        console.log('Response status:', response.status);
        console.log('Response ok:', response.ok);
        return response.json();
    })
    .then(data => {
        console.log('← Data parsed:', data);
        hideTypingIndicator();
        
        if (data.success) {
            console.log('✓ Success! Adding AI response');
            addMessage(data.response, 'ai');
        } else {
            console.log('⚠ Server returned error:', data.error);
            addMessage('Sorry, there was an error processing your question. Please try again.', 'ai');
        }
    })
    .catch(error => {
        console.error('✗ Fetch error occurred:', error);
        hideTypingIndicator();
        addMessage('Sorry, there was a connection error. Please make sure the server is running.', 'ai');
    });
}

function addMessage(text, type) {
    console.log(`→ Adding ${type} message:`, text.substring(0, 50) + '...');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = type === 'ai' ? '🤖' : '👤';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    // Insert before typing indicator
    chatMessages.insertBefore(messageDiv, typingIndicator);
    console.log('✓ Message div inserted');
    
    // Add timestamp
    const timestamp = document.createElement('div');
    timestamp.className = 'timestamp';
    timestamp.textContent = getTimestamp();
    chatMessages.insertBefore(timestamp, typingIndicator);
    console.log('✓ Timestamp added');
    
    // Scroll to bottom
    scrollToBottom();
}

function showTypingIndicator() {
    console.log('→ Showing typing indicator');
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

function hideTypingIndicator() {
    console.log('→ Hiding typing indicator');
    typingIndicator.style.display = 'none';
}

function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getTimestamp() {
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

// Focus input on load
window.addEventListener('load', () => {
    console.log('✓ Window loaded - focusing input');
    chatInput.focus();
});

console.log('✓ All event listeners attached successfully!');