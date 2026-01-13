// Renders AI_LEDGER into the AI Usage table.
// If you add fields to AI_LEDGER objects, update the renderer here.
(function(){
  function esc(s){
    return String(s).replace(/[&<>\"']/g, function(c){
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]);
    });
  }

  function render(){
    if(typeof AI_LEDGER === "undefined"){ return; }
    var tbody = document.getElementById("ledgerBody");
    if(!tbody){ return; }

    tbody.innerHTML = "";
    AI_LEDGER.forEach(function(row){
      var tr = document.createElement("tr");

      function tdText(v){
        var td = document.createElement("td");
        td.innerHTML = esc(v);
        return td;
      }

      tr.appendChild(tdText(row.date || ""));
      tr.appendChild(tdText(row.model || ""));
      tr.appendChild(tdText(row.affected || ""));
      tr.appendChild(tdText(row.summary || ""));

      var tdLink = document.createElement("td");
      if(row.transcriptHref){
        var a = document.createElement("a");
        a.href = row.transcriptHref;
        a.textContent = "View";
        tdLink.appendChild(a);
      }else{
        tdLink.textContent = "";
      }
      tr.appendChild(tdLink);

      tbody.appendChild(tr);
    });
  }

  document.addEventListener("DOMContentLoaded", render);
})();
