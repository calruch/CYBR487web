(function(){
  try{
    var active = window.__ACTIVE_NAV__ || "";
    var links = document.querySelectorAll("[data-nav]");
    for(var i=0;i<links.length;i++){
      var a = links[i];
      if(a.getAttribute("data-nav") === active){
        a.setAttribute("aria-current", "page");
      }
    }
  }catch(e){}
})();