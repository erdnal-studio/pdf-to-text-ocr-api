# PDF to Text API & OCR: Python, Node.js, cURL, n8n and MCP examples

Extract text from PDFs, scanned documents and images (image to text OCR) by URL or file upload, page by page, as
**JSON, plain text or Markdown** for LLMs and RAG. Copy-paste examples for the
[PDF to Text & OCR API](https://apify.com/erdnal_api/erdnal-documents-text-extraction) by Erdnal, usable from the
Apify API, a plain REST API on RapidAPI, n8n, Make, Zapier and AI agents (MCP).

- **Text layer first, OCR only when needed:** digital PDF pages are read from their text layer (fast and exact);
  only scanned pages and images go through OCR (Tesseract). Cheaper and more accurate than OCR on every page.
- **PDF to Markdown for LLM and RAG:** one `## Page N` section per page, ready to chunk and embed.
- **Scanned PDF and image to text:** JPEG and PNG, 7 OCR languages (English, French, German, Spanish, Italian,
  Portuguese, Dutch), with a confidence score per page.
- **Invoice to JSON:** optional structured invoice and receipt data (number, dates, supplier, VAT, totals, lines).
- **Pay per page, failures free:** $0.50 per 1,000 text pages, $2 per 1,000 OCR pages. EU-hosted, documents not kept.

## Contents

- [Quick start (Python)](#quick-start-python)
- [Node.js](#nodejs)
- [cURL, one HTTP call](#curl-one-http-call)
- [PDF to Markdown for LLM and RAG](#pdf-to-markdown-for-llm-and-rag)
- [Scanned PDF and image to text (OCR)](#scanned-pdf-and-image-to-text-ocr)
- [REST API on RapidAPI (file upload)](#rest-api-on-rapidapi-file-upload)
- [n8n, Make and Zapier](#n8n-make-and-zapier)
- [AI agents: Claude, Cursor, VS Code (MCP)](#ai-agents-claude-cursor-vs-code-mcp)
- [Output](#output)
- [Pricing](#pricing)
- [Limits](#limits)
- [FAQ](#faq)

## Quick start (Python)

```bash
pip install "apify-client>=3.4"
export APIFY_TOKEN=<your Apify API token>   # Apify Console > Settings > API & Integrations
python examples/python/pdf_to_text_apify.py https://example.com/report.pdf
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("erdnal_api/erdnal-documents-text-extraction").call(
    run_input={"documentUrls": ["https://example.com/report.pdf"], "mode": "auto", "languages": ["eng"]},
    logger=None,  # don't stream the run log
)
for doc in client.dataset(run.default_dataset_id).iterate_items():
    print(doc["documentUrl"], doc["pagesProcessed"], "pages")
    print(doc["text"])
```

Full script: [`examples/python/pdf_to_text_apify.py`](examples/python/pdf_to_text_apify.py).

## Node.js

```bash
cd examples/node && npm install
APIFY_TOKEN=<your Apify API token> node pdf-to-text.mjs https://example.com/report.pdf
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('erdnal_api/erdnal-documents-text-extraction').call({
    documentUrls: ['https://example.com/report.pdf'],
    mode: 'auto',
}, { log: null });
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items[0].text);
```

Full script: [`examples/node/pdf-to-text.mjs`](examples/node/pdf-to-text.mjs).

## cURL, one HTTP call

Runs the extraction and returns the results as JSON in the same request:

```bash
curl -X POST \
  "https://api.apify.com/v2/acts/erdnal_api~erdnal-documents-text-extraction/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"documentUrls": ["https://example.com/report.pdf"], "mode": "auto", "languages": ["eng"]}'
```

Script: [`examples/curl/pdf-to-text-apify.sh`](examples/curl/pdf-to-text-apify.sh).

## PDF to Markdown for LLM and RAG

Set `includeMarkdown: true` to get a `markdown` field with one `## Page N` section per page (same price). Split it
by page to keep the page number as metadata for citations:

```python
run = client.actor("erdnal_api/erdnal-documents-text-extraction").call(
    run_input={"documentUrls": [url], "includeMarkdown": True, "includePages": False}, logger=None
)
markdown = next(client.dataset(run.default_dataset_id).iterate_items())["markdown"]
```

[`examples/python/pdf_to_markdown_rag.py`](examples/python/pdf_to_markdown_rag.py) turns it into chunks
`{"text", "metadata": {"source", "page"}}` that work with LangChain, LlamaIndex or any vector store. Ready-made
preset: [PDF to Markdown for LLM & RAG](https://apify.com/erdnal_api/erdnal-documents-text-extraction/examples/pdf-to-markdown).

## Scanned PDF and image to text (OCR)

`mode: "auto"` already sends scanned pages and JPEG/PNG images to OCR. Force OCR on every page with `mode: "ocr"`,
and choose up to 3 languages:

```json
{
  "documentUrls": ["https://example.com/scan.pdf", "https://example.com/receipt.png"],
  "mode": "ocr",
  "languages": ["eng", "fra"],
  "pages": "1-5"
}
```

Each page has `method` (`text` or `ocr`) and `confidence` (0 to 1); below about 0.8, review the text. Presets:
[Scanned PDF to Text (OCR)](https://apify.com/erdnal_api/erdnal-documents-text-extraction/examples/scanned-pdf-to-text-ocr),
[Image to Text OCR](https://apify.com/erdnal_api/erdnal-documents-text-extraction/examples/image-to-text-ocr).

## REST API on RapidAPI (file upload)

The same extraction is available as a classic REST API with an API key, including **file upload** (no public URL
needed) and `output=text` or `output=markdown`. Plans, free plan included:
[PDF & Image Text Extraction (OCR) on RapidAPI](https://rapidapi.com/erdnal-erdnal-default/api/pdf-image-text-extraction-ocr).

```bash
curl -X POST "https://pdf-image-text-extraction-ocr.p.rapidapi.com/v1/documents/extract" \
  -H "X-RapidAPI-Key: $RAPIDAPI_KEY" -H "X-RapidAPI-Host: pdf-image-text-extraction-ocr.p.rapidapi.com" \
  -F file=@scan.pdf -F output=markdown
```

Python: [`examples/python/pdf_to_text_rapidapi.py`](examples/python/pdf_to_text_rapidapi.py); shell:
[`examples/curl/pdf-to-text-rapidapi.sh`](examples/curl/pdf-to-text-rapidapi.sh).

## n8n, Make and Zapier

- **n8n:** import [`n8n/pdf-to-text-ocr-workflow.json`](n8n/pdf-to-text-ocr-workflow.json) (an HTTP Request node
  calling the Apify API). Create a Header Auth credential: name `Authorization`, value `Bearer <your Apify token>`.
  The Apify node for n8n works too.
- **Make and Zapier:** use their Apify integration, Actor `erdnal_api/erdnal-documents-text-extraction`, then send
  the `text` or `markdown` field to a database, a spreadsheet or an AI step.

## AI agents: Claude, Cursor, VS Code (MCP)

AI agents can extract text from PDFs and images through the Apify MCP server. Add this server URL to your MCP
client and sign in with your Apify account when asked:

```
https://mcp.apify.com?tools=erdnal_api/erdnal-documents-text-extraction
```

Claude Desktop (via `mcp-remote`): [`mcp/claude_desktop_config.json`](mcp/claude_desktop_config.json).

## Output

One item per document:

```json
{
  "documentUrl": "https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf",
  "ok": true,
  "inputType": "pdf",
  "pagesTotal": 2,
  "pagesProcessed": 2,
  "ocrPages": 1,
  "text": "INVOICE INV-2026-0042 (SAMPLE)\nDemo Supplier Ltd, ...\n\nPAYMENT TERMS (scanned page)\n...",
  "chars": 496,
  "minConfidence": 0.962,
  "pages": [
    {"page": 1, "method": "text", "text": "INVOICE INV-2026-0042 (SAMPLE) ...", "chars": 305, "confidence": null},
    {"page": 2, "method": "ocr", "text": "PAYMENT TERMS (scanned page) ...", "chars": 191, "confidence": 0.962}
  ],
  "creditsCharged": 5,
  "errorCode": null
}
```

A failed document has `ok: false`, an `errorCode` and `creditsCharged: 0`; the run goes on with the next one.

## Pricing

| Page | Price | Per 1,000 pages |
|---|---|---|
| Read from the PDF text layer | $0.0005 | $0.50 |
| Read by OCR (scanned page, image) | $0.002 | $2 |
| Invoice data (`extract: "invoice"`), on top | +$0.0025 | +$2.50 |

Failed documents are free; Markdown and page details cost nothing extra. No subscription on Apify: you pay per page,
and Apify's free plan credits cover small tests. Details:
[pricing on Apify](https://apify.com/erdnal_api/erdnal-documents-text-extraction).

## Limits

- 20 MB per file, 200 pages per document (use `pages` for longer documents);
- 5 OCR pages per document: split long scanned PDFs with `pages` (`1-5`, `6-10`, …);
- OCR takes about 3 to 4 seconds per page;
- public `https://` URLs on Apify; file upload on the RapidAPI REST API.

## FAQ

**What is the difference between PDF to text and OCR?**
A digital PDF contains a text layer: reading it is exact and fast. A scanned PDF or a photo is only an image of
text: OCR (optical character recognition) recognises the characters. In `auto` mode this API does both, page by
page, and charges OCR only for the pages that need it.

**Can I convert a PDF to Markdown for ChatGPT, Claude or a RAG pipeline?**
Yes: `includeMarkdown: true` on Apify, or `output=markdown` on RapidAPI. Headings per page keep page numbers for
citations.

**Does it read handwriting or tables?**
It does not read handwriting. Tables come back as text in reading order, not as cells.

**Where are documents processed, and are they kept?**
In the European Union, only to produce the result. Documents and extracted text are not kept after the response
(the invoice option sends the extracted text to an AI model to structure it, nothing is stored).

**Which one should I use, Apify or RapidAPI?**
Apify for batches of URLs, n8n/Make/Zapier and AI agents, billed per page; RapidAPI for file uploads and a classic
REST API with monthly plans.

## More from Erdnal

- [Image Compression & WebP AVIF Converter](https://apify.com/erdnal_api/erdnal-media-image-optimizer): compress
  images in bulk and convert JPG/PNG to WebP or AVIF, with resizing and EXIF/GPS removal.
- [Invoice & Receipt to JSON](https://apify.com/erdnal_api/erdnal-documents-text-extraction/examples/invoice-to-json):
  invoice parser preset.

Support: support@erdnal.com. Examples under the [MIT license](LICENSE).
