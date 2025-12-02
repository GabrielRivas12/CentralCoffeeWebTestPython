// Constantes y configuraciones actualizadas
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

const SUGGESTED_TOPICS = [
    "☕ Tipos de café y variedades",
    "🌱 Cultivo y producción cafetalera", 
    "🔥 Procesos de tueste y molido",
    "📊 Estadísticas del mercado del café",
    "🇳🇮 Café de Nicaragua específicamente",
    "🌍 Café de otras regiones del mundo",
    "💧 Métodos de preparación y brewing",
    "📈 Comercio y exportación de café",
    "🔬 Calidad y trazabilidad del café"
];

// TEMAS ESTRICTAMENTE PERMITIDOS
const ALLOWED_COFFEE_TOPICS = [
    // Café básico
    'café', 'cafe', 'cafetal', 'cafetalero', 'caficultor', 'caficultura', 'cafeto',
    
    // Producción y cultivo
    'producción', 'produccion', 'cultivo', 'cultivar', 'cosecha', 'recolección', 'recoleccion',
    'siembra', 'plantación', 'plantacion', 'finca', 'cafetalera',
    
    // Procesos
    'tueste', 'tostar', 'tostado', 'molido', 'moler', 'beneficio', 'secado', 'fermentación', 'fermentacion',
    'lavado', 'natural', 'proceso', 'trillado', 'clasificación', 'clasificacion',
    
    // Comercio y mercado
    'exportación', 'exportacion', 'comercio', 'mercado', 'precio', 'calidad', 'venta', 'compra',
    'exportador', 'importador', 'comercialización', 'comercializacion',
    
    // Variedades y tipos
    'arábica', 'robusta', 'variedad', 'caturra', 'catuaí', 'catuai', 'maragogipe', 'bourbon',
    'pacámara', 'pacamara', 'typica', 'java', 'geisha', 'mundo novo',
    
    // Características de calidad
    'sabor', 'aroma', 'acidez', 'cuerpo', 'dulzura', 'notas', 'catación', 'cata', 'barismo', 'barista',
    'fragancia', 'textura', 'aftertaste', 'cupping', 'puntaje', 'scaa',
    
    // Regiones de Nicaragua
    'nicaragua', 'nicaragüense', 'jinotega', 'matagalpa', 'nueva segovia', 'estelí', 'carazo',
    'madriz', 'boaco', 'río blanco', 'san fernando', 'yali', 'dipilto', 'jalapa',
    'somoto', 'ocotal', 'la dalia', 'esquipulas',
    
    // Regiones internacionales
    'colombia', 'colombiano', 'brasil', 'brasileño', 'brasileño', 'etiopía', 'etíope',
    'kenia', 'keniata', 'costa rica', 'costarricense', 'guatemala', 'guatemalteco',
    'honduras', 'hondureño', 'el salvador', 'salvadoreño', 'mexico', 'mexicano',
    'perú', 'peruano', 'venezuela', 'venezolano', 'asia', 'vietnam', 'indonesia',
    'india', 'sumatra', 'java', 'áfrica', 'centroamérica', 'suramérica',
    
    // Técnicas y procesos específicos
    'sombra', 'sol', 'altura', 'orgánico', 'organico', 'convencional', 'sostenible',
    'certificación', 'certificacion', 'fair trade', 'comercio justo', 'rainforest',
    'utz', 'orgánico', 'shade grown', 'bird friendly',
    
    // Estadísticas y datos
    'estadísticas', 'estadisticas', 'datos', 'cifras', 'volumen', 'toneladas', 'quintales',
    'hectáreas', 'hectareas', 'rendimiento', 'productividad', 'producción anual',
    'mercado mundial', 'exportaciones globales',
    
    // Equipos y herramientas (solo relacionados con café)
    'molino', 'cafetera', 'prensa francesa', 'chemex', 'v60', 'aeropress', 'moka', 'expresso', 'espresso',
    'filtro', 'tamper', 'molinillo', 'tostador', 'granja', 'beneficiador',
    
    // Términos específicos de la industria
    'trazabilidad', 'origen', 'región', 'region', 'microclima', 'altitud', 'suelo', 'clima',
    'perfil de tueste', 'punto de tueste', 'grado de tueste', 'especialidad', 'especialty',
    'terroir', 'micro-lote', 'single origin'
];

// TEMAS ESTRICTAMENTE PROHIBIDOS - TODO LO DEMÁS
const FORBIDDEN_TOPICS_PATTERNS = [
    {
        topic: 'política y gobierno',
        keywords: [
            'fsln', 'partido', 'liberal', 'sandino', 'ortega', 'chamorro', 'bolaños', 'aleman', 
            'elección', 'elecciones', 'voto', 'votar', 'gobierno', 'presidente', 'ministro', 
            'diputado', 'congreso', 'asamblea', 'alcalde', 'municipio', 'estado', 'nación',
            'política', 'politica', 'político', 'politico', 'ideología', 'oposición',
            'revolución', 'revolucion', 'sandinista', 'liberalista', 'conservador'
        ],
        phrases: [
            'partido político',
            'sistema político',
            'gobierno de nicaragua',
            'elecciones presidenciales',
            'votar por',
            'candidato a',
            'oposición política',
            'ideología política',
            'presidente de nicaragua',
            'ministro de'
        ],
        exactMatches: []
    },
    {
        topic: 'deportes',
        keywords: [
            'fútbol', 'futbol', 'balón', 'pelota', 'gol', 'equipo', 'jugador', 'partido', 
            'liga', 'campeonato', 'deportivo', 'deporte', 'beisbol', 'béisbol', 'boxeo',
            'natación', 'natacion', 'ciclismo', 'atletismo', 'competencia', 'competir',
            'estadio', 'arbitro', 'entrenador', 'deportista', 'olímpico', 'olimpico'
        ],
        phrases: [
            'jugar al fútbol',
            'partido de fútbol',
            'equipo de deportes',
            'liga nacional',
            'campeonato mundial',
            'juego de beisbol',
            'partido de baseball'
        ],
        exactMatches: []
    },
    {
        topic: 'tecnología y programación',
        keywords: [
            'programar', 'código', 'codigo', 'javascript', 'python', 'java', 'html', 'css', 
            'react', 'node', 'aplicación', 'aplicacion', 'app', 'software', 'desarrollador',
            'computadora', 'ordenador', 'celular', 'iphone', 'android', 'windows', 'mac',
            'internet', 'web', 'página', 'pagina', 'redes sociales', 'facebook', 'instagram',
            'whatsapp', 'tiktok', 'twitter'
        ],
        phrases: [
            'programación de software',
            'desarrollo web',
            'aplicación móvil',
            'lenguaje de programación',
            'escribir código',
            'red social',
            'teléfono celular'
        ],
        exactMatches: []
    },
    {
        topic: 'videojuegos',
        keywords: [
            'videojuego', 'video juego', 'jugar', 'consola', 'playstation', 'xbox', 'nintendo', 
            'gamer', 'nivel', 'personaje', 'minecraft', 'fortnite', 'call of duty', 'fifa',
            'juego online', 'multijugador', 'streaming', 'twitch', 'youtube gaming'
        ],
        phrases: [
            'jugar videojuegos',
            'juego de consola',
            'video juego de',
            'jugar en línea',
            'transmisión en vivo'
        ],
        exactMatches: []
    },
    {
        topic: 'música y entretenimiento',
        keywords: [
            'música', 'musica', 'canción', 'cancion', 'cantar', 'artista', 'banda', 'concierto', 
            'disco', 'álbum', 'album', 'ritmo', 'melodía', 'melodia', 'radio', 'spotify',
            'película', 'pelicula', 'cine', 'actor', 'actriz', 'netflix', 'disney',
            'series', 'televisión', 'television', 'youtube', 'tiktok'
        ],
        phrases: [
            'escuchar música',
            'canción de',
            'grupo musical',
            'concierto de',
            'ver película',
            'serie de televisión'
        ],
        exactMatches: []
    },
    {
        topic: 'comida y bebidas (excepto café)',
        keywords: [
            'comida', 'alimento', 'cocina', 'receta', 'cocinar', 'restaurante', 'comer',
            'bebida', 'refresco', 'jugo', 'agua', 'cerveza', 'vino', 'licor', 'ron', 'whisky',
            'té', 'te', 'infusión', 'leche', 'azúcar', 'azucar', 'pan', 'carne', 'pollo',
            'pescado', 'vegetales', 'frutas', 'arroz', 'frijoles', 'queso'
        ],
        phrases: [
            'preparar comida',
            'receta de cocina',
            'ir a restaurante',
            'bebida alcohólica',
            'té de hierbas'
        ],
        exactMatches: []
    },
    {
        topic: 'sexo y relaciones',
        keywords: [
            'sexo', 'sexual', 'cama', 'relación', 'relacion', 'cuerpo', 'beso', 'amor', 
            'novio', 'novia', 'pareja', 'matrimonio', 'casarse', 'divorcio', 'familia',
            'hijos', 'hijas', 'embarazo', 'bebé', 'bebe'
        ],
        phrases: [
            'relación sexual',
            'relación íntima',
            'relaciones sexuales',
            'acto sexual',
            'vida sexual',
            'vida amorosa'
        ],
        exactMatches: ['sexo', 'copular', 'coito']
    },
    {
        topic: 'religión y espiritualidad',
        keywords: [
            'dios', 'iglesia', 'religión', 'religion', 'fe', 'oración', 'oracion', 'rezar', 
            'santo', 'virgen', 'biblia', 'católico', 'catolico', 'cristiano', 'evangélico',
            'protestante', 'musulmán', 'musulman', 'judío', 'judio', 'ateo', 'agnóstico'
        ],
        phrases: [
            'creer en dios',
            'ir a la iglesia',
            'fe religiosa',
            'práctica religiosa',
            'rezar el rosario'
        ],
        exactMatches: []
    },
    {
        topic: 'violencia y armas',
        keywords: [
            'violencia', 'arma', 'pistola', 'rifle', 'disparar', 'matar', 'pelea', 'golpe', 
            'sangre', 'muerto', 'muerte', 'asesinato', 'crimen', 'delito', 'policía', 'policia',
            'ejército', 'ejercito', 'soldado', 'guerra', 'conflicto', 'paz'
        ],
        phrases: [
            'arma de fuego',
            'acto violento',
            'violencia física',
            'cometer un crimen'
        ],
        exactMatches: []
    },
    {
        topic: 'salud y medicina',
        keywords: [
            'salud', 'enfermedad', 'doctor', 'médico', 'medico', 'hospital', 'clínica', 
            'medicina', 'remedio', 'pastilla', 'vitamina', 'cuerpo', 'cerebro', 'corazón',
            'cáncer', 'cancer', 'covid', 'virus', 'bacteria', 'dieta', 'ejercicio', 'gimnasio'
        ],
        phrases: [
            'ir al doctor',
            'enfermedad grave',
            'tomar medicina',
            'hacer ejercicio'
        ],
        exactMatches: []
    },
    {
        topic: 'educación y estudio',
        keywords: [
            'escuela', 'colegio', 'universidad', 'estudio', 'estudiar', 'profesor', 'maestro',
            'alumno', 'estudiante', 'clase', 'curso', 'tarea', 'examen', 'graduación',
            'carrera', 'titulo', 'diploma', 'aprender', 'enseñar'
        ],
        phrases: [
            'ir a la escuela',
            'estudiar para examen',
            'clase universitaria'
        ],
        exactMatches: []
    },
    {
        topic: 'trabajo y negocios',
        keywords: [
            'trabajo', 'empleo', 'jefe', 'compañero', 'oficina', 'negocio', 'empresa',
            'empresario', 'dinero', 'salario', 'sueldo', 'contrato', 'entrevista',
            'economía', 'economia', 'finanzas', 'banco', 'cuenta', 'tarjeta', 'crédito'
        ],
        phrases: [
            'buscar trabajo',
            'trabajo en oficina',
            'ganar dinero',
            'negocio propio'
        ],
        exactMatches: []
    },
    {
        topic: 'viajes y turismo',
        keywords: [
            'viaje', 'viajar', 'turismo', 'turista', 'vacaciones', 'hotel', 'playa',
            'montaña', 'ciudad', 'pueblo', 'avión', 'avion', 'aeropuerto', 'bus',
            'carro', 'coche', 'moto', 'bicicleta'
        ],
        phrases: [
            'viajar a',
            'ir de vacaciones',
            'reservar hotel',
            'playa bonita'
        ],
        exactMatches: []
    },
    {
        topic: 'animales y mascotas',
        keywords: [
            'perro', 'gato', 'mascota', 'animal', 'veterinario', 'pez', 'pájaro', 'pajaro',
            'caballo', 'vaca', 'cerdo', 'gallina', 'zoo', 'zoológico'
        ],
        phrases: [
            'tener mascota',
            'cuidar animales',
            'ir al veterinario'
        ],
        exactMatches: []
    }
];

const COFFEE_ADVISOR_URL = 'https://magicloops.dev/api/loop/f55cde9f-e4e9-4718-bc35-a9b086fdd1ff/run';
const COFFEE_STATS_URL = 'https://magicloops.dev/api/loop/e4c3cd48-b631-4127-8279-47a4f924290e/run';

// URL de la IA que genera el informe (NUEVO ENDPOINT ESPECÍFICO)
const COFFEE_CLASSIFICATION_REPORT_URL = 'https://magicloops.dev/api/loop/f55cde9f-e4e9-4718-bc35-a9b086fdd1ff/run';

// Función para obtener el informe de la otra IA
async function getCoffeeReport(coffeeType) {
    try {
        console.log('📝 Solicitando informe keniano para:', coffeeType);
        
        const response = await fetch(COFFEE_CLASSIFICATION_REPORT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: `Genera un informe específico sobre la clasificación "${coffeeType}" en el sistema keniano de clasificación de café. Explica qué significa esta clasificación, sus características principales, calidad y estándares según el sistema keniano.`,
                language: 'español'
            })
        });

        const data = await response.json();
        return data.response || 'Informe no disponible en este momento.';

    } catch (error) {
        console.error('❌ Error obteniendo el informe:', error);
        return 'Error al generar el informe. Por favor, intenta nuevamente.';
    }
}

// Funciones de utilidad
const cleanText = (text) => {
    if (!text || typeof text !== 'string') return '';
    
    return text
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^\w\s]/gi, ' ')
        .replace(/\s+/g, ' ')
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

// Función para analizar contexto de la conversación
const analyzeConversationContext = (currentMessage, previousMessages = []) => {
    const cleanCurrent = cleanText(currentMessage);
    
    // 1. Buscar palabras de café en el mensaje actual
    const hasCurrentCoffee = ALLOWED_COFFEE_TOPICS.some(topic => {
        const cleanTopic = cleanText(topic);
        const regex = new RegExp(`\\b${cleanTopic}\\b`, 'i');
        return regex.test(cleanCurrent);
    });
    
    // 2. Analizar mensajes anteriores para contexto
    let hasPreviousCoffeeContext = false;
    let conversationTopics = [];
    
    // Revisar últimos 3-5 mensajes para contexto
    const recentMessages = previousMessages.slice(-5);
    recentMessages.forEach(msg => {
        const cleanMsg = cleanText(msg.text || msg);
        ALLOWED_COFFEE_TOPICS.forEach(topic => {
            const cleanTopic = cleanText(topic);
            const regex = new RegExp(`\\b${cleanTopic}\\b`, 'i');
            if (regex.test(cleanMsg)) {
                hasPreviousCoffeeContext = true;
                if (!conversationTopics.includes(topic)) {
                    conversationTopics.push(topic);
                }
            }
        });
    });
    
    // 3. Detectar preguntas implícitas sobre el tema actual
    const isFollowUpQuestion = 
        // Palabras que indican continuación
        /\b(y|además|también|otro|otra|más|sobre|respecto|acerca)\b/i.test(cleanCurrent) ||
        // Preguntas sobre "eso", "eso", "lo mismo", etc.
        /\b(eso|esto|aquello|lo mismo|el mismo|la misma)\b/i.test(cleanCurrent) ||
        // Preguntas que empiezan con "qué", "cómo", "cuándo", etc. en contexto de café
        (/^(qué|cómo|cuándo|dónde|por qué|cuál|quién)\b/i.test(cleanCurrent) && hasPreviousCoffeeContext);
    
    return {
        hasCurrentCoffee,
        hasPreviousCoffeeContext,
        conversationTopics,
        isFollowUpQuestion,
        isInCoffeeContext: hasCurrentCoffee || (hasPreviousCoffeeContext && isFollowUpQuestion)
    };
};

// FUNCIÓN Detectar temas prohibidos con contexto más amplio
const containsForbiddenTopic = (message, previousMessages = []) => {
    const cleanMessage = cleanText(message);
    console.log('🔍 Analizando mensaje:', cleanMessage);
    
    // Analizar contexto de conversación
    const context = analyzeConversationContext(message, previousMessages);
    console.log('📊 Contexto analizado:', context);
    
    // REGLA 1: Saludos y despedidas siempre permitidos
    if (isGreeting(message) || isThanksOrGoodbye(message)) {
        console.log('✅ Saludo/Despedida - PERMITIDO');
        return false;
    }
    
    // REGLA 2: Si está en contexto de café (nicaragua o internacional), es más permisivo
    if (context.isInCoffeeContext) {
        console.log('✅ En contexto de café - VERIFICADO');
        
        // En contexto de café, solo bloquear temas MUY prohibidos
        const hasStrongForbidden = FORBIDDEN_TOPICS_PATTERNS.some(pattern => {
            // Temas sensibles que NUNCA se permiten
            const sensitiveTopics = ['sexo', 'violencia', 'drogas', 'arma', 'pistola', 'matar', 'asesinato'];
            
            if (sensitiveTopics.some(s => pattern.topic.includes(s))) {
                const hasSensitive = pattern.keywords?.some(keyword => {
                    const cleanKeyword = cleanText(keyword);
                    const regex = new RegExp(`\\b${cleanKeyword}\\b`, 'i');
                    return regex.test(cleanMessage);
                });
                
                if (hasSensitive) {
                    console.log(`❌ Tema sensible detectado: ${pattern.topic}`);
                    return true;
                }
            }
            return false;
        });
        
        if (hasStrongForbidden) {
            console.log('❌ Tema sensible en contexto de café - RECHAZADO');
            return true;
        }
        
        console.log('✅ Mensaje en contexto de café - PERMITIDO');
        return false;
    }
    
    // Fuera de contexto, verificar que tenga relación con café (nicaragua o internacional)
    const hasCoffeeRelation = ALLOWED_COFFEE_TOPICS.some(topic => {
        const cleanTopic = cleanText(topic);
        const regex = new RegExp(`\\b${cleanTopic}\\b`, 'i');
        return regex.test(cleanMessage);
    });
    
    if (!hasCoffeeRelation) {
        console.log('❌ Sin relación con café y sin contexto - RECHAZADO');
        return true;
    }
    
    // REGLA 4: Si tiene relación con café, verificar que no mezcle con temas prohibidos fuertes
    const hasForbiddenMix = FORBIDDEN_TOPICS_PATTERNS.some(pattern => {
        const { topic, keywords, phrases, exactMatches } = pattern;
        
        // Verificar coincidencias exactas (siempre prohibidas)
        if (exactMatches && exactMatches.some(exact => {
            const cleanExact = cleanText(exact);
            const regex = new RegExp(`\\b${cleanExact}\\b`, 'i');
            return regex.test(cleanMessage);
        })) {
            console.log(`❌ Coincidencia exacta prohibida: ${topic}`);
            return true;
        }
        
        // Verificar múltiples palabras clave del mismo tema prohibido
        if (keywords) {
            const foundKeywords = keywords.filter(keyword => {
                const cleanKeyword = cleanText(keyword);
                const regex = new RegExp(`\\b${cleanKeyword}\\b`, 'i');
                return regex.test(cleanMessage);
            });
            
            // Si encuentra 2+ palabras de un tema prohibido, rechazar
            if (foundKeywords.length >= 2) {
                console.log(`❌ Múltiples palabras prohibidas: ${topic} - ${foundKeywords}`);
                return true;
            }
        }
        
        return false;
    });
    
    if (hasForbiddenMix) {
        console.log('❌ Mezcla de café con tema prohibido - RECHAZADO');
        return true;
    }
    
    console.log('✅ Mensaje relacionado con café - PERMITIDO');
    return false;
};

// Clase principal del chat actualizada
class CoffeeAssistant {
    constructor() {
        this.messages = [];
        this.isTyping = false;
        this.typingInterval = null;
        this.currentDot = 0;
        this.conversationContext = {
            hasCoffeeTopic: false,
            lastTopics: [],
            isCoffeeConversation: false
        };
        
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
    
    // Actualizar contexto de conversación
    updateConversationContext() {
        if (this.messages.length > 0) {
            const lastUserMessages = this.messages
                .filter(msg => msg.sender === 'user')
                .slice(-3)
                .map(msg => msg.text);
            
            const context = analyzeConversationContext(
                lastUserMessages[lastUserMessages.length - 1] || '', 
                lastUserMessages
            );
            
            this.conversationContext = {
                hasCoffeeTopic: context.hasPreviousCoffeeContext,
                lastTopics: context.conversationTopics,
                isCoffeeConversation: context.hasPreviousCoffeeContext
            };
        }
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
        console.log('Mensaje:', message);
        console.log('Contexto actual:', this.conversationContext);
        
        const previousUserMessages = this.messages
            .filter(msg => msg.sender === 'user')
            .map(msg => msg.text);
        
        const forbidden = containsForbiddenTopic(message, previousUserMessages);
        console.log('¿Contiene tema prohibido?', forbidden);
        
        // Verificar si es un saludo
        if (isGreeting(message)) {
            const topicsText = SUGGESTED_TOPICS.map(topic => `• ${topic}`).join('\n');
            return `¡Hola! 👋 Soy CentralCoffeeIA, tu asistente especializado en el café nicaragüense. 

Puedo ayudarte con temas como:

${topicsText}

¿En qué aspecto del café te gustaría que te ayude hoy? ☕`;
        }

        // Verificar si es agradecimiento o despedida
        if (isThanksOrGoodbye(message)) {
            return "¡De nada! 😊 Ha sido un placer ayudarte. Si tienes más preguntas sobre café nicaragüense o internacional, aquí estaré. ¡Que tengas un excelente día! ☕";
        }

        // Verificar temas prohibidos CON CONTEXTO
        if (forbidden) {
            // Mensaje más contextual
            if (this.conversationContext.hasCoffeeTopic) {
                return "Noto que estamos hablando de café. Me centro específicamente en aspectos técnicos y comerciales del café, tanto de Nicaragua como a nivel mundial. ¿Podrías reformular tu pregunta manteniendo el enfoque en el café?";
            }
            
            const topicsText = SUGGESTED_TOPICS.slice(0, 5).map(topic => `• ${topic}`).join('\n');
            return `Lo siento, sólo puedo ofrecer información especializada sobre café:\n\n${topicsText}`;
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
        
        // Actualizar contexto
        this.updateConversationContext();
        
        this.startTypingIndicator();

        // Verificar respuestas automáticas
        const automaticResponse = this.handleAutomaticResponse(message);
        
        if (automaticResponse) {
            setTimeout(() => {
                this.stopTypingIndicator();
                this.addMessage(automaticResponse, 'bot');
                this.updateConversationContext();
            }, 1000);
            return;
        }

        // Si no es respuesta automática, consultar la API
        try {
            const aiResponse = await this.sendMessageToAPI(message);
            
            setTimeout(() => {
                this.stopTypingIndicator();
                this.addMessage(aiResponse, 'bot');
                this.updateConversationContext();
            }, 1000);

        } catch (error) {
            console.error('Error al procesar mensaje:', error);
            setTimeout(() => {
                this.stopTypingIndicator();
                this.addMessage('Error al procesar tu mensaje. Por favor, inténtalo de nuevo.', 'bot');
                this.updateConversationContext();
            }, 1000);
        }
    }
    
    addMessage(text, sender) {
        const messageElement = document.createElement('div');
        
        // Usar 'bot-message' en lugar de 'ai-message'
        messageElement.className = `message ${sender === 'user' ? 'user-message' : 'bot-message'}`;
        
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
        
        // Usar 'bot-message' en lugar de 'ai-message'
        typingElement.className = 'message bot-message typing-indicator';
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
            this.conversationContext = {
                hasCoffeeTopic: false,
                lastTopics: [],
                isCoffeeConversation: false
            };
            
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