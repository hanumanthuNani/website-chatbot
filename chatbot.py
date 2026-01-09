import os
import requests
from bs4 import BeautifulSoup
from huggingface_hub import InferenceClient

# =====================================================
# CONFIGURATION
# =====================================================

# Primary model (strong instruction-following)
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"

MAX_CONTEXT_CHARS = 3500

# Secure token handling:
# 1. Try environment variable
# 2. Fallback to user input (console demo friendly)
HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

if not HF_TOKEN:
    print("[System] HUGGINGFACEHUB_API_TOKEN not found in environment.")
    HF_TOKEN = input("Please enter your Hugging Face Access Token: ").strip()

if not HF_TOKEN:
    print("[Error] No API token provided. Exiting.")
    exit(1)

# Initialize Hugging Face Inference Client (server-side inference)
client = InferenceClient(
    model=MODEL_ID,
    token=HF_TOKEN
)

# Simple in-memory cache to reduce repeated inference calls
answer_cache = {}

# =====================================================
# WEB SCRAPER
# =====================================================

def fetch_website_text(url: str) -> str | None:
    """
    Fetches and cleans visible text from a website.
    Only extracts meaningful headings and paragraphs.
    """
    print(f"\n[System] Scraping content from: {url}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        texts = []
        for tag in soup.find_all(["h1", "h2", "h3", "p"]):
            text = tag.get_text(strip=True)
            if len(text) > 30:
                texts.append(text)

        combined_text = " ".join(texts)
        return combined_text[:MAX_CONTEXT_CHARS]

    except Exception as e:
        print(f"[Error] Failed to scrape website: {e}")
        return None

# =====================================================
# LLM INTERACTION
# =====================================================

def get_answer_from_llm(context: str, question: str) -> str:
    """
    Sends website context and user question to the LLM
    using chat-completion format for better instruction following.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI assistant answering questions strictly using "
                "the provided website content.\n\n"
                "Rules:\n"
                "- Use ONLY the website content.\n"
                "- If the answer is not present, reply exactly:\n"
                "  'Information not available on the website.'\n"
                "- Be concise and factual.\n\n"
                f"WEBSITE CONTENT:\n{context}"
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat_completion(
        messages=messages,
        max_tokens=250,
        temperature=0.1
    )

    return response.choices[0].message.content.strip()

# =====================================================
# MAIN APPLICATION
# =====================================================

def main():
    print("=== Relinns Technologies | Website Chatbot Assessment ===\n")

    url = input("Enter website URL (Press Enter for https://botpenguin.com/): ").strip()
    if not url:
        url = "https://botpenguin.com/"

    context = fetch_website_text(url)

    if not context:
        print("[System] No content extracted. Please check the URL.")
        return

    print("[System] Website loaded successfully.")
    print("[System] Type 'exit' to quit.\n")

    while True:
        question = input("User: ").strip()

        if not question:
            continue

        if question.lower() in ("exit", "quit", "bye"):
            print("[System] Session ended.")
            break

        cache_key = question.lower().strip()
        if cache_key in answer_cache:
            print(f"Chatbot (Cached): {answer_cache[cache_key]}\n")
            continue

        try:
            print("Processing your question...")
            answer = get_answer_from_llm(context, question)
            answer_cache[cache_key] = answer
            print(f"Chatbot: {answer}\n")

        except Exception as e:
            print(f"[Error] Inference failed: {e}")

# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    main()
