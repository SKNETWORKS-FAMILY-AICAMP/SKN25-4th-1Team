const LANG_KEY = "smartcs-lang";

const T = {
    ko: {
        "nav.faq": "FAQ",
        "nav.service-centers": "서비스센터",
        "nav.login": "로그인",
        "nav.signup": "회원가입",
        "home.hero-title": "무엇을 도와드릴까요?",
        "home.series-label": "기기 시리즈",
        "home.select-series": "시리즈 선택",
        "home.model-label": "기기 모델",
        "home.search-placeholder": "무엇이든 물어보세요",
        "faq.title": "자주 묻는 질문",
        "faq.search-placeholder": "검색어를 입력하세요",
        "faq.top-topics": "인기 주제",
        "faq.back": "목록으로",
        "faq.related": "관련 질문",
        "search.eyebrow": "검색 / 필터",
        "search.desc": "최신순, 조회순, 제목순 정렬과 카테고리 필터를 적용해 FAQ를 찾아보세요.",
        "search.keyword-placeholder": "FAQ 제목 또는 내용을 검색하세요",
        "search.all-categories": "전체 카테고리",
        "search.sort-latest": "최신순",
        "search.sort-views": "조회순",
        "search.sort-title": "제목순",
        "search.submit": "검색",
        "search.empty-title": "FAQ를 찾지 못했어요.",
        "search.empty-desc": "현재 조건에 맞는 FAQ가 없습니다.",
        "search.chat-link": "채팅으로 이어가기",
        "sc.eyebrow": "서비스센터",
        "sc.title": "현재 위치 기준으로 가까운 서비스센터를 찾아보세요.",
        "sc.desc": "좌표를 입력하면 가까운 서비스센터를 조회할 수 있습니다.",
        "sc.lat-placeholder": "위도",
        "sc.lng-placeholder": "경도",
        "sc.submit": "가까운 센터 조회",
        "sc.map-placeholder": "지도 연동 영역",
        "sc.nearby-title": "가까운 센터",
        "sc.nearby-desc": "거리순으로 정렬된 결과입니다.",
        "sc.empty-title": "센터 정보를 불러오지 못했어요.",
        "sc.empty-desc": "Kakao API 키 또는 네트워크 상태를 확인해 주세요.",
        "login.title": "로그인",
        "login.subtitle": "Smart CS 기능을 사용하려면 로그인해 주세요.",
        "login.email": "이메일",
        "login.email-placeholder": "example@email.com",
        "login.password": "비밀번호",
        "login.password-placeholder": "비밀번호를 입력해 주세요",
        "login.submit": "로그인",
        "login.signup-link": "계정이 없으신가요? 회원가입",
        "signup.title": "회원가입",
        "signup.subtitle": "Smart CS 계정을 만들고 서비스를 이용해 보세요.",
        "signup.name": "이름",
        "signup.name-placeholder": "이름을 입력해 주세요",
        "signup.email": "이메일",
        "signup.email-placeholder": "example@email.com",
        "signup.password": "비밀번호",
        "signup.password-placeholder": "비밀번호를 입력해 주세요",
        "signup.confirm": "비밀번호 확인",
        "signup.confirm-placeholder": "비밀번호를 다시 입력해 주세요",
        "signup.submit": "회원가입",
        "signup.login-link": "이미 계정이 있으신가요? 로그인",
        "common.voice": "음성 입력",
        "common.listening": "듣는 중...",
        "common.reset-chat": "대화 초기화",
        "common.send": "전송",
        "common.voice-unsupported": "이 브라우저는 음성 인식을 지원하지 않습니다.",
        "common.voice-start-error": "음성 인식을 시작하지 못했습니다.",
        "common.voice-not-allowed": "마이크 권한이 거부되었습니다.",
        "common.voice-service-not-allowed": "브라우저에서 음성 인식 서비스가 차단되었습니다.",
        "common.voice-no-speech": "음성이 감지되지 않았습니다. 다시 시도해 주세요.",
        "common.voice-audio-capture": "사용 가능한 마이크를 찾지 못했습니다.",
        "common.voice-network": "음성 인식 중 네트워크 오류가 발생했습니다.",
        "common.voice-fallback-error": "음성 입력을 가져오지 못했습니다. 다시 시도해 주세요.",
    },
    en: {
        "nav.faq": "FAQ",
        "nav.service-centers": "Service Centers",
        "nav.login": "Login",
        "nav.signup": "Sign Up",
        "home.hero-title": "How can we help you?",
        "home.series-label": "Device Series",
        "home.select-series": "Select series",
        "home.model-label": "Device Model",
        "home.search-placeholder": "Ask anything",
        "faq.title": "Frequently Asked Questions",
        "faq.search-placeholder": "Enter a search term",
        "faq.top-topics": "Top Topics",
        "faq.back": "Back to list",
        "faq.related": "Related Questions",
        "search.eyebrow": "Search / Filter",
        "search.desc": "Browse FAQs with sorting by latest, views, and title, plus category filtering.",
        "search.keyword-placeholder": "Search FAQ title or content",
        "search.all-categories": "All Categories",
        "search.sort-latest": "Latest",
        "search.sort-views": "Most Viewed",
        "search.sort-title": "By Title",
        "search.submit": "Search",
        "search.empty-title": "No FAQ found.",
        "search.empty-desc": "No FAQ matches the current filters.",
        "search.chat-link": "Continue in chat",
        "sc.eyebrow": "Service Centers",
        "sc.title": "Find nearby service centers from your current location.",
        "sc.desc": "Enter coordinates to check the nearest service centers.",
        "sc.lat-placeholder": "Latitude",
        "sc.lng-placeholder": "Longitude",
        "sc.submit": "Find Nearby Centers",
        "sc.map-placeholder": "Reserved area for future map integration.",
        "sc.nearby-title": "Nearby Centers",
        "sc.nearby-desc": "Results are sorted by distance.",
        "sc.empty-title": "Could not load center information.",
        "sc.empty-desc": "Please check your Kakao API key or network connection.",
        "login.title": "Login",
        "login.subtitle": "Sign in to use Smart CS features.",
        "login.email": "Email",
        "login.email-placeholder": "example@email.com",
        "login.password": "Password",
        "login.password-placeholder": "Enter your password",
        "login.submit": "Login",
        "login.signup-link": "No account? Sign up",
        "signup.title": "Sign Up",
        "signup.subtitle": "Create your Smart CS account and start using support features.",
        "signup.name": "Name",
        "signup.name-placeholder": "Enter your name",
        "signup.email": "Email",
        "signup.email-placeholder": "example@email.com",
        "signup.password": "Password",
        "signup.password-placeholder": "Enter your password",
        "signup.confirm": "Confirm Password",
        "signup.confirm-placeholder": "Enter your password again",
        "signup.submit": "Sign Up",
        "signup.login-link": "Already have an account? Login",
        "common.voice": "Voice",
        "common.listening": "Listening...",
        "common.reset-chat": "Reset Chat",
        "common.send": "Send",
        "common.voice-unsupported": "This browser does not support speech recognition.",
        "common.voice-start-error": "Could not start speech recognition.",
        "common.voice-not-allowed": "Microphone permission was denied.",
        "common.voice-service-not-allowed": "Speech service is blocked in this browser.",
        "common.voice-no-speech": "No speech was detected. Please try again.",
        "common.voice-audio-capture": "No microphone was found.",
        "common.voice-network": "Speech recognition network error occurred.",
        "common.voice-fallback-error": "Could not get voice input. Please try again.",
    },
};

function getCurrentLang() {
    return localStorage.getItem(LANG_KEY) || "ko";
}

function getBackendLanguage(lang = getCurrentLang()) {
    return lang === "en" ? "english" : "korean";
}

function translate(key, lang = getCurrentLang()) {
    const table = T[lang] || T.ko;
    return table[key] ?? key;
}

function applyTranslations(lang) {
    const t = T[lang] || T.ko;

    document.documentElement.lang = lang === "en" ? "en" : "ko";

    document.querySelectorAll("[data-i18n]").forEach((el) => {
        const val = t[el.dataset.i18n];
        if (val !== undefined) {
            el.textContent = val;
        }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
        const val = t[el.dataset.i18nPlaceholder];
        if (val !== undefined) {
            el.placeholder = val;
        }
    });

    document.querySelectorAll("[data-result-count]").forEach((el) => {
        const count = el.dataset.resultCount;
        el.textContent = lang === "en" ? `${count} result(s)` : `검색 결과 ${count}건`;
    });

    const voiceButtons = document.querySelectorAll("[data-i18n-voice-button]");
    voiceButtons.forEach((button) => {
        if (!button.classList.contains("is-listening")) {
            button.textContent = translate("common.voice", lang);
        }
    });

    const resetButton = document.querySelector("[data-i18n-reset-button]");
    if (resetButton) {
        resetButton.textContent = translate("common.reset-chat", lang);
    }

    const sendButton = document.querySelector("[data-i18n-send-button]");
    if (sendButton) {
        sendButton.textContent = translate("common.send", lang);
    }

    const selectedLanguageInput = document.querySelector("#selected-language");
    if (selectedLanguageInput) {
        selectedLanguageInput.value = getBackendLanguage(lang);
    }

    document.querySelectorAll("[data-home-prompt-tag]").forEach((el) => {
        const nextText = lang === "en" ? el.dataset.tagEn : el.dataset.tagKo;
        if (nextText) {
            el.textContent = nextText;
        }
    });
}

function setLanguage(lang, options = {}) {
    const { syncServer = true, reloadDynamicPages = false } = options;
    localStorage.setItem(LANG_KEY, lang);
    applyTranslations(lang);
    document.querySelectorAll("[data-language-toggle]").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.languageToggle === lang);
    });

    if (!syncServer) {
        return;
    }

    const formData = new FormData();
    formData.append("selected_language", getBackendLanguage(lang));
    postForm("/language/", formData)
        .then(() => {
            const currentPath = window.location.pathname;
            if (reloadDynamicPages && (currentPath.startsWith("/faq/") || currentPath.startsWith("/search/"))) {
                window.location.reload();
            }
        })
        .catch(() => null);
}

function getCookie(name) {
    const cookies = document.cookie ? document.cookie.split(";") : [];
    for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(`${name}=`)) {
            return decodeURIComponent(trimmed.slice(name.length + 1));
        }
    }
    return "";
}

function postForm(url, formData) {
    const csrfToken =
        document.querySelector('meta[name="csrf-token"]')?.getAttribute("content") ||
        document.querySelector("[name=csrfmiddlewaretoken]")?.value ||
        getCookie("csrftoken") ||
        "";
    return fetch(url, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrfToken,
        },
        body: formData,
    }).then((response) => response.json());
}

function renderChatMessage(role, content) {
    const article = document.createElement("article");
    article.className = `message ${role}`;

    const roleLabel = document.createElement("span");
    roleLabel.className = "role";
    roleLabel.textContent = role;

    const text = document.createElement("p");
    text.textContent = content;

    article.append(roleLabel, text);
    return article;
}

function syncHomeChatState() {
    const shell = document.querySelector(".home-chat-shell");
    const chatLog = document.querySelector("#chat-log");
    if (!shell || !chatLog) {
        return;
    }

    const visibleMessages = chatLog.querySelectorAll(".message").length;
    const isPristine = visibleMessages <= 1;
    shell.classList.toggle("is-pristine", isPristine);
    shell.classList.toggle("has-history", !isPristine);
}

function initDeviceSelection() {
    const seriesSelect = document.querySelector("[data-device-source]");
    const deviceSelect = document.querySelector("#device-select");
    if (!seriesSelect || !deviceSelect) {
        return;
    }

    const selectedDevice = deviceSelect.dataset.selectedDevice || "선택하지 않음";
    const selectedDeviceDisplay = deviceSelect.dataset.selectedDeviceDisplay || selectedDevice;

    function getModelsFromOption(option) {
        if (!option || !option.dataset.models) {
            return [];
        }
        return option.dataset.models
            .split("||")
            .map((model) => model.trim())
            .filter(Boolean);
    }

    function getDisplayModelsFromOption(option) {
        if (!option || !option.dataset.displayModels) {
            return [];
        }
        return option.dataset.displayModels
            .split("||")
            .map((model) => model.trim())
            .filter(Boolean);
    }

    function renderDeviceOptions(models, displayModels, preferredModel = "") {
        deviceSelect.innerHTML = "";

        if (!models.length) {
            const emptyOption = document.createElement("option");
            emptyOption.value = "선택하지 않음";
            emptyOption.textContent = getCurrentLang() === "en" ? "Not selected" : "선택하지 않음";
            deviceSelect.appendChild(emptyOption);
            return;
        }

        models.forEach((model, index) => {
            const nextOption = document.createElement("option");
            nextOption.value = model;
            nextOption.textContent = displayModels[index] || model;
            if ((preferredModel && model === preferredModel) || (!preferredModel && index === 0)) {
                nextOption.selected = true;
            }
            deviceSelect.appendChild(nextOption);
        });
    }

    function syncModelsForSelectedSeries(preferredModel = "") {
        const option = seriesSelect.options[seriesSelect.selectedIndex];
        const models = getModelsFromOption(option);
        const displayModels = getDisplayModelsFromOption(option);
        renderDeviceOptions(models, displayModels, preferredModel);
    }

    const seriesOptions = Array.from(seriesSelect.options).slice(1);
    const matchedSeriesOption = seriesOptions.find((option) => getModelsFromOption(option).includes(selectedDevice));

    if (matchedSeriesOption) {
        seriesSelect.value = matchedSeriesOption.value;
        syncModelsForSelectedSeries(selectedDevice);
    } else {
        deviceSelect.innerHTML = "";
        const emptyOption = document.createElement("option");
        emptyOption.value = selectedDevice;
        emptyOption.textContent = selectedDeviceDisplay;
        deviceSelect.appendChild(emptyOption);
    }

    seriesSelect.addEventListener("change", () => {
        syncModelsForSelectedSeries("");
    });

    deviceSelect.addEventListener("change", () => {
        const formData = new FormData();
        formData.append("selected_device", deviceSelect.value);
        postForm("/device/", formData).catch(() => null);
    });
}

function initChat() {
    const form = document.querySelector("#chat-form");
    const chatLog = document.querySelector("#chat-log");
    const quickButtons = document.querySelectorAll("[data-quick-question]");
    const questionInput = document.querySelector("#chat-question");
    const resetButton = document.querySelector("#reset-chat-button");
    const selectedLanguageInput = document.querySelector("#selected-language");

    if (!form || !chatLog || !questionInput) {
        return;
    }

    async function submitQuestion(question, answerOverride = "") {
        const normalizedQuestion = (question ?? questionInput.value).trim();
        if (!normalizedQuestion) {
            return;
        }

        questionInput.value = "";
        chatLog.appendChild(renderChatMessage("user", normalizedQuestion));
        syncHomeChatState();

        if (answerOverride && getCurrentLang() !== "en") {
            chatLog.appendChild(renderChatMessage("assistant", answerOverride));
            syncHomeChatState();
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        const formData = new FormData(form);
        formData.set("question", normalizedQuestion);
        formData.set("answer_override", getCurrentLang() === "en" ? "" : answerOverride);
        formData.set("selected_language", getBackendLanguage());
        if (selectedLanguageInput) {
            selectedLanguageInput.value = getBackendLanguage();
        }

        try {
            const payload = await postForm(form.action, formData);
            if (!answerOverride || getCurrentLang() === "en") {
                const answer = payload?.answer || "답변을 가져오지 못했습니다. 다시 시도해 주세요.";
                chatLog.appendChild(renderChatMessage("assistant", answer));
                syncHomeChatState();
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        } catch (error) {
            if (!answerOverride || getCurrentLang() === "en") {
                chatLog.appendChild(renderChatMessage("assistant", "요청 처리 중 오류가 발생했습니다."));
                syncHomeChatState();
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        }
    }

    quickButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            await submitQuestion(button.dataset.quickQuestion || "", button.dataset.quickAnswer || "");
        });
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        await submitQuestion(questionInput.value, "");
    });

    if (resetButton) {
        resetButton.addEventListener("click", async () => {
            const formData = new FormData();
            await postForm("/chat/reset/", formData);
            window.location.reload();
        });
    }

    syncHomeChatState();
}

function initHomeResetLink() {
    const homeLink = document.querySelector("[data-home-reset-link]");
    if (!homeLink) {
        return;
    }

    homeLink.addEventListener("click", async (event) => {
        event.preventDefault();
        const formData = new FormData();
        try {
            await postForm("/chat/reset/", formData);
        } catch (error) {
            // Even if reset fails, still move the user home.
        }
        window.location.href = homeLink.href;
    });
}

function initLandingTools() {
    const langButtons = document.querySelectorAll("[data-language-toggle]");
    const voiceButtons = document.querySelectorAll("[data-voice-input]");

    langButtons.forEach((button) => {
        button.addEventListener("click", () =>
            setLanguage(button.dataset.languageToggle, {
                syncServer: true,
                reloadDynamicPages: true,
            })
        );
    });

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        voiceButtons.forEach((voiceButton) => {
            voiceButton.disabled = true;
            voiceButton.title = translate("common.voice-unsupported");
        });
        return;
    }

    let recognition = null;
    let isListening = false;

    function syncVoiceButtons(label) {
        voiceButtons.forEach((voiceButton) => {
            voiceButton.textContent = label;
            voiceButton.classList.toggle("is-listening", isListening);
            voiceButton.setAttribute("aria-pressed", isListening ? "true" : "false");
        });
    }

    function buildRecognition() {
        const nextRecognition = new SpeechRecognition();
        nextRecognition.lang = getCurrentLang() === "en" ? "en-US" : "ko-KR";
        nextRecognition.interimResults = false;
        nextRecognition.maxAlternatives = 1;
        nextRecognition.continuous = false;

        nextRecognition.onstart = () => {
            isListening = true;
            syncVoiceButtons(translate("common.listening"));
        };

        nextRecognition.onend = () => {
            isListening = false;
            syncVoiceButtons(translate("common.voice"));
        };

        nextRecognition.onresult = (event) => {
            const transcript = event.results?.[0]?.[0]?.transcript?.trim();
            const input = document.querySelector("#chat-question");
            if (transcript && input) {
                input.value = transcript;
                input.focus();
            }
            nextRecognition.stop();
        };

        nextRecognition.onerror = (event) => {
            const errorCode = event?.error || "unknown";
            const errorMap = {
                "not-allowed": "common.voice-not-allowed",
                "service-not-allowed": "common.voice-service-not-allowed",
                "no-speech": "common.voice-no-speech",
                "audio-capture": "common.voice-audio-capture",
                "network": "common.voice-network",
            };
            window.alert(translate(errorMap[errorCode] || "common.voice-fallback-error"));
        };

        return nextRecognition;
    }

    syncVoiceButtons(translate("common.voice"));

    voiceButtons.forEach((voiceButton) => {
        voiceButton.addEventListener("click", () => {
            if (isListening && recognition) {
                recognition.stop();
                return;
            }

            recognition = buildRecognition();
            try {
                recognition.start();
            } catch (error) {
                isListening = false;
                syncVoiceButtons(translate("common.voice"));
                window.alert(translate("common.voice-start-error"));
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initDeviceSelection();
    initChat();
    initHomeResetLink();
    initLandingTools();
    setLanguage(getCurrentLang(), {
        syncServer: false,
        reloadDynamicPages: false,
    });
});
