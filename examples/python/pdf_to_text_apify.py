"""PDF to text with OCR: extract the text of PDFs and scanned images by URL, page by page.

Runs the "PDF to Text & OCR" Actor on Apify and prints the text of each document.
Setup:  pip install -r requirements.txt  and  export APIFY_TOKEN=<your Apify API token>
Usage:  python pdf_to_text_apify.py https://example.com/report.pdf [more URLs...]
"""

import os
import sys

from apify_client import ApifyClient

ACTOR = "erdnal_api/erdnal-documents-text-extraction"
SAMPLE = "https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf"


def pdf_to_text(urls: list[str], languages: list[str] | None = None) -> list[dict]:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(
        logger=None,  # don't stream the run log
        run_input={
            "documentUrls": urls,
            "mode": "auto",  # text layer when present, OCR only for scanned pages
            "languages": languages or ["eng"],
        },
    )
    return list(client.dataset(run.default_dataset_id).iterate_items())


if __name__ == "__main__":
    for doc in pdf_to_text(sys.argv[1:] or [SAMPLE]):
        if not doc["ok"]:
            print(f"{doc['documentUrl']}: failed ({doc['errorCode']}), not charged")
            continue
        print(f"== {doc['documentUrl']}: {doc['pagesProcessed']} pages, {doc['ocrPages']} by OCR")
        for page in doc["pages"]:
            print(f"-- page {page['page']} ({page['method']}, confidence {page['confidence']})")
            print(page["text"])
