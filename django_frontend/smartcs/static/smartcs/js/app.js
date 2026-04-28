const LANG_KEY = "smartcs-lang";

const T = {
    ko: {
        "nav.faq": "FAQ",
        "nav.service-centers": "Service Centers",
        "nav.login": "Login",
        "nav.signup": "Sign Up",
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
        "search.desc": "최신순, 조회순, 제목순 정렬과 카테고리 필터를 적용한 FAQ 리스트입니다.",
        "search.keyword-placeholder": "FAQ 제목 또는 내용을 검색하세요",
        "search.all-categories": "전체 카테고리",
        "search.sort-latest": "최신순",
        "search.sort-views": "조회순",
        "search.sort-title": "제목순",
        "search.submit": "검색",
        "search.empty-title": "표시할 FAQ가 없습니다.",
        "search.empty-desc": "현재 저장소에 FAQ CSV가 없거나 조건에 맞는 결과가 없습니다.",
        "search.chat-link": "채팅으로 연결",
        "sc.eyebrow": "서비스센터 안내",
        "sc.title": "현재 위치 기준으로 가까운 서비스센터를 안내합니다.",
        "sc.desc": "좌표를 입력하면 가까운 서비스센터 결과를 확인할 수 있습니다.",
        "sc.lat-placeholder": "위도",
        "sc.lng-placeholder": "경도",
        "sc.submit": "가까운 센터 조회",
        "sc.map-placeholder": "지도 연동 전 미리보기 영역입니다.",
        "sc.nearby-title": "가까운 센터",
        "sc.nearby-desc": "조회 결과를 거리순으로 보여줍니다.",
        "sc.empty-title": "센터 정보를 불러오지 못했습니다.",
        "sc.empty-desc": "Kakao API 키 또는 네트워크 상태를 확인해주세요.",
        "login.title": "로그인",
        "login.subtitle": "Smart CS 기능을 사용하려면 로그인하세요.",
        "login.email": "이메일",
        "login.email-placeholder": "example@email.com",
        "login.password": "비밀번호",
        "login.password-placeholder": "비밀번호를 입력하세요",
        "login.submit": "로그인",
        "login.signup-link": "계정이 없으신가요? 회원가입",
        "signup.title": "회원가입",
        "signup.subtitle": "Smart CS 계정을 만들고 서비스를 이용하세요.",
        "signup.name": "이름",
        "signup.name-placeholder": "이름을 입력하세요",
        "signup.email": "이메일",
        "signup.email-placeholder": "example@email.com",
        "signup.password": "비밀번호",
        "signup.password-placeholder": "비밀번호를 입력하세요",
        "signup.confirm": "비밀번호 확인",
        "signup.confirm-placeholder": "비밀번호를 다시 입력하세요",
        "signup.submit": "회원가입",
        "signup.login-link": "이미 계정이 있으신가요? 로그인",
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
        "search.desc": "FAQ list with sorting by latest, views, and title, plus category filter.",
        "search.keyword-placeholder": "Search FAQ title or content",
        "search.all-categories": "All Categories",
        "search.sort-latest": "Latest",
        "search.sort-views": "Most Viewed",
        "search.sort-title": "By Title",
        "search.submit": "Search",
        "search.empty-title": "No FAQ found.",
        "search.empty-desc": "No FAQ CSV in the repository, or no results match the criteria.",
        "search.chat-link": "Chat about this",
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
    },
};

function applyTranslations(lang) {
    const t = T[lang] || T.ko;

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
}

function setLanguage(lang) {
    localStorage.setItem(LANG_KEY, lang);
    applyTranslations(lang);
    document.querySelectorAll("[data-language-toggle]").forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.languageToggle === lang);
    });
}

function getCurrentLang() {
    return localStorage.getItem(LANG_KEY) || "ko";
}

function postForm(url, formData) {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value || "";
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

    function getModelsFromOption(option) {
        if (!option || !option.dataset.models) {
            return [];
        }
        return option.dataset.models
            .split("||")
            .map((model) => model.trim())
            .filter(Boolean);
    }

    function renderDeviceOptions(models, preferredModel = "") {
        deviceSelect.innerHTML = "";

        if (!models.length) {
            const emptyOption = document.createElement("option");
            emptyOption.value = "선택하지 않음";
            emptyOption.textContent = "선택하지 않음";
            deviceSelect.appendChild(emptyOption);
            return;
        }

        models.forEach((model, index) => {
            const nextOption = document.createElement("option");
            nextOption.value = model;
            nextOption.textContent = model;
            if ((preferredModel && model === preferredModel) || (!preferredModel && index === 0)) {
                nextOption.selected = true;
            }
            deviceSelect.appendChild(nextOption);
        });
    }

    function syncModelsForSelectedSeries(preferredModel = "") {
        const option = seriesSelect.options[seriesSelect.selectedIndex];
        const models = getModelsFromOption(option);
        renderDeviceOptions(models, preferredModel);
    }

    const seriesOptions = Array.from(seriesSelect.options).slice(1);
    const matchedSeriesOption = seriesOptions.find((option) => getModelsFromOption(option).includes(selectedDevice));

    if (matchedSeriesOption) {
        seriesSelect.value = matchedSeriesOption.value;
        syncModelsForSelectedSeries(selectedDevice);
    } else {
        renderDeviceOptions([], "");
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

        if (answerOverride) {
            chatLog.appendChild(renderChatMessage("assistant", answerOverride));
            syncHomeChatState();
            chatLog.scrollTop = chatLog.scrollHeight;
        }

        const formData = new FormData(form);
        formData.set("question", normalizedQuestion);
        formData.set("answer_override", answerOverride);

        try {
            const payload = await postForm(form.action, formData);
            if (!answerOverride) {
                const answer = payload?.answer || "답변을 가져오지 못했습니다. 다시 시도해주세요.";
                chatLog.appendChild(renderChatMessage("assistant", answer));
                syncHomeChatState();
                chatLog.scrollTop = chatLog.scrollHeight;
            }
        } catch (error) {
            if (!answerOverride) {
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

function initLandingTools() {
    const langButtons = document.querySelectorAll("[data-language-toggle]");
    const voiceButtons = document.querySelectorAll("[data-voice-input]");

    langButtons.forEach((button) => {
        button.addEventListener("click", () => setLanguage(button.dataset.languageToggle));
    });

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        voiceButtons.forEach((voiceButton) => {
            voiceButton.disabled = true;
            voiceButton.title = "This browser does not support speech recognition.";
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

        nextRecognition.onstart = () => {
            isListening = true;
            syncVoiceButtons(getCurrentLang() === "en" ? "Listening..." : "듣는 중...");
        };

        nextRecognition.onend = () => {
            isListening = false;
            syncVoiceButtons("Voice");
        };

        nextRecognition.onresult = (event) => {
            const transcript = event.results?.[0]?.[0]?.transcript?.trim();
            const input = document.querySelector("#chat-question");
            if (transcript && input) {
                input.value = transcript;
                input.focus();
            }
        };

        nextRecognition.onerror = (event) => {
            const lang = getCurrentLang();
            const errorCode = event?.error || "unknown";
            const messages = {
                "not-allowed": lang === "en" ? "Microphone permission was denied." : "마이크 권한이 거부되었습니다.",
                "service-not-allowed": lang === "en" ? "Speech service is blocked in this browser." : "브라우저에서 음성 인식 서비스 사용이 차단되었습니다.",
                "no-speech": lang === "en" ? "No speech was detected. Please try again." : "음성이 감지되지 않았습니다. 다시 시도해주세요.",
                "audio-capture": lang === "en" ? "No microphone was found." : "사용 가능한 마이크를 찾지 못했습니다.",
                "network": lang === "en" ? "Speech recognition network error occurred." : "음성 인식 네트워크 오류가 발생했습니다.",
            };
            window.alert(messages[errorCode] || (lang === "en" ? "Could not get voice input. Please try again." : "음성 입력을 가져오지 못했습니다. 다시 시도해주세요."));
        };

        return nextRecognition;
    }

    syncVoiceButtons("Voice");

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
                syncVoiceButtons("Voice");
                window.alert(getCurrentLang() === "en" ? "Could not start speech recognition." : "음성 인식을 시작하지 못했습니다.");
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    initDeviceSelection();
    initChat();
    initLandingTools();
    setLanguage(getCurrentLang());
});
