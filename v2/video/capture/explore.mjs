import puppeteer from 'puppeteer';
const b = await puppeteer.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', args:['--use-angle=d3d11']});
const p = await b.newPage();
await p.setViewport({width:1920,height:1080,deviceScaleFactor:1});
await p.goto('http://localhost:8767', {waitUntil:'networkidle0'});
await new Promise(r=>setTimeout(r,2500));
await p.screenshot({path:'out/explore/0-home.png'});
console.log(await p.evaluate(()=>[...document.querySelectorAll('button')].map(b=>b.id+':'+b.textContent.trim().slice(0,30)).join(' | ')));
await b.close();
