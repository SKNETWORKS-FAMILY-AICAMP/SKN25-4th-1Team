const body = document.body;
const chatUrl = body.dataset.chatUrl;
const deviceUrl = body.dataset.deviceUrl;
const resetUrl = body.dataset.resetUrl;
const initialView = body.dataset.initialView || "chat";
const deviceData = JSON.parse(document.getElementById("device-data").textContent);

const navButtons = Array.from(document.querySelectorAll("[data-view-target]"));
const chatView = document.getElementById("chat-view");
const faqView = document.getElementById("faq-view");
const chatForm = document.getElementById("chat-form");
const chatQuestion = document.getElementById("chat-question");
const chatMessages = document.getElementById("chat-messages");
const deviceForm = document.getElementById("device-form");
const seriesSelect = document.getElementById("series-select");
const deviceSelect = document.getElementById("device-select");
const resetChatButton = document.getElementById("reset-chat-button");
const selectedDeviceBadge = document.getElementById("selected-device-badge");

function getCsrfToken() {
    const tokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
    return tokenInput ? tokenInput.value : "";
}

function escapeHtml(value) {
    return value
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function updateUrlView(viewName) {
    const url = new URL(window.location.href);
    url.searchParams.set("view", viewName);
    window.history.replaceState({}, "", url);
}

function setView(viewName) {
    const showChat = viewName !== "faq";
    chatView.hidden = !showChat;
    faqView.hidden = showChat;

    navButtons.forEach((button) => {
        button.classList.toggle("is-active", button.dataset.viewTarget === viewName);
    });

    updateUrlView(viewName);
}

function renderMessage(role, content) {
    const article = document.createElement("article");
    article.className = `chat-bubble chat-bubble--${role}`;
    article.innerHTML = `
        <span class="chat-role">${role === "assistant" ? "AI" : "사용자"}</span>
        <div class="chat-content">${escapeHtml(content).replaceAll("\n", "<br>")}</div>
    `;
    return article;
}

function appendMessage(role, content) {
    chatMessages.appendChild(renderMessage(role, content));
    chatMessages.lastElementChild?.scrollIntoView({ behavior: "smooth", block: "end" });
}

function replaceMessages(messages) {
    chatMessages.innerHTML = "";
    messages.forEach((message) => {
        appendMessage(message.role, message.content);
    });
}

function buildDeviceOptions(seriesName, selectedDevice) {
    const fragment = document.createDocumentFragment();
    let options = [];

    if (seriesName === "기타") {
        options = ["기타 기기"];
    } else if (seriesName === "선택하지 않음") {
        options = ["선택하지 않음"];
    } else {
        options = deviceData[seriesName] || [];
    }

    if (!options.length) {
        options = ["선택하지 않음"];
    }

    options.forEach((optionValue) => {
        const option = document.createElement("option");
        option.value = optionValue;
        option.textContent = optionValue;
        option.selected = optionValue === selectedDevice;
        fragment.appendChild(option);
    });

    deviceSelect.replaceChildren(fragment);
}

async function submitQuestion(question) {
    if (!question.trim()) {
        return;
    }

    appendMessage("user", question);
    chatQuestion.value = "";
    setView("chat");

    const pendingMessage = renderMessage("assistant", "답변을 준비 중입니다...");
    chatMessages.appendChild(pendingMessage);

    try {
        const response = await fetch(chatUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({ question }),
        });
        const payload = await response.json();
        pendingMessage.remove();

        if (!response.ok) {
            appendMessage("assistant", payload.error || "질문을 처리하지 못했습니다.");
            return;
        }

        appendMessage("assistant", payload.answer);
    } catch (error) {
        pendingMessage.remove();
        appendMessage("assistant", "서버와 통신하는 중 오류가 발생했습니다.");
    }
}

navButtons.forEach((button) => {
    button.addEventListener("click", () => {
        setView(button.dataset.viewTarget);
    });
});

seriesSelect.addEventListener("change", () => {
    buildDeviceOptions(seriesSelect.value, deviceSelect.value);
});

deviceForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(deviceForm);
    const response = await fetch(deviceUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken(),
        },
        body: formData,
    });

    if (!response.ok) {
        return;
    }

    const payload = await response.json();
    selectedDeviceBadge.textContent = `기기: ${payload.selected_device}`;
    buildDeviceOptions(payload.selected_series, payload.selected_device);
});

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    await submitQuestion(chatQuestion.value);
});

document.querySelectorAll("[data-question]").forEach((button) => {
    button.addEventListener("click", async () => {
        await submitQuestion(button.dataset.question || "");
    });
});

resetChatButton.addEventListener("click", async () => {
    const response = await fetch(resetUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCsrfToken(),
        },
    });

    if (!response.ok) {
        return;
    }

    const payload = await response.json();
    replaceMessages(payload.messages || []);
    setView("chat");
});

buildDeviceOptions(seriesSelect.value, deviceSelect.dataset.selectedDevice || "선택하지 않음");
setView(initialView);
