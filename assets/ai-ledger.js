// AI Usage Ledger
// ============================================================
// How to add a new ledger entry:
// 1) Copy an existing object in AI_LEDGER below and paste it as a new item.
// 2) Update the fields (date, model, affected, summary, transcriptHref).
// 3) Create a matching transcript page by copying:
//      pages/transcripts/_template.html
//    and saving it as the path you used in transcriptHref.
//
// NOTE: This file is intentionally plain JS (not JSON) so we can include comments.
const AI_LEDGER = [
  {
    date: "2026-01-08",
    model: "GPT-5.2 Thinking",
    affected: "Docs site scaffolding + Lab 1 starter pages",
    summary: "Generated initial GitHub Pages documentation scaffolding and starter content aligned to README/Lab 1.",
    transcriptHref: "transcripts/2026-01-08-docs-site.html"
  }
];
