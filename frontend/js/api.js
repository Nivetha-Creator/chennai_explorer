const API_BASE_URL = "";


async function sendChatMessage(message, sessionId = null, language = "en") {

    const response = await fetch(`${API_BASE_URL}/api/chat`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: message,
            session_id: sessionId,
            language: language
        })
    });


    if (!response.ok) {

        const errorData = await response.json().catch(() => ({}));

        throw new Error(
            errorData.detail || "Unable to connect to Chennai Explorer."
        );
    }


    return await response.json();
}