/* 加入主畫面教學動畫：播一次，播完顯示「重新播放」；點步驟可跳到該步並暫停 */
(function(){
  document.querySelectorAll('.a2hs').forEach(function(root){
    if(root.dataset.ready) return; root.dataset.ready='1';
    var f=root.querySelector('.finger'), scr=root.querySelector('.scr');
    var plan=JSON.parse(root.dataset.plan), last=Math.max.apply(null,Object.keys(plan).map(Number));
    var s=1, timer=null, ptimer=null, playing=true, btn=root.querySelector('[data-a2="toggle"]');
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    function pointAt(k){
      var el=k&&root.querySelector('[data-k="'+k+'"]');
      if(!el){f.style.opacity=0;return}
      var a=el.getBoundingClientRect(), b=scr.getBoundingClientRect();
      f.style.left=(a.left-b.left+a.width/2-13)+'px'; f.style.top=(a.top-b.top+a.height/2-13)+'px'; f.style.opacity=1;
      setTimeout(function(){f.classList.remove('tap');void f.offsetWidth;f.classList.add('tap');el.classList.remove('hl');void el.offsetWidth;el.classList.add('hl')},650);
    }
    function setBtn(){btn.textContent=root.classList.contains('ended')?'▶ 重新播放':(playing?'暫停':'▶ 繼續播放')}
    function go(n){
      s=n; root.setAttribute('data-s',n); var p=plan[n];
      root.querySelectorAll('.cap li').forEach(function(li,i){li.classList.toggle('on',i===p.c)});
      clearTimeout(ptimer); ptimer=setTimeout(function(){pointAt(p.k)}, p.d);
      clearTimeout(timer);
      if(playing) timer=setTimeout(function(){ if(n>=last){ playing=false; root.classList.add('ended'); f.style.opacity=0; setBtn(); } else go(n+1); }, p.t);
    }
    function restart(){ root.classList.remove('ended'); playing=true; setBtn(); go(1); }
    root.querySelector('[data-a2="replay"]').addEventListener('click',restart);
    root.querySelectorAll('.cap li').forEach(function(li){li.addEventListener('click',function(){ root.classList.remove('ended'); playing=false; setBtn(); go(+li.dataset.go); })});
    btn.addEventListener('click',function(){
      if(root.classList.contains('ended')) return restart();
      playing=!playing; setBtn(); if(playing) go(s); else clearTimeout(timer);
    });
    if(reduce) playing=false;
    setBtn(); go(1);
  });
})();
