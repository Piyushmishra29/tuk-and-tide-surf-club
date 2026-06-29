// Puppeteer screenshot helper.
// Usage: node shot.js [desktop|mobile] [outName] [#anchor-or-empty]
let puppeteer; try{ puppeteer=require('puppeteer'); }catch(e){ puppeteer=require('puppeteer-core'); }
(async()=>{
  const mode=process.argv[2]||'desktop';
  const out=process.argv[3]||('shot_'+mode);
  const anchor=process.argv[4]||'';
  const path=require('path');
  const url='file://'+path.join(__dirname,'index.html')+'?static'+(anchor?anchor:'');
  const vp=mode==='mobile'?{width:390,height:844,deviceScaleFactor:2}:{width:1440,height:900,deviceScaleFactor:1};
  const CHROME='/Users/piyushmishra/.cache/puppeteer/chrome/mac-149.0.7827.22/chrome-mac-x64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';
  const b=await puppeteer.launch({headless:'new',executablePath:CHROME,args:['--no-sandbox','--hide-scrollbars']});
  const p=await b.newPage();
  await p.setViewport(vp);
  await p.goto(url,{waitUntil:'networkidle0',timeout:60000});
  // scroll through page to trigger lazy-loaded images, then return to top
  await p.evaluate(async()=>{ const h=document.body.scrollHeight; for(let y=0;y<=h;y+=400){ window.scrollTo(0,y); await new Promise(r=>setTimeout(r,40)); } window.scrollTo(0,0); });
  await p.evaluate(async()=>{ await Promise.all(Array.from(document.images).map(i=>i.complete?0:new Promise(r=>{i.onload=i.onerror=r;}))); });
  await new Promise(r=>setTimeout(r,900));
  if(anchor){ await p.evaluate(a=>{const el=document.querySelector(a);if(el)el.scrollIntoView();},anchor); await new Promise(r=>setTimeout(r,500)); await p.screenshot({path:__dirname+'/'+out+'.png'}); }
  else { await p.screenshot({path:__dirname+'/'+out+'.png',fullPage:true}); }
  await b.close();
  console.log('shot ->',out+'.png');
})().catch(e=>{console.error(e);process.exit(1);});
