#!/usr/bin/env sh
# PDF to text with OCR in one HTTP call: runs the Actor and returns the results as JSON.
# Usage: APIFY_TOKEN=<your Apify API token> ./pdf-to-text-apify.sh [PDF or image URL]
set -eu
URL="${1:-https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf}"

curl -sS -X POST \
  "https://api.apify.com/v2/acts/erdnal_api~erdnal-documents-text-extraction/run-sync-get-dataset-items" \
  -H "Authorization: Bearer ${APIFY_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"documentUrls\": [\"${URL}\"], \"mode\": \"auto\", \"languages\": [\"eng\"]}"
