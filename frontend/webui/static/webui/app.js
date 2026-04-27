const chatForm = document.querySelector("#chatForm");
const chatLog = document.querySelector("#chatLog");
const messageInput = document.querySelector("#messageInput");
const sendButton = document.querySelector("#sendButton");
const deviceSelect = document.querySelector("#deviceSelect");

const sessionId = crypto.randomUUID ? crypto.randomUUID() : String(Date.now());

function appendMessage(role, text) {
  const message = document.createElement("article");
  message.className = `message ${role}`;
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  message.appendChild(paragraph);
  chatLog.appendChild(message);
  chatLog.scrollTop = chatLog.scrollHeight;
  return message;
}

async function sendMessage(message) {
  const response = await fetch("/api/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      selected_device: deviceSelect.value,
      session_id: sessionId,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "요청 처리 중 오류가 발생했습니다.");
  }
  return data.answer;
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = messageInput.value.trim();
  if (!message) {
    return;
  }

  appendMessage("user", message);
  messageInput.value = "";
  sendButton.disabled = true;
  const loadingMessage = appendMessage("bot loading", "답변을 생성하고 있습니다...");

  try {
    const answer = await sendMessage(message);
    loadingMessage.classList.remove("loading");
    loadingMessage.querySelector("p").textContent = answer;
  } catch (error) {
    loadingMessage.classList.remove("loading");
    loadingMessage.querySelector("p").textContent = error.message;
  } finally {
    sendButton.disabled = false;
    messageInput.focus();
  }
});

messageInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    chatForm.requestSubmit();
  }
});
