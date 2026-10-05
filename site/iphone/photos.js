'use strict';
const button=document.querySelector('#save');
const status=document.querySelector('#status');
let files=[];
let loading=false;
async function prepare(){
  if(loading)return;
  loading=true;button.disabled=true;button.textContent='Loading images…';files=[];
  try{
    const response=await fetch('images.json');
    if(!response.ok)throw new Error('Manifest unavailable');
    const entries=await response.json();
    const gallery=document.querySelector('#gallery');gallery.replaceChildren();
    for(const entry of entries){
      const figure=document.createElement('figure');
      const caption=document.createElement('figcaption');caption.textContent=entry.label;
      const image=document.createElement('img');image.src=entry.url;image.alt=entry.label;image.loading='lazy';image.width=1224;image.height=1584;
      figure.append(caption,image);gallery.append(figure);
    }
    let done=0;
    // All downloads finish before the tap so Safari's user gesture stays active.
    files=await Promise.all(entries.map(async entry=>{
      const response=await fetch(entry.url);
      if(!response.ok)throw new Error('Image unavailable');
      const blob=await response.blob();
      const file=new File([blob],entry.name,{type:'image/jpeg'});
      status.textContent=`Preparing images: ${++done} of ${entries.length}.`;
      return file;
    }));
    if(navigator.share&&navigator.canShare&&navigator.canShare({files})){
      button.disabled=false;button.textContent='Save all 31 images to Photos';
      status.textContent='Ready. Choose Save Images after tapping the button.';
    }else{
      button.textContent='Open this page in iPhone Safari';
      status.textContent='This browser cannot share all images together. Open the individual images below to save them.';
      document.querySelector('details').open=true;
    }
  }catch(error){
    files=[];button.disabled=false;button.textContent='Retry loading images';
    status.textContent='Could not load every image. Check your connection, then retry.';
  }finally{loading=false;}
}
button.addEventListener('click',()=>{
  if(!files.length){prepare();return;}
  // Files only: sending a URL or text can hide the Save Images action on iOS.
  navigator.share({files}).catch(error=>{
    status.textContent=error.name==='AbortError'?'Ready whenever you are. Tap to open the share sheet again.':'The share sheet could not open. Try again, or save the individual images below.';
  });
});
prepare();
