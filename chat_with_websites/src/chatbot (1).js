document.addEventListener("DOMContentLoaded", function () {
    // Create and append the CSS for the chatbot
    const styles = `
    #chatbot-toggle-button {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 24px;
        cursor: pointer;
        z-index: 2147483647; 
    }

    #chatbot-container {
        position: fixed;
        bottom: 70px;
        right: 10px;
        width: 300px;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        background-color: white;
        display: flex;
        flex-direction: column;
        font-family: Arial, sans-serif;
        display: none; /* Hidden by default */
       z-index: 2147483647; 
    }
    #chatbot-header {
        background-color: #007bff;
        color: white;
        padding: 10px;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    #chatbot-body {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
        max-height: 300px;
    }
    #chatbot-input-container {
        display: flex;
        border-top: 1px solid #ccc;
    }
    #chatbot-input {
        flex: 1;
        padding: 10px;
        border: none;
        border-bottom-left-radius: 10px;
    }
    #chatbot-send-button {
        padding: 10px;
        background-color: #007bff;
        color: white;
        border: none;
        cursor: pointer;
        border-bottom-right-radius: 10px;
    }
    #chatbot-send-button:hover {
        background-color: #0056b3;
    }
    .chatbot-message {
        margin: 5px 0;
        padding: 10px;
        border-radius: 10px;
        max-width: 80%;
    }
    .chatbot-message-user {
        background-color: #f1f1f1;
        color: black;
        align-self: flex-start;
    }
    .chatbot-message-assistant {
        background-color: #007bff;
        color: white;
        margin-left:20px;
        align-self: flex-end;
    }
    `;

    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = styles;
    document.head.appendChild(styleSheet);

    // Create and append the toggle button
    const toggleButton = document.createElement('button');
    toggleButton.id = 'chatbot-toggle-button';
    toggleButton.innerHTML = '🗨'; // Chat icon
    document.body.appendChild(toggleButton);

    // Create and append the HTML structure for the chatbot
    const chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'chatbot-container';
    chatbotContainer.innerHTML = `
        <div id="chatbot-header">Chatbot</div>
        <div id="chatbot-body"></div>
        <div id="chatbot-input-container">
            <input type="text" id="chatbot-input" placeholder="Type a message...">
            <button id="chatbot-send-button">Send</button>
        </div>
    `;
    document.body.appendChild(chatbotContainer);

    const chatbotBody = document.getElementById("chatbot-body");
    const chatbotInput = document.getElementById("chatbot-input");
    const chatbotSendButton = document.getElementById("chatbot-send-button");

    let threadId = null;

    // Toggle chatbot visibility
    toggleButton.addEventListener('click', () => {
        if (chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '') {
            chatbotContainer.style.display = 'flex';
            toggleButton.innerHTML = 'x'; // Cross icon
            toggleButton.classList.add('white-icon'); // Ensure the icon is white when displayed
        } else {
            chatbotContainer.style.display = 'none';
            toggleButton.innerHTML = '🗨'; // Chat icon
            toggleButton.classList.remove('white-icon');
        }
    });

    // Initialize the chatbot
    async function initializeChatbot() {
        try {
            const response = await fetch('https://assistant-api-qyuerd4l2a-uc.a.run.app/create_thread');
            const data = await response.json();
            threadId = data.thread_id;
        } catch (error) {
            console.error('Error creating thread:', error);
        }
    }

    // Send a message and display "thinking..." indicator
    async function sendMessage(message) {
        displayMessage(message, 'user'); // Display the user's message
        displayThinking(); // Display the "thinking..." message
        try {
            const response = await fetch('https://assistant-api-qyuerd4l2a-uc.a.run.app/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: message,
                    thread_id: threadId
                })
            });
            const data = await response.json();
            const messageId = data.message_id;
            delayedRetrieveMessageResponse(threadId, messageId, 2000); // Adjust delay as needed
        } catch (error) {
            console.error('Error sending message:', error);
            removeThinking(); // Remove the "thinking..." message in case of error
        }
    }

    // Display a temporary "thinking..." message
    function displayThinking() {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message', 'chatbot-message-assistant');
        messageElement.textContent = "Thinking...";
        messageElement.id = 'thinking-message'; // Add an ID for later removal or update
        chatbotBody.appendChild(messageElement);
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }

    // Remove or update the "thinking..." message
    function removeThinking() {
        const thinkingMessage = document.getElementById('thinking-message');
        if (thinkingMessage) {
            chatbotBody.removeChild(thinkingMessage);
        }
    }

    // Retrieve message response and update the chat interface
    async function retrieveMessageResponse(threadId, messageId) {
        let url = `https://assistant-api-qyuerd4l2a-uc.a.run.app/retrieve_message_responses/${encodeURIComponent(threadId)}/${encodeURIComponent(messageId)}`;
        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                const errorDetails = await response.json();
                throw new Error(`HTTP error ${response.status}: ${JSON.stringify(errorDetails)}`);
            }

            const data = await response.json();
            removeThinking(); // Remove the "thinking..." message
            displayMessage(data.content, 'assistant'); // Display the actual response
        } catch (error) {
            console.error('Error retrieving message response:', error);
            removeThinking(); // Ensure removal of the "thinking..." message in case of error
        }
    }

    // Function to initialize and call retrieveMessageResponse with a delay
    function delayedRetrieveMessageResponse(threadId, messageId, delay) {
        setTimeout(() => {
            retrieveMessageResponse(threadId, messageId);
        }, delay); // Delay in milliseconds
    }

    // Display a message
    function displayMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message', `chatbot-message-${sender}`);
        messageElement.textContent = message;
        chatbotBody.appendChild(messageElement);
        chatbotBody.scrollTop = chatbotBody.scrollHeight;
    }

    // Handle send button click
    chatbotSendButton.addEventListener('click', () => {
        const message = chatbotInput.value.trim();
        if (message) {
            sendMessage(message);
            chatbotInput.value = '';
        }
    });

    // Handle enter key press in input
    chatbotInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            chatbotSendButton.click();
        }
    });

    // Initialize the chatbot on page load
    initializeChatbot();
});
