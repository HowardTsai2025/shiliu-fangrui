/* 加入主畫面教學動畫：播一次，播完顯示「重新播放」；點步驟可跳到該步並暫停。
   initA2HS(scope, played)：scope 內每個 .a2hs 啟動；played[種類] 為 true 時直接停在播完畫面（避免網頁重畫時一直重播）。 */
function initA2HS(scope, played){
  played=played||{};
  (scope||document).querySelectorAll('.a2hs').forEach(function(root){
    if(root.dataset.ready||(root.closest&&root.closest('details:not([open])'))) return; root.dataset.ready='1';
    var kind=root.classList.contains('and')?'and':(root.classList.contains('ipad')?'ipad':'ios');
    var f=root.querySelector('.finger'), scr=root.querySelector('.scr');
    var plan=JSON.parse(root.dataset.plan), last=Math.max.apply(null,Object.keys(plan).map(Number));
    var s=1, timer=null, ptimer=null, playing=true, btn=root.querySelector('[data-a2="toggle"]');
    var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
    function pointAt(k){
      var el=k&&root.querySelector('[data-k="'+k+'"]');
      if(!el||!root.isConnected){f.style.opacity=0;return}
      var a=el.getBoundingClientRect(), b=scr.getBoundingClientRect();
      f.style.left=(a.left-b.left+a.width/2-13)+'px'; f.style.top=(a.top-b.top+a.height/2-13)+'px'; f.style.opacity=1;
      setTimeout(function(){f.classList.remove('tap');void f.offsetWidth;f.classList.add('tap');el.classList.remove('hl');void el.offsetWidth;el.classList.add('hl')},650);
    }
    function setBtn(){btn.textContent=root.classList.contains('ended')?'▶ 重新播放':(playing?'暫停':'▶ 繼續播放')}
    function end(){ playing=false; played[kind]=true; root.classList.add('ended'); f.style.opacity=0; setBtn(); }
    function mark(n){ s=n; root.setAttribute('data-s',n); var c=plan[n].c;
      root.querySelectorAll('.cap li').forEach(function(li,i){li.classList.toggle('on',i===c)}); }
    function go(n){
      if(!root.isConnected) return;
      mark(n); var p=plan[n];
      clearTimeout(ptimer); ptimer=setTimeout(function(){pointAt(p.k)}, p.d);
      clearTimeout(timer);
      if(playing) timer=setTimeout(function(){ if(n>=last) end(); else go(n+1); }, p.t);
    }
    function restart(){ root.classList.remove('ended'); playing=true; setBtn(); go(1); }
    root.querySelector('[data-a2="replay"]').addEventListener('click',restart);
    root.querySelectorAll('.cap li').forEach(function(li){li.addEventListener('click',function(){ root.classList.remove('ended'); playing=false; setBtn(); go(+li.dataset.go); })});
    btn.addEventListener('click',function(){
      if(root.classList.contains('ended')) return restart();
      playing=!playing; setBtn(); if(playing) go(s); else clearTimeout(timer);
    });
    if(played[kind]){ mark(last); end(); return; }
    if(reduce) playing=false;
    setBtn(); go(1);
  });
}
