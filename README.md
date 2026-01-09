# Website Chatbot – Relinns Technologies Assessment

This project is a console-based chatbot that answers user questions using information extracted from a given website URL.  
The chatbot scrapes website content, processes it as context, and uses a hosted large language model via Hugging Face Inference API to generate accurate, context-bound responses.

The solution is designed to demonstrate practical backend engineering skills, safe LLM integration, and clean system design without unnecessary complexity.

---

## Key Features

- Console-based chatbot (no frontend required)
- Website content extraction using web scraping
- Context-aware question answering
- Hosted LLM inference (no local model downloads)
- Secure API token handling (no hardcoded secrets)
- Low hallucination via constrained prompting
- Simple in-memory caching for performance optimization
- Model-agnostic architecture (easy to switch models)

---

## Technology Stack

- **Language:** Python 3
- **Libraries:**
  - `requests` – HTTP requests
  - `beautifulsoup4` – Web scraping
  - `huggingface_hub` – Hosted LLM inference

---

## High-Level Workflow

1. User provides a website URL.
2. The application scrapes headings and paragraphs from the website.
3. Extracted content is cleaned and limited to a safe context size.
4. User questions are sent along with the website context to an instruction-tuned language model.
5. The chatbot generates answers strictly based on the website content.
6. Repeated questions are served from cache to reduce API calls.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd rellins-chatbot
2. Install dependencies
bash
Copy code
pip install requests beautifulsoup4 huggingface_hub
3. Provide Hugging Face Access Token
The application requires a Hugging Face access token for inference.

You can provide the token in either of the following ways:

Option A: Environment Variable (Recommended)
Windows

bat
Copy code
setx HUGGINGFACEHUB_API_TOKEN "hf_********"
Linux / macOS

bash
Copy code
export HUGGINGFACEHUB_API_TOKEN="hf_********"
Option B: Interactive Input
If the environment variable is not set, the program will prompt you to enter the token during execution.

4. Run the application
bash
Copy code
python chatbot.py
Usage
Enter a website URL when prompted
(Press Enter to use the default: https://botpenguin.com/)

Ask questions related to the website content

Type exit or quit to end the session

Model Information
The default model used is:

HuggingFaceH4/zephyr-7b-beta

This model was chosen for strong instruction-following and better handling of longer website content.

The implementation is model-agnostic and can be switched to lighter models (e.g., google/flan-t5-base) without code changes if required.

Notes
The chatbot answers strictly from website content and avoids external knowledge.

If information is not present on the website, the chatbot responds with:

"Information not available on the website."

This project is intended for assessment and demonstration purposes.

Author
Hanumanthu Nani



---