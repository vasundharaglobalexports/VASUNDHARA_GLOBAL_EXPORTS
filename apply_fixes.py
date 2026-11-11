from pathlib import Path
import re, shutil
root=Path('/mnt/data/vge_mobile_fix')
htmls=list(root.glob('*.html'))

# 1) Rename process page to export-process.html
old=root/'process.html'; new=root/'export-process.html'
if old.exists():
    if new.exists(): new.unlink()
    old.rename(new)

# 2) Update process filename and menu label everywhere
htmls=list(root.glob('*.html'))
for p in htmls:
    s=p.read_text(encoding='utf-8', errors='ignore')
    s=s.replace('process.html','export-process.html')
    # Only visible nav/menu labels tied to export-process href
    s=re.sub(r'(<a[^>]+href=["\']export-process\.html["\'][^>]*>)\s*Process\s*(</a>)', r'\1Export Process\2', s, flags=re.I)
    p.write_text(s,encoding='utf-8')

# 3) Robust final mobile header/menu lock: same geometry across pages, no overlaps; clickable links
mobile_css=r'''
<style id="vge-mobile-header-unified-final">
/* FINAL mobile header lock: shared by Home, About, Granite Collection and all standalone pages. */
@media (max-width:767px){
  .premium-header{position:sticky!important;top:0!important;z-index:5000!important;width:100%!important;height:88px!important;min-height:88px!important;background:#fff!important;box-shadow:0 1px 0 #ece7de!important;overflow:visible!important}
  .premium-header .premium-nav{position:relative!important;width:100%!important;max-width:none!important;height:88px!important;min-height:88px!important;margin:0!important;padding:0 9px!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:6px!important;overflow:visible!important}
  .premium-brand{display:flex!important;align-items:center!important;gap:5px!important;min-width:0!important;max-width:calc(100% - 132px)!important;flex:1 1 auto!important;margin:0!important;padding:0!important;position:relative!important;left:auto!important;transform:none!important}
  .premium-brand img{display:block!important;width:64px!important;height:50px!important;max-width:64px!important;flex:0 0 64px!important;object-fit:contain!important;margin:0!important;padding:0!important;border:0!important}
  .premium-brand-copy{display:block!important;min-width:0!important;max-width:92px!important;flex:0 1 92px!important;margin:0!important;padding:0!important;overflow:visible!important}
  .premium-brand-copy strong,.premium-brand-copy strong.vge-mobile-brand-name{display:block!important;font-family:Arial,Helvetica,sans-serif!important;font-size:0!important;line-height:1.03!important;font-weight:900!important;letter-spacing:-.2px!important;color:#101820!important;white-space:normal!important;overflow:visible!important}
  .premium-brand-copy strong::before{content:"VASUNDHARA\A GLOBAL EXPORTS"!important;white-space:pre!important;display:block!important;font:900 11px/1.03 Arial,Helvetica,sans-serif!important;letter-spacing:-.2px!important;color:#101820!important}
  .premium-brand-copy small{display:none!important}

  .premium-header .premium-nav-links{position:fixed!important;top:88px!important;right:0!important;left:auto!important;width:min(78vw,340px)!important;height:calc(100dvh - 88px)!important;margin:0!important;padding:20px 18px 28px!important;display:flex!important;flex-direction:column!important;align-items:stretch!important;justify-content:flex-start!important;gap:0!important;background:#06111b!important;color:#fff!important;overflow-y:auto!important;transform:translateX(105%)!important;transition:transform .22s ease!important;z-index:5002!important;box-shadow:-18px 0 35px rgba(0,0,0,.18)!important;pointer-events:none!important}
  .premium-header .premium-nav-links.is-open{transform:translateX(0)!important;pointer-events:auto!important}
  .premium-header .premium-nav-links>a.site-flow-link{display:block!important;width:100%!important;min-height:54px!important;padding:16px 10px!important;border-bottom:1px solid rgba(255,255,255,.08)!important;color:#e9edf2!important;font:800 16px/1.25 Arial,Helvetica,sans-serif!important;white-space:normal!important;pointer-events:auto!important;position:relative!important;z-index:5004!important}
  .premium-header .premium-nav-links>a.site-flow-link.active{color:#d6a329!important;border-bottom:3px solid #b68a22!important}
  .premium-header .premium-nav-links>.vge-language-wrap{display:none!important}
  .premium-header .premium-nav-links>.request-quotation-btn{display:flex!important;align-items:center!important;justify-content:center!important;width:100%!important;min-height:54px!important;margin-top:18px!important;padding:13px 10px!important;border-radius:10px!important;background:#b58a2e!important;color:#101820!important;font:900 15px/1.2 Arial,Helvetica,sans-serif!important;pointer-events:auto!important;position:relative!important;z-index:5004!important}

  .vge-mobile-controls{position:static!important;display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:8px!important;width:124px!important;min-width:124px!important;max-width:124px!important;height:46px!important;margin:0!important;padding:0!important;flex:0 0 124px!important;background:transparent!important;border:0!important;z-index:5005!important}
  .vge-mobile-language{display:block!important;width:74px!important;height:44px!important;flex:0 0 74px!important;margin:0!important;padding:0!important;order:1!important}
  .vge-mobile-language select{display:block!important;width:74px!important;height:44px!important;margin:0!important;padding:0 17px 0 8px!important;border:1px solid #c99436!important;border-radius:10px!important;background:#fff!important;color:#101820!important;font:800 10.5px/44px Arial,Helvetica,sans-serif!important;appearance:auto!important}
  .vge-mobile-menu-toggle{position:relative!important;display:flex!important;align-items:center!important;justify-content:center!important;width:42px!important;height:42px!important;min-width:42px!important;max-width:42px!important;flex:0 0 42px!important;margin:0!important;padding:0!important;border:1px solid #c99436!important;border-radius:10px!important;background:#081624!important;color:#fff!important;order:2!important;z-index:5006!important}
  .vge-mobile-menu-toggle span,.vge-mobile-menu-toggle:before,.vge-mobile-menu-toggle:after{content:""!important;position:absolute!important;left:50%!important;width:22px!important;height:3px!important;margin-left:-11px!important;border-radius:3px!important;background:#fff!important;transition:.2s ease!important}
  .vge-mobile-menu-toggle span{top:50%!important;margin-top:-1.5px!important}
  .vge-mobile-menu-toggle:before{top:calc(50% - 8px)!important}
  .vge-mobile-menu-toggle:after{top:calc(50% + 5px)!important}
  .vge-mobile-menu-toggle.is-open span{opacity:0!important}
  .vge-mobile-menu-toggle.is-open:before{top:50%!important;transform:rotate(45deg)!important}
  .vge-mobile-menu-toggle.is-open:after{top:50%!important;transform:rotate(-45deg)!important}
  body.vge-menu-open{overflow:hidden!important}
  body.vge-menu-open:after{content:""!important;position:fixed!important;inset:88px 0 0!important;background:rgba(0,0,0,.38)!important;z-index:5001!important}
}
@media (max-width:360px){
  .premium-header .premium-nav{padding:0 6px!important;gap:4px!important}
  .premium-brand{max-width:calc(100% - 116px)!important;gap:3px!important}
  .premium-brand img{width:57px!important;height:46px!important;max-width:57px!important;flex-basis:57px!important}
  .premium-brand-copy{max-width:84px!important;flex-basis:84px!important}
  .premium-brand-copy strong::before{font-size:9.7px!important}
  .vge-mobile-controls{width:112px!important;min-width:112px!important;max-width:112px!important;flex-basis:112px!important;gap:6px!important}
  .vge-mobile-language,.vge-mobile-language select{width:66px!important;flex-basis:66px!important}
  .vge-mobile-language select{font-size:9.4px!important;padding-left:6px!important}
  .vge-mobile-menu-toggle{width:40px!important;height:40px!important;min-width:40px!important;max-width:40px!important;flex-basis:40px!important}
}
</style>
'''

mobile_js=r'''
<script id="vge-mobile-menu-navigation-final">
(function(){
  function boot(){
    var nav=document.querySelector('.premium-header .premium-nav');
    var links=document.querySelector('.premium-header .premium-nav-links');
    var sourceSelect=document.querySelector('.premium-header .vge-language-select');
    if(!nav||!links) return;
    var controls=nav.querySelector('.vge-mobile-controls');
    if(!controls && sourceSelect){
      controls=document.createElement('div'); controls.className='vge-mobile-controls';
      var lang=document.createElement('div'); lang.className='vge-mobile-language';
      var clone=sourceSelect.cloneNode(true); clone.removeAttribute('id'); clone.setAttribute('aria-label','Choose website language');
      lang.appendChild(clone);
      var toggle=document.createElement('button'); toggle.type='button'; toggle.className='vge-mobile-menu-toggle'; toggle.setAttribute('aria-label','Open navigation menu'); toggle.setAttribute('aria-expanded','false'); toggle.innerHTML='<span></span>';
      controls.appendChild(lang); controls.appendChild(toggle); nav.appendChild(controls);
      clone.addEventListener('change',function(){sourceSelect.value=clone.value;sourceSelect.dispatchEvent(new Event('change',{bubbles:true}));});
      sourceSelect.addEventListener('change',function(){clone.value=sourceSelect.value;});
    }
    if(!controls) return;
    var toggle=controls.querySelector('.vge-mobile-menu-toggle');
    if(!toggle) return;
    function closeMenu(){links.classList.remove('is-open');toggle.classList.remove('is-open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open navigation menu');document.body.classList.remove('vge-menu-open');}
    function openMenu(){links.classList.add('is-open');toggle.classList.add('is-open');toggle.setAttribute('aria-expanded','true');toggle.setAttribute('aria-label','Close navigation menu');document.body.classList.add('vge-menu-open');}
    toggle.onclick=function(e){e.preventDefault();e.stopPropagation();links.classList.contains('is-open')?closeMenu():openMenu();};
    links.querySelectorAll('a[href]').forEach(function(a){
      a.addEventListener('click',function(e){
        var href=a.getAttribute('href');
        closeMenu();
        if(!href || href==='#') return;
        // Force reliable same-site navigation on mobile/GitHub Pages.
        e.preventDefault();
        setTimeout(function(){window.location.href=href;},10);
      });
    });
    document.addEventListener('click',function(e){if(links.classList.contains('is-open')&&!links.contains(e.target)&&!controls.contains(e.target)) closeMenu();});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
})();
</script>
'''

for p in list(root.glob('*.html')):
    s=p.read_text(encoding='utf-8',errors='ignore')
    # Avoid duplicates on reruns
    s=re.sub(r'<style id="vge-mobile-header-unified-final">.*?</style>\s*','',s,flags=re.S)
    s=re.sub(r'<script id="vge-mobile-menu-navigation-final">.*?</script>\s*','',s,flags=re.S)
    # append before closing body so final CSS wins
    insert=mobile_css+mobile_js
    s=s.replace('</body>',insert+'\n</body>')
    p.write_text(s,encoding='utf-8')

# 4) Granite Collection: mobile 6 featured cards horizontal swipe, like index
p=root/'granite-collection.html'
s=p.read_text(encoding='utf-8',errors='ignore')
s=re.sub(r'<style id="vge-featured-mobile-horizontal-final">.*?</style>\s*','',s,flags=re.S)
feat_css=r'''
<style id="vge-featured-mobile-horizontal-final">
/* Mobile: the six featured granite cards swipe horizontally, matching the Home collection behavior. */
@media (max-width:640px){
  .vge-featured-start{padding:42px 0 38px!important;overflow:hidden!important}
  .vge-featured-start .vge-featured-container{width:100%!important;max-width:none!important;padding:0 18px!important;box-sizing:border-box!important}
  .vge-featured-start .vge-featured-head{text-align:left!important;margin:0 0 24px!important}
  .vge-featured-start .vge-featured-eyebrow{font-size:11px!important;letter-spacing:.14em!important;margin-bottom:8px!important}
  .vge-featured-start h1{font-size:30px!important;line-height:1.08!important;margin-bottom:10px!important}
  .vge-featured-start .vge-featured-head p{font-size:15px!important;line-height:1.55!important;margin:0!important}
  .vge-featured-grid{display:flex!important;grid-template-columns:none!important;gap:14px!important;overflow-x:auto!important;overflow-y:hidden!important;-webkit-overflow-scrolling:touch!important;scroll-snap-type:x mandatory!important;scroll-padding-left:18px!important;scrollbar-width:none!important;margin-left:-18px!important;margin-right:-18px!important;padding:2px 18px 22px!important}
  .vge-featured-grid::-webkit-scrollbar{display:none!important}
  .vge-featured-card{flex:0 0 86%!important;width:86%!important;max-width:390px!important;min-width:0!important;scroll-snap-align:start!important;border-radius:18px!important}
  .vge-featured-image{height:190px!important;min-height:190px!important}
  .vge-featured-content{padding:17px!important}
  .vge-featured-content h2{font-size:21px!important;line-height:1.16!important}
  .vge-featured-content p{font-size:14px!important;line-height:1.5!important}
  .vge-featured-view-btn{min-height:46px!important;margin-top:14px!important}
}
</style>
'''
s=s.replace('</body>',feat_css+'\n</body>')
p.write_text(s,encoding='utf-8')

# 5) Sitemap URLs update process -> export-process and ensure all 7 pages included
site=root/'sitemap.xml'
if site.exists():
    text=site.read_text(encoding='utf-8',errors='ignore').replace('/process.html','/export-process.html')
    site.write_text(text,encoding='utf-8')

# 6) redirects: legacy process path points to export-process; legacy catalogue retained redirect
redir=root/'_redirects'
lines=[]
if redir.exists():
    lines=[ln for ln in redir.read_text(encoding='utf-8',errors='ignore').splitlines() if '/process.html' not in ln]
lines.append('/process.html /export-process.html 301')
redir.write_text('\n'.join(lines).strip()+'\n',encoding='utf-8')

print('done')
