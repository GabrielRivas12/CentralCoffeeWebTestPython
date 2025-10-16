// Constantes y configuraciones
const GREETINGS = [
    'hola', 'holi', 'holis', 'holaa', 'holaaa', 'hey', 'heyy', 'hello', 'hi', 
    'buenas', 'buenos días', 'buenas tardes', 'buenas noches', 'qué tal', 
    'qué onda', 'qué hay', 'saludos', 'qué más', 'cómo estás', 'como estas',
    'qué hubo', 'quihubo', 'buen día', 'buendia', 'good morning', 'good afternoon'
];

const THANKS_AND_GOODBYE = [
    'gracias', 'muchas gracias', 'mil gracias', 'gracias por todo', 'te agradezco',
    'agradecido', 'agradecida', 'thanks', 'thank you', 'ty', 'merci', 'danke',
    'adiós', 'adios', 'chao', 'bye', 'bye bye', 'goodbye', 'hasta luego', 
    'hasta pronto', 'nos vemos', 'que tengas buen día', 'que te vaya bien',
    'cuídate', 'cuidase', 'hasta la próxima', 'fue un gusto', 'fue un placer',
    'perfecto', 'está bien', 'de acuerdo', 'ok', 'okey', 'listo', 'genial',
    'excelente', 'estupendo', 'maravilloso', 'fantástico', 'increíble'
];

const FORBIDDEN_TOPICS = [
    'política', 'politica', 'gobierno', 'presidente', 'elecciones', 'votar', 'voto',
    'partido', 'democracia', 'izquierda', 'derecha', 'liberal', 'conservador',
    'deportes', 'deporte', 'fútbol', 'futbol', 'baloncesto', 'béisbol', 'beisbol',
    'tenis', 'natación', 'ciclismo', 'atletismo', 'competencia', 'competir',
    'programación', 'programacion', 'código', 'codigo', 'javascript', 'python',
    'java', 'html', 'css', 'react', 'node', 'aplicación', 'app', 'software',
    'hardware', 'computadora', 'ordenador', 'tecnología', 'tecnologia',
    'videojuegos', 'video juego', 'playstation', 'xbox', 'nintendo',
    'música', 'musica', 'canción', 'cancion', 'artista', 'banda',
    'cine', 'película', 'pelicula', 'actor', 'actriz', 'netflix',
    'guerra', 'conflicto', 'violencia', 'armas', 'pistola', 'rifle',
    'religión', 'religion', 'dios', 'iglesia', 'fe', 'creencia',
    'drogas', 'alcohol', 'tabaco', 'marihuana', 'cigarro', 'licor',
    'moda', 'ropa', 'viajes', 'turismo', 'automóvil', 'carro', 'coche',
    'finanzas', 'dinero', 'inversión', 'bolsa', 'economía', 'sexo', 'copular', 'coito', 'coger'
];

const COFFEE_ADVISOR_URL = 'https://magicloops.dev/api/loop/f55cde9f-e4e9-4718-bc35-a9b086fdd1ff/run';
const COFFEE_STATS_URL = 'https://magicloops.dev/api/loop/e4c3cd48-b631-4127-8279-47a4f924290e/run';

// Funciones de utilidad
const cleanText = (text) => {
    if (!text || typeof text !== 'string') return '';
    
    return text
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^\w\s]/gi, ' ')
        .trim();
};

const isGreeting = (message) => {
    const cleanMessage = cleanText(message);
    const words = cleanMessage.split(/\s+/);
    
    return GREETINGS.some(greeting => {
        const cleanGreeting = cleanText(greeting);
        return words.some(word => word === cleanGreeting);
    });
};

const isThanksOrGoodbye = (message) => {
    const cleanMessage = cleanText(message);
    const words = cleanMessage.split(/\s+/);
    
    return THANKS_AND_GOODBYE.some(phrase => {
        const cleanPhrase = cleanText(phrase);
        
        if (cleanPhrase.includes(' ')) {
            return cleanMessage.includes(cleanPhrase);
        }
        
        return words.some(word => word === cleanPhrase);
    });
};

const containsForbiddenTopic = (message) => {
    const cleanMessage = cleanText(message);
    const words = cleanMessage.split(/\s+/);
    
    return FORBIDDEN_TOPICS.some(topic => {
        const cleanTopic = cleanText(topic);
        return words.some(word => word === cleanTopic);
    });
};

// Clase principal del chat
class CoffeeAssistant {
    constructor() {
        this.messages = [];
        this.isTyping = false;
        this.typingInterval = null;
        this.currentDot = 0;
        
        // Elementos del DOM
        this.chatContent = document.getElementById('chatContent');
        this.chatContentWrapper = document.getElementById('chatContentWrapper');
        this.centeredInputContainer = document.getElementById('centeredInputContainer');
        this.normalInputContainer = document.getElementById('normalInputContainer');
        
        // Inputs centrados
        this.centeredMessageInput = document.getElementById('centeredMessageInput');
        this.sendButtonCentered = document.getElementById('sendButtonCentered');
        
        // Inputs normales
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.clearButton = document.getElementById('clearButton');
        
        this.initializeEventListeners();
        this.setupAutoResize();
    }
    
    initializeEventListeners() {
        // Eventos para el input centrado
        this.sendButtonCentered.addEventListener('click', () => this.sendMessageFromCentered());
        this.centeredMessageInput.addEventListener('input', () => {
            this.sendButtonCentered.disabled = !this.centeredMessageInput.value.trim();
        });
        this.centeredMessageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessageFromCentered();
            }
        });
        
        // Eventos para el input normal
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.clearButton.addEventListener('click', () => this.clearChat());
        this.messageInput.addEventListener('input', () => {
            this.sendButton.disabled = !this.messageInput.value.trim();
        });
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }
    
    setupAutoResize() {
        // Auto-resize para ambos inputs
        [this.centeredMessageInput, this.messageInput].forEach(input => {
            input.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = Math.min(this.scrollHeight, 120) + 'px';
            });
        });
    }
    
    // Enviar mensaje desde el input centrado
    sendMessageFromCentered() {
        const message = this.centeredMessageInput.value.trim();
        if (!message) return;
        
        // Ocultar input centrado y mostrar el normal
        this.switchToNormalInput();
        
        // Enviar el mensaje
        this.sendMessageInternal(message);
        
        // Limpiar el input centrado
        this.centeredMessageInput.value = '';
        this.sendButtonCentered.disabled = true;
        this.centeredMessageInput.style.height = 'auto';
    }
    
    // Cambiar a input normal
    switchToNormalInput() {
        this.centeredInputContainer.classList.add('hidden');
        this.normalInputContainer.style.display = 'flex';
        this.chatContent.classList.add('with-messages');
        
        // Copiar el valor del input centrado al normal
        this.messageInput.value = this.centeredMessageInput.value;
        this.sendButton.disabled = !this.messageInput.value.trim();
    }
    
    handleAutomaticResponse(message) {
        if (containsForbiddenTopic(message)) {
            return "Lo siento, sólo puedo ofrecer información sobre café de Nicaragua, su producción, trazabilidad, tueste y comercio.";
        }

        if (isGreeting(message)) {
            return "¡Hola! 👋 Soy CentralCoffeeIA, tu asistente especializado en café de Nicaragua. ¿En qué puedo ayudarte hoy? Puedo brindarte información sobre:\n\n• Producción de café\n• Trazabilidad\n• Tipos de tueste\n• Comercio y exportación\n• Estadísticas del sector\n\n¿Qué te gustaría saber?";
        }

        if (isThanksOrGoodbye(message)) {
            return "¡De nada! 😊 Ha sido un placer ayudarte. Si necesitas más información sobre el café de Nicaragua, no dudes en preguntarme. ¡Que tengas un excelente día! ☕";
        }

        return null;
    }
    
    async sendMessageToAPI(message) {
        let url, body;
        
        if (message.startsWith('/stats')) {
            const parts = message.replace('/stats', '').trim().split(/\s+/);
            url = COFFEE_STATS_URL;
            body = { dataType: parts[0] || '', region: parts[1] || '' };
        } else {
            url = COFFEE_ADVISOR_URL;
            body = { question: message, language: 'español' };
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body),
            });

            const data = await response.json();
            return data.response || JSON.stringify(data);
        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            return 'Error al obtener datos. Por favor, inténtalo de nuevo.';
        }
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;
        this.sendMessageInternal(message);
    }
    
    async sendMessageInternal(message) {
        // Agregar mensaje del usuario
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        this.sendButton.disabled = true;
        this.messageInput.style.height = 'auto';
        
        this.startTypingIndicator();

        // Verificar respuestas automáticas
        const automaticResponse = this.handleAutomaticResponse(message);
        
        if (automaticResponse) {
            setTimeout(() => {
                this.stopTypingIndicator();
                this.addMessage(automaticResponse, 'ai');
            }, 1000);
            return;
        }

        // Si no es respuesta automática, consultar la API
        try {
            const aiResponse = await this.sendMessageToAPI(message);
            
            setTimeout(() => {
                this.stopTypingIndicator();
                this.addMessage(aiResponse, 'ai');
            }, 1000);

        } catch (error) {
            console.error('Error al procesar mensaje:', error);
            setTimeout(() => {
                this.stopTypingIndicator();
                this.addMessage('Error al procesar tu mensaje. Por favor, inténtalo de nuevo.', 'ai');
            }, 1000);
        }
    }
    
    addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;
        messageElement.textContent = text;
        
        this.chatContent.appendChild(messageElement);
        this.scrollToBottom();
        
        if (sender === 'user') {
            this.messages.push({ text, sender });
        }
    }
    
    startTypingIndicator() {
        this.isTyping = true;
        
        const typingElement = document.createElement('div');
        typingElement.className = 'message ai-message typing-indicator';
        typingElement.id = 'typingIndicator';
        
        const dotsContainer = document.createElement('div');
        dotsContainer.className = 'typing-dots';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-dot';
            dot.id = `typingDot${i + 1}`;
            dotsContainer.appendChild(dot);
        }
        
        typingElement.appendChild(dotsContainer);
        this.chatContent.appendChild(typingElement);
        this.scrollToBottom();
        
        this.typingInterval = setInterval(() => {
            const dots = document.querySelectorAll('.typing-dot');
            dots.forEach(dot => dot.style.opacity = '0.3');
            
            if (dots[this.currentDot]) {
                dots[this.currentDot].style.opacity = '1';
            }
            
            this.currentDot = (this.currentDot + 1) % 3;
        }, 300);
    }
    
    stopTypingIndicator() {
        this.isTyping = false;
        this.currentDot = 0;
        
        if (this.typingInterval) {
            clearInterval(this.typingInterval);
            this.typingInterval = null;
        }
        
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    clearChat() {
        if (confirm('¿Estás seguro de que quieres borrar toda la conversación?')) {
            this.chatContent.innerHTML = '';
            this.messages = [];
            this.stopTypingIndicator();
            
            // Volver al input centrado
            this.centeredInputContainer.classList.remove('hidden');
            this.normalInputContainer.style.display = 'none';
            this.chatContent.classList.remove('with-messages');
        }
    }
    
    scrollToBottom() {
        setTimeout(() => {
            this.chatContent.scrollTop = this.chatContent.scrollHeight;
        }, 100);
    }
}

// Inicializar la aplicación cuando se carga la página
document.addEventListener('DOMContentLoaded', () => {
    new CoffeeAssistant();
});