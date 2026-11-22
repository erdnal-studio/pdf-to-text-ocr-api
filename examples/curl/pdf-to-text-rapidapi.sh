#!/usr/bin/env sh
# PDF to text and OCR over REST (RapidAPI): a local file or a public URL, JSON or Markdown output.
# Usage: RAPIDAPI_KEY=<your RapidAPI key> ./pdf-to-text-rapidapi.sh [file.pdf | https://...]
set -eu
HOST="pdf-image-text-extraction-ocr.p.rapidapi.com"
SOURCE="${1:-https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf}"

case "$SOURCE" in
  https://*)
    curl -sS -X POST "https://${HOST}/v1/documents/extract-url" \
      -H "X-RapidAPI-Key: ${RAPIDAPI_KEY}" -H "X-RapidAPI-Host: ${HOST}" \
      -H "Content-Type: application/json" \
      -d "{\"document_url\": \"${SOURCE}\", \"output\": \"markdown\"}" ;;
  *)
    curl -sS -X POST "https://${HOST}/v1/documents/extract" \
      -H "X-RapidAPI-Key: ${RAPIDAPI_KEY}" -H "X-RapidAPI-Host: ${HOST}" \
      -F "file=@${SOURCE}" -F output=markdown ;;
esac
