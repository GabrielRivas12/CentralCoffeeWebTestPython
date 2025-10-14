const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const resultDiv = document.getElementById("result");

// Analizar la imagen automáticamente al subirla
imageInput.addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  // Previsualizar imagen
  const reader = new FileReader();
  reader.onload = function (e) {
    preview.src = e.target.result;
    preview.style.display = "block";
  };
  reader.readAsDataURL(file);

  // Analizar automáticamente
  resultDiv.innerHTML = `<p>Analizando imagen "${file.name}"...</p>`;
  setTimeout(() => {
    resultDiv.innerHTML = `
            <p>Resultado del reconocimiento de la imagen "${file.name}":</p>
            <ul>
                <li>Etiqueta 1: 92%</li>
                <li>Etiqueta 2: 85%</li>
                <li>Etiqueta 3: 60%</li>
            </ul>
        `;
  }, 1000);
});

// Chatbot
const messagesDiv = document.getElementById("messages");

function sendMessage() {
  const input = document.getElementById("userInput");
  const text = input.value.trim();
  if (!text) return;

  const userMsg = document.createElement("div");
  userMsg.classList.add("user-message");
  userMsg.textContent = text;
  messagesDiv.appendChild(userMsg);

  input.value = "";
  messagesDiv.scrollTop = messagesDiv.scrollHeight;

  setTimeout(() => {
    const botMsg = document.createElement("div");
    botMsg.classList.add("bot-message");
    botMsg.textContent = `Aquí iría la respuesta del bot a: "${text}"`;
    messagesDiv.appendChild(botMsg);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }, 500);
}

document.getElementById("userInput").addEventListener("keypress", function (e) {
  if (e.key === "Enter") sendMessage();
});
