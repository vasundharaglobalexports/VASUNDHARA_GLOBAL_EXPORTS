(function(){
  'use strict';
  const categories = Array.isArray(window.VGE_CATEGORIES) ? window.VGE_CATEGORIES : [];
  const products = Array.isArray(window.VGE_MONUMENTS) ? window.VGE_MONUMENTS : [];
  const $ = (id) => document.getElementById(id);
  const catRoot = $('vgeMnCategories'), filtersRoot = $('vgeMnFilters'), grid = $('vgeMnProductGrid');
  if (!catRoot || !filtersRoot || !grid) return;
  const q = new URLSearchParams(window.location.search);
  const categoryName = (key) => (categories.find(c=>c.key===key)||{}).name || 'Granite memorial';
  const quoteUrl = (p) => 'contact.html?product='+encodeURIComponent('Granite Monuments & Headstones')+(p?'&design='+encodeURIComponent(p.name):'')+'#request-quotation';
  const waUrl = (p) => 'https://wa.me/917899895735?text='+encodeURIComponent('Hello Vasundhara Global Exports, I am interested in '+(p ? p.name : 'granite monuments and headstones')+'. Please share quotation details.');
  let active = categories.some(c=>c.key===q.get('category')) ? q.get('category') : 'all';
  let search = '';
  function tag(t,c){const el=document.createElement(t); if(c)el.className=c;return el;}
  function text(t,c,value){const el=tag(t,c);el.textContent=value;return el;}
  function setCategory(key){active=key; search='';$('vgeMnSearch').value=''; renderFilters();renderProducts(); if (window.history && history.replaceState) {const url=new URL(window.location.href);if(active==='all')url.searchParams.delete('category');else url.searchParams.set('category',active);history.replaceState(null,'',url.toString());} $('designs').scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'start'});}
  categories.forEach((c)=>{
    const b=tag('button','vge-mn-category'); b.type='button'; b.setAttribute('aria-label','Browse '+c.name);
    const img=tag('img'); img.src=c.image; img.alt=''; img.loading='lazy'; b.append(img);
    const wrap=tag('span','vge-mn-category-copy');wrap.append(text('span','vge-mn-category-name',c.name),text('span','vge-mn-category-desc',c.description)); b.append(wrap,text('span','vge-mn-category-arrow','↗'));
    b.addEventListener('click',()=>setCategory(c.key));catRoot.append(b);
  });
  function renderFilters(){
    filtersRoot.replaceChildren();
    [{key:'all',name:'All designs'},...categories].forEach(c=>{
      const btn=text('button','',c.name);btn.type='button';btn.setAttribute('aria-pressed',String(active===c.key));
      btn.addEventListener('click',()=>setCategory(c.key));filtersRoot.append(btn);
    });
  }
  function renderProducts(){
    const s=search.trim().toLowerCase();
    const displayed=products.filter(p=>(active==='all'||p.category===active) && (!s||(p.name+' '+categoryName(p.category)).toLowerCase().includes(s)));
    grid.replaceChildren();
    const frag=document.createDocumentFragment();
    displayed.forEach((p)=>{
      const article=tag('article','vge-mn-product');
      const media=tag('button','vge-mn-product-photo');media.type='button';media.setAttribute('aria-label','View '+p.name+' details');
      const img=tag('img');img.src=p.image;img.alt=p.name+' reference design';img.loading='lazy';img.decoding='async';media.append(img); media.addEventListener('click',()=>openModal(p));
      const body=tag('div','vge-mn-product-body');body.append(text('span','vge-mn-product-type',categoryName(p.category)),text('h3','',p.name));
      const actions=tag('div','vge-mn-product-actions');const details=text('button','','View details');details.type='button';details.addEventListener('click',()=>openModal(p));const link=text('a','','Enquire ↗');link.href=quoteUrl(p);link.setAttribute('aria-label','Request a quote for '+p.name);actions.append(details,link);body.append(actions);
      article.append(media,body);frag.append(article);
    });grid.append(frag);
    $('vgeMnCount').textContent=displayed.length+' design'+(displayed.length===1?'':'s')+' displayed';
    $('vgeMnEmpty').hidden=displayed.length>0;
  }
  $('vgeMnSearch').addEventListener('input',(event)=>{search=event.target.value;renderProducts();});
  const modal=$('vgeMnModal');let lastFocused=null;
  function openModal(p){
    lastFocused=document.activeElement;
    $('vgeMnModalImage').src=p.image;$('vgeMnModalImage').alt=p.name;
    $('vgeMnModalCategory').textContent=categoryName(p.category);
    $('vgeMnModalTitle').textContent=p.name;
    $('vgeMnModalQuote').href=quoteUrl(p);$('vgeMnModalWa').href=waUrl(p);
    modal.setAttribute('aria-hidden','false');document.body.classList.add('vge-mn-modal-open');modal.focus({preventScroll:true});
  }
  function closeModal(){modal.setAttribute('aria-hidden','true');document.body.classList.remove('vge-mn-modal-open');if(lastFocused && lastFocused.isConnected)lastFocused.focus();}
  $('vgeMnModalClose').addEventListener('click',closeModal);
  modal.addEventListener('click',ev=>{if(ev.target.matches('[data-vge-mn-close]'))closeModal();});
  document.addEventListener('keydown',ev=>{
    if(modal.getAttribute('aria-hidden')==='true')return;
    if(ev.key==='Escape')closeModal();
    if(ev.key==='Tab'){
      const els=[...modal.querySelectorAll('button:not([disabled]),a[href]')].filter(el=>el.getClientRects().length);
      if(!els.length)return;
      if(ev.shiftKey && document.activeElement===els[0]){ev.preventDefault();els[els.length-1].focus();}
      else if(!ev.shiftKey && document.activeElement===els[els.length-1]){ev.preventDefault();els[0].focus();}
    }
  });
  renderFilters();renderProducts();
})();
