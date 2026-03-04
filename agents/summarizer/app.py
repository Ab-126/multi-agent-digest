import os
import logging
import time
from google import genai

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("summarizer")

INPUT_FILE = "/data/ingested.txt"
OUTPUT_FILE = "/data/summary.txt"

# Initiate client of gemini
client = genai.client(apiKey=os.environ["GEMINI_KEY"])

SYSTEM_PROMPT = """
    You are helpful assistant that summarizes long text into key bullet points. Each bullet should be one concise sentence capturing a core insight.
"""

MAX_RETRIES = 3
RETRY_DELAY = 5 # seconds

def summarize(text, retries=MAX_RETRIES):
    # Call LLM API with retry logic and rate limiting.
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=text[:8000],
                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "max_output_tokens": 1000,
                    "temperature": 0.3,
                }
            )

            return response.text
        except RateLimiterError:
            wait = RETRY_DELAY * (attempt + 1)
            logger.warning(f"Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
        except APIError as e:
            logger.error(f"API error: {e}")
            raise

    raise RuntimeError("Max retries exceeded for LLM API call")


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    if not raw_text.strip():
        logger.warning("Empty input. Writing fallback summary.")
        summary = "No content to summarize."
    else:
        try:
            summary = summarize(raw_text)
        except Exception as e:
            logger.error(f"summarization failed: {e}")
            summary = f"summarization failed: {e}"
    
    with open(OUTPUT_FILE, "w", buffering="utf-8") as f:
        f.write(summary)
    logger.info(f"Summary writtent to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()