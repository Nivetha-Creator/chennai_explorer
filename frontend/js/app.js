const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat-btn");
const clearChatBtn = document.getElementById("clear-chat-btn");


let sessionId = crypto.randomUUID();
let selectedLanguage = "en";


/* =====================================
   FORMAT BOT RESPONSE
===================================== */

function formatBotMessage(text) {

    let safeText = escapeHTML(text);


    // Bold text: **text**
    safeText = safeText.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    // Bullet points
    safeText = safeText.replace(
        /^\s*[-•]\s+(.*)$/gm,
        "<div class=\"response-bullet\">• $1</div>"
    );


    // Numbered points
    safeText = safeText.replace(
        /^\s*(\d+)\.\s+(.*)$/gm,
        "<div class=\"response-number\"><strong>$1.</strong> $2</div>"
    );


    // Convert remaining line breaks
    safeText = safeText.replace(
        /\n/g,
        "<br>"
    );


    return safeText;
}


/* =====================================
   ADD MESSAGE
===================================== */

function addMessage(message, type) {

    const welcome = document.getElementById("welcome-area");

    if (welcome) {
        welcome.remove();
    }


    const messageElement = document.createElement("div");

    messageElement.className = `message ${type}`;


    const formattedMessage =
        type === "bot"
            ? formatBotMessage(message)
            : escapeHTML(message);


    messageElement.innerHTML = `
        <div class="message-content">
            ${formattedMessage}
        </div>
    `;


    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =====================================
   ESCAPE HTML
===================================== */

function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


/* =====================================
   TYPING INDICATOR
===================================== */

function showTypingIndicator() {

    const existing =
        document.getElementById("typing-indicator");

    if (existing) {
        return;
    }


    const typingElement =
        document.createElement("div");


    typingElement.className = "message bot";

    typingElement.id = "typing-indicator";


    typingElement.innerHTML = `
        <div class="message-content">
            <span>Chennai Explorer is typing...</span>
        </div>
    `;


    chatBox.appendChild(typingElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}


/* =====================================
   REMOVE TYPING INDICATOR
===================================== */

function removeTypingIndicator() {

    const typingElement =
        document.getElementById("typing-indicator");


    if (typingElement) {
        typingElement.remove();
    }
}


/* =====================================
   SEND MESSAGE
===================================== */

async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message) {
        return;
    }


    addMessage(message, "user");


    messageInput.value = "";

    messageInput.style.height = "auto";


    sendBtn.disabled = true;

    showTypingIndicator();


    try {

        const data = await sendChatMessage(
            message,
            sessionId,
            selectedLanguage
        );


        removeTypingIndicator();


        addMessage(
            data.reply,
            "bot"
        );


        if (data.session_id) {
            sessionId = data.session_id;
        }


    } catch (error) {

        removeTypingIndicator();


        console.error(error);


        addMessage(
            "Sorry, I couldn't connect to the Chennai Explorer AI right now. Please try again.",
            "bot"
        );


    } finally {

        sendBtn.disabled = false;

        messageInput.focus();
    }
}


/* =====================================
   ENTER TO SEND
===================================== */

messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();
        }

    }
);


/* =====================================
   AUTO RESIZE TEXTAREA
===================================== */

messageInput.addEventListener(
    "input",
    function() {

        this.style.height = "auto";

        this.style.height =
            `${Math.min(this.scrollHeight, 120)}px`;

    }
);


/* =====================================
   SEND BUTTON
===================================== */

sendBtn.addEventListener(
    "click",
    sendMessage
);


/* =====================================
   NEW CHAT
===================================== */

newChatBtn.addEventListener(
    "click",
    function() {

        sessionId = crypto.randomUUID();

        location.reload();

    }
);


/* =====================================
   CLEAR CHAT
===================================== */

clearChatBtn.addEventListener(
    "click",
    function() {

        sessionId = crypto.randomUUID();

        location.reload();

    }
);


/* =====================================
   SUGGESTION / NAVIGATION BUTTONS
===================================== */

document
    .querySelectorAll("[data-message]")
    .forEach(button => {

        button.addEventListener(
            "click",
            function() {

                const message =
                    this.dataset.message;

                messageInput.value = message;

                sendMessage();

            }
        );

    });