// PDF to text with OCR in Node.js: extract the text of PDFs and scanned images by URL, page by page.
// Setup:  npm install  and  export APIFY_TOKEN=<your Apify API token>
// Usage:  node pdf-to-text.mjs https://example.com/report.pdf [more URLs...]
import { ApifyClient } from 'apify-client';

const ACTOR = 'erdnal_api/erdnal-documents-text-extraction';
const SAMPLE = 'https://api.erdnal.com/v1/documents/samples/demo-invoice.pdf';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const urls = process.argv.length > 2 ? process.argv.slice(2) : [SAMPLE];

const run = await client.actor(ACTOR).call({
    documentUrls: urls,
    mode: 'auto', // text layer when present, OCR only for scanned pages
    languages: ['eng'],
    includeMarkdown: true, // optional: one "## Page N" section per page, for LLM and RAG
}, { log: null }); // don't stream the run log
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const doc of items) {
    if (!doc.ok) {
        console.log(`${doc.documentUrl}: failed (${doc.errorCode}), not charged`);
        continue;
    }
    console.log(`== ${doc.documentUrl}: ${doc.pagesProcessed} pages, ${doc.ocrPages} by OCR`);
    console.log(doc.markdown);
}
