// assets/ai-ledger.js
// AI Usage Ledger Entries
// ---------------------------------------------------------
// To add a new row:
// 1) Copy/paste an existing object inside AI_LEDGER and edit it.
// 2) Create a new transcript page in pages/transcripts/ using _template.html.
// 3) Set transcriptHref to the new transcript page path.
//
const AI_LEDGER = [
  {
    date: "2026-01-08",
    model: "GPT-5.2 Thinking",
    affected: "Documentation site scaffolding",
    summary: "Built the initial docs site structure, styling, and starter pages aligned to the repo source files.",
    transcriptHref: "transcripts/2026-01-08-docs-site.html",
  },
];

function renderAiLedger(tableId){
  const table = document.getElementById(tableId);
  if(!table) return;

  const rows = AI_LEDGER.map((e) => {
    const a = `<a href="${e.transcriptHref}">View</a>`;
    return `
      <tr>
        <td>${e.date}</td>
        <td>${e.model}</td>
        <td>${e.affected}</td>
        <td>${e.summary}</td>
        <td>${a}</td>
      </tr>
    `;
  }).join("");

  table.querySelector("tbody").innerHTML = rows;
}
