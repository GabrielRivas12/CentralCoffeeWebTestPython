const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const labelContainer = document.getElementById('label-container');
const messagesDiv = document.getElementById('messages');

const URL = "/static/model/";
let model;

async function init() {
    const modelURL = URL + "model.json";
    const metadataURL = URL + "metadata.json";
    
    labelContainer.innerHTML = "<p>Cargando modelo...</p>";
    try {
        model = await tmImage.load(modelURL, metadataURL);
        labelContainer.innerHTML = "<p>Modelo cargado. Por favor, sube una imagen.</p>";
    } catch (error) {
        console.error("Error al cargar el modelo:", error);
        labelContainer.innerHTML = "<p>Error al cargar el modelo. Revisa la consola.</p>";
    }
}

async function predict(image) {
    if (!model) {
        labelContainer.innerHTML = "<p>El modelo no está cargado todavía.</p>";
        return;
    }
    
    labelContainer.innerHTML = "<p>Analizando...</p>";
    const prediction = await model.predict(image);
    
    const winner = prediction.reduce((prev, current) => (prev.probability > current.probability) ? prev : current);

    labelContainer.innerHTML = "";
    const winnerDiv = document.createElement('div');
    winnerDiv.className = 'winner-prediction';
    
    const winnerName = document.createElement('h3');
    winnerName.textContent = winner.className;
    
    const winnerProb = document.createElement('p');
    winnerProb.textContent = `Confianza: ${(winner.probability * 100).toFixed(2)}%`;
    
    winnerDiv.appendChild(winnerName);
    winnerDiv.appendChild(winnerProb);
    labelContainer.appendChild(winnerDiv);

    // Lógica para actualizar el chat sin acumular mensajes
    const lastMessage = messagesDiv.lastElementChild;
    const newBotText = `He detectado que el tipo de café es: ${winner.className}. ¿Quieres saber más sobre este tipo?`;

    // Si el último mensaje es un resultado de predicción, actualízalo
    if (lastMessage && lastMessage.hasAttribute('data-prediction-result')) {
        lastMessage.textContent = newBotText;
    } else {
        // Si no, limpia el mensaje de bienvenida (si existe) y añade uno nuevo
        if (messagesDiv.children.length > 0 && messagesDiv.children[0].textContent.startsWith('Hola!')) {
            messagesDiv.innerHTML = '';
        }
        const botMsg = document.createElement('div');
        botMsg.classList.add('bot-message');
        botMsg.setAttribute('data-prediction-result', 'true'); // Marcar como mensaje de predicción
        botMsg.textContent = newBotText;
        messagesDiv.appendChild(botMsg);
    }

    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

imageInput.addEventListener('change', function () {
    const file = this.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
        preview.src = e.target.result;
        preview.style.display = 'block';
        predict(preview); 
    }
    reader.readAsDataURL(file);
});

init();

function sendMessage() {
    const input = document.getElementById('userInput');
    const text = input.value.trim();
    if (!text) return;

    const userMsg = document.createElement('div');
    userMsg.classList.add('user-message');
    userMsg.textContent = text;
    messagesDiv.appendChild(userMsg);

    input.value = '';
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    setTimeout(() => {
        const botMsg = document.createElement('div');
        botMsg.classList.add('bot-message');
        botMsg.textContent = `Aquí iría la respuesta del bot a: "${text}"`;
        messagesDiv.appendChild(botMsg);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }, 500);
}

document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});
