"""PDF to Markdown for LLM and RAG: one "## Page N" section per page, split into chunks ready to embed.

Setup:  pip install -r requirements.txt  and  export APIFY_TOKEN=<your Apify API token>
Usage:  python pdf_to_markdown_rag.py https://example.com/report.pdf
"""

import os
import re
import sys

from apify_client import ApifyClient

ACTOR = "erdnal_api/erdnal-documents-text-extraction"
SAMPLE = "https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf"


def pdf_to_markdown(url: str) -> str:
    client = ApifyClient(os.environ["APIFY_TOKEN"])
    run = client.actor(ACTOR).call(
        logger=None,  # don't stream the run log
        run_input={"documentUrls": [url], "includeMarkdown": True, "includePages": False},
    )
    doc = next(client.dataset(run.default_dataset_id).iterate_items())
    if not doc["ok"]:
        raise RuntimeError(f"{url}: {doc['errorCode']} ({doc['errorMessage']})")
    return doc["markdown"]


def chunks_by_page(markdown: str, source: str) -> list[dict]:
    """One chunk per page, with the page number as metadata (works with any vector store)."""
    parts = re.split(r"^## Page (\d+)\n", markdown, flags=re.MULTILINE)[1:]
    return [
        {"text": text.strip(), "metadata": {"source": source, "page": int(number)}}
        for number, text in zip(parts[::2], parts[1::2], strict=True)
        if text.strip()
    ]


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else SAMPLE
    for chunk in chunks_by_page(pdf_to_markdown(url), url):
        print(chunk["metadata"], chunk["text"][:120].replace("\n", " "), "...")
    # LangChain: [Document(page_content=c["text"], metadata=c["metadata"]) for c in chunks]
