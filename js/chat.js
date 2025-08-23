document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // A simple, rule-based Q&A system for biology
const biologyAnswers = {
    'cell': 'The cell is the basic structural, functional, and biological unit of all known organisms. It’s like the fundamental building block of life. There are two main types: prokaryotic (without a nucleus, like bacteria) and eukaryotic (with a nucleus, like plant and animal cells).',
    'prokaryotic cell': 'A prokaryotic cell is a single-celled organism that lacks a membrane-bound nucleus, mitochondria, or any other membrane-bound organelle. Bacteria and archaea are examples of prokaryotic cells.',
    'eukaryotic cell': 'A eukaryotic cell is a type of cell that has a true nucleus and other membrane-bound organelles. These cells are found in plants, animals, fungi, and protists.',
    'organelle': 'An organelle is a specialized subunit within a cell that has a specific function. Think of them as the "mini-organs" of the cell. Key organelles include the nucleus, mitochondria, and endoplasmic reticulum.',
    'nucleus': 'The nucleus is the control center of the eukaryotic cell. It contains the cell\'s genetic material, DNA, organized into chromosomes. Its main function is to maintain the integrity of the genes and control the activities of the cell.',
    'mitochondria': 'Mitochondria are often called the "powerhouses of the cell." They generate most of the chemical energy needed to power the cell\'s biochemical reactions, producing ATP from glucose and oxygen through a process called cellular respiration.',
    'cellular respiration': 'Cellular respiration is the metabolic process in which organisms convert energy from nutrients into ATP (adenosine triphosphate) and then release waste products. It occurs in three main stages: glycolysis, the Krebs cycle, and the electron transport chain.',
    'chloroplast': 'Chloroplasts are the sites of photosynthesis in plant and algae cells. They contain a green pigment called chlorophyll that absorbs sunlight, giving plants their green color.',
    'dna': 'DNA, or deoxyribonucleic acid, is the hereditary material in humans and almost all other organisms. It contains the instructions for building an organism. The structure of DNA is a double helix, resembling a twisted ladder.',
    'gene': 'A gene is a basic unit of heredity. It is a segment of DNA that codes for a specific protein, which determines a trait. Genes are passed from parents to offspring.',
    'chromosome': 'A chromosome is a thread-like structure of nucleic acids and protein found in the nucleus of most living cells. It carries the genetic information in the form of genes.',
    'genetics': 'Genetics is the scientific study of genes and heredity—of how certain qualities or traits are passed from parents to offspring as a result of changes in DNA sequence.',
    'photosynthesis': 'Photosynthesis is the process used by plants, algae, and some bacteria to convert light energy into chemical energy, which is later used to fuel the organisms\' activities. The main reactants are carbon dioxide and water, and the products are glucose and oxygen.',
    'mitosis': 'Mitosis is a process of nuclear division in eukaryotic cells that occurs when a parent cell divides to produce two identical daughter cells. It is essential for growth and repair in multicellular organisms.',
    'meiosis': 'Meiosis is a specialized type of cell division that reduces the chromosome number by half. This process is essential for sexual reproduction and results in the formation of gametes (sperm and egg cells).',
    'evolution': 'Evolution is the change in the heritable characteristics of biological populations over successive generations. The primary mechanism of evolution is natural selection, as first proposed by Charles Darwin.',
    'natural selection': 'Natural selection is the process by which organisms that are better adapted to their environment tend to survive and produce more offspring. This leads to the gradual change in a population over time.',
    'species': 'A species is a group of living organisms consisting of similar individuals capable of exchanging genes or interbreeding. They are a fundamental category of biological classification.',
    'taxonomy': 'Taxonomy is the science of naming, describing, and classifying organisms. The taxonomic hierarchy includes domains, kingdoms, phyla, classes, orders, families, genera, and species.',
    'bacteria': 'Bacteria are single-celled organisms that are prokaryotic, meaning they do not have a nucleus. While some can cause disease, many are beneficial, playing a crucial role in decomposition and nutrient cycles.',
    'virus': 'A virus is a microscopic infectious agent that replicates only inside the living cells of other organisms. They are not considered living organisms because they cannot reproduce on their own.',
    'protein': 'Proteins are large biomolecules, or macromolecules, consisting of long chains of amino acid residues. They perform a vast array of functions within organisms, including catalyzing metabolic reactions and DNA replication.',
    'amino acid': 'An amino acid is the basic building block of a protein. There are 20 common amino acids that combine in various sequences to form the thousands of different proteins found in the body.',
    'ecosystem': 'An ecosystem is a community of living organisms in conjunction with the nonliving components of their environment, interacting as a system. Examples include a forest, a coral reef, or even a small pond.',
    'heredity': 'Heredity is the passing of traits from parents to their offspring. It is the reason why offspring resemble their parents, and it is the foundation of genetics.',
    'population': 'A population is a group of organisms of one species that interbreed and live in the same place at the same time.',
    'community': 'A community is an assemblage of different populations of organisms living in the same area and interacting with each other.',
    'ecology': 'Ecology is the branch of biology that studies the relationships among organisms and their physical environment.',
    'biome': 'A biome is a large, naturally occurring community of flora and fauna occupying a major habitat, such as a forest or tundra.',
    'biomass': 'Biomass is the total mass of organisms in a given area or ecosystem.',
    'food chain': 'A food chain is a linear network of links in a food web starting from producer organisms (like plants) and ending at apex predator species or decomposers.',
    'homeostasis': 'Homeostasis is the ability of an organism or a cell to maintain a stable internal environment despite external changes.',
    'photosynthesis equation': 'The chemical equation for photosynthesis is 6CO₂ + 6H₂O + Light Energy → C₆H₁₂O₆ + 6O₂. This means carbon dioxide and water, with light energy, produce glucose (a sugar) and oxygen.',
    'cellular respiration equation': 'The chemical equation for cellular respiration is C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP. This shows how glucose and oxygen produce carbon dioxide, water, and energy.',
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