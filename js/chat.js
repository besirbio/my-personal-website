document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function displayMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function getGeminiResponse(prompt) {
        // Send the user's prompt to your local backend server
        const response = await fetch('http://localhost:3000/ask-gemini', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: prompt }),
        });
        const data = await response.json();
        return data.answer;
    }

    async function handleUserInput() {
        const userText = userInput.value.trim();
        if (userText === '') return;

        displayMessage('user', userText);
        userInput.value = '';

        // Display a loading message while waiting for the AI
        displayMessage('bot', 'Thinking...');

        try {
            const botResponse = await getGeminiResponse(userText);
            // Replace the loading message with the actual response
            const lastMessage = chatBox.lastChild;
            if (lastMessage && lastMessage.textContent === 'Thinking...') {
                chatBox.removeChild(lastMessage);
            }
            displayMessage('bot', botResponse);
        } catch (error) {
            console.error('Error:', error);
            const lastMessage = chatBox.lastChild;
            if (lastMessage && lastMessage.textContent === 'Thinking...') {
                chatBox.removeChild(lastMessage);
            }
            displayMessage('bot', "Sorry, I'm unable to connect right now. Please try again later.");
        }
    }

    sendBtn.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    displayMessage('bot', 'Hello! I am a Gemini-powered Biology Tutor. How can I help you today?');
});