"""PDF to text and OCR over a plain REST API (RapidAPI): upload a file or send a URL, get JSON or Markdown.

Setup:  pip install requests  and  export RAPIDAPI_KEY=<your RapidAPI key>
        (subscribe to a plan, free plan included, on
        https://rapidapi.com/erdnal-erdnal-default/api/pdf-image-text-extraction-ocr)
Usage:  python pdf_to_text_rapidapi.py scan.pdf      (local file)
        python pdf_to_text_rapidapi.py https://example.com/report.pdf
"""

import os
import sys

import requests

HOST = "pdf-image-text-extraction-ocr.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY", ""), "X-RapidAPI-Host": HOST}
SAMPLE = "https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf"


def extract(source: str, output: str = "json", languages: str = "eng") -> requests.Response:
    if source.startswith("https://"):
        return requests.post(
            f"https://{HOST}/v1/documents/extract-url",
            headers=HEADERS,
            json={"document_url": source, "output": output, "languages": languages},
            timeout=120,
        )
    with open(source, "rb") as file:
        return requests.post(
            f"https://{HOST}/v1/documents/extract",
            headers=HEADERS,
            files={"file": file},
            data={"output": output, "languages": languages},
            timeout=120,
        )


if __name__ == "__main__":
    response = extract(sys.argv[1] if len(sys.argv) > 1 else SAMPLE)
    response.raise_for_status()
    print("credits charged:", response.headers.get("X-Units-Charged"))
    for page in response.json()["pages"]:
        print(f"-- page {page['page']} ({page['method']}, confidence {page['confidence']})")
        print(page["text"])
