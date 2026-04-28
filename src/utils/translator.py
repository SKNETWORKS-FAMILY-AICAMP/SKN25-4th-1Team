from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")


@lru_cache(maxsize=512)
def translate_to_korean(text: str, source_lang: str) -> str:
    """
    Translate foreign-language input into Korean for the existing RAG flow.
    """
    if not text or source_lang == "korean":
        return text

    prompt = (
        "Translate the following user message into natural Korean. "
        "Return only the translated Korean text.\n"
        f"Text: {text}\n"
        "Korean:"
    )
    return llm.invoke(prompt).content.strip()


@lru_cache(maxsize=1024)
def translate_to_language(text: str, target_lang: str) -> str:
    """
    Translate Korean output into the target language.
    """
    if not text or target_lang == "korean":
        return text

    prompt = (
        f"Translate the following Korean customer-support answer into natural {target_lang}. "
        "Return only the translated text.\n"
        f"Text: {text}\n"
        "Translation:"
    )
    return llm.invoke(prompt).content.strip()
