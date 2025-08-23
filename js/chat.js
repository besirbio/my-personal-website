document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // A simple, rule-based Q&A system for biology
    const biologyAnswers = {
        'cell': 'The cell is the basic structural, functional, and biological unit of all known organisms. There are two main types: prokaryotic and eukaryotic.',
        'dna': 'DNA, or deoxyribonucleic acid, is the hereditary material in humans and almost all other organisms. It contains the instructions for building an organism.',
        'photosynthesis': 'Photosynthesis is the process used by plants, algae and certain bacteria to convert light energy into chemical energy, which is later used to fuel the organisms\' activities.',
        'mitosis': 'Mitosis is a process of nuclear division in eukaryotic cells that occurs when a parent cell divides to produce two identical daughter cells.',
        'evolution': 'Evolution is the change in the heritable characteristics of biological populations over successive generations.',
        'bacteria': 'Bacteria are single-celled organisms that are prokaryotic, meaning they do not have a nucleus.',
        'virus': 'A virus is a microscopic infectious agent that replicates only inside the living cells of other organisms.',
        'protein': 'Proteins are large biomolecules, or macromolecules, consisting of one or more long chains of amino acid residues. They perform a vast array of functions within organisms.',
        'ecosystem': 'An ecosystem is a community of living organisms in conjunction with the nonliving components of their environment, interacting as a system.',
        'heredity': 'Heredity is the passing of traits from parents to their offspring, either through asexual or sexual reproduction.',
        'what is your name': 'I am a simple Biology Q&A bot designed to help you with your studies!',
        'hello': 'Hello! How can I help you with biology today?',
        'hi': 'Hi there! Feel free to ask me anything about biology.',
        'how are you': 'I am an AI, so I don\'t have feelings, but I\'m ready to help you learn!',
    };

    function displayMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        messageElement.innerHTML = `<p>${message}</p>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function getBotResponse(input) {
        const lowerInput = input.toLowerCase();
        for (const keyword in biologyAnswers) {
            if (lowerInput.includes(keyword)) {
                return biologyAnswers[keyword];
            }
        }
        return "I'm sorry, I can only answer questions about the topics I've been taught. Please ask me about a different biology term.";
    }

    function handleUserInput() {
        const userText = userInput.value.trim();
        if (userText === '') return;

        displayMessage('user', userText);
        userInput.value = '';

        setTimeout(() => {
            const botResponse = getBotResponse(userText);
            displayMessage('bot', botResponse);
        }, 500); // Wait for half a second before responding
    }

    sendBtn.addEventListener('click', handleUserInput);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });

    // Display a welcome message when the page loads
    displayMessage('bot', 'Hello! I am a simple Biology Q&A Bot. How can I help you today?');
});