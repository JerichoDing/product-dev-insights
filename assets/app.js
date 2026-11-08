'use strict';
(() => {
 const cards=[...document.querySelectorAll('.case')];
 const fields=['search','topic','author','stage'].map(id=>document.getElementById(id));
 const storageKey='product-dev-insights:checklist:v1';
 const checks=[...document.querySelectorAll('[data-task]')];
 let saved={};
 try { saved=JSON.parse(localStorage.getItem(storageKey)||'{}')||{}; } catch { saved={}; }
 function filter(){
  const [query,topic,author,stage]=fields.map(x=>x.value.trim());
  const words=query.toLocaleLowerCase().split(/\s+/).filter(Boolean);
  let count=0;
  for(const card of cards){
   const visible=words.every(w=>card.textContent.toLocaleLowerCase().includes(w))&&(!topic||card.dataset.topic===topic)&&(!author||card.dataset.author===author)&&(!stage||card.dataset.stage===stage);
   card.hidden=!visible;if(visible)count++;
  }
  document.getElementById('result-count').textContent=`显示 ${count} / ${cards.length} 篇经验`;
  document.getElementById('empty').hidden=count>0;
 }
 fields.forEach(x=>x.addEventListener(x.type==='search'?'input':'change',filter));
 document.getElementById('reset').addEventListener('click',()=>{fields.forEach(x=>x.value='');filter();});
 function progress(){document.getElementById('progress').textContent=`已完成 ${checks.filter(x=>x.checked).length} / ${checks.length}`;}
 checks.forEach(x=>{x.checked=saved[x.dataset.task]===true;x.addEventListener('change',()=>{saved[x.dataset.task]=x.checked;try{localStorage.setItem(storageKey,JSON.stringify(saved));}catch{/* private mode / quota: still works in memory */}progress();});});
 document.getElementById('export').addEventListener('click',()=>{
  const list=cards.filter(x=>!x.hidden).map(x=>({title:x.querySelector('h3').textContent,author:x.dataset.author,stage:x.dataset.stage,url:x.querySelector('.source').href}));
  const content=JSON.stringify({title:'中文产品开发经验 · 当前阅读清单',saved_at:new Date().toISOString(),items:list},null,2);
  const url=URL.createObjectURL(new Blob([content],{type:'application/json;charset=utf-8'}));
  const link=document.createElement('a');link.href=url;link.download='product-dev-reading-list.json';document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
 });
 filter();progress();
})();
