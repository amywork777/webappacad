import { useState } from 'react';
const API=import.meta.env.VITE_API_URL||'/api';
const send=async(p,b,f)=>fetch(API+p,{method:'POST',...(f?{body:b}:{headers:{'Content-Type':'application/json'},body:JSON.stringify(b)})});

export default function App(){
  const [txt,setTxt]=useState(''),[busy,setBusy]=useState(false);
  const go=async()=>{setBusy(true);const r=await send('/generate',{prompt:txt});window.location=URL.createObjectURL(await r.blob());setBusy(false);};
  const img=async f=>{const fd=new FormData();fd.append('file',f);fd.append('prompt',txt);const r=await send('/generate_from_image',fd,true);window.location=URL.createObjectURL(await r.blob());};
  return(<div style={{maxWidth:600,margin:'3rem auto',fontFamily:'sans-serif'}}>
    <h2>AI ↔ CAD demo</h2>
    <textarea rows="4" style={{width:'100%'}} value={txt} onChange={e=>setTxt(e.target.value)} placeholder="e.g. 120 mm bottle"/>
    <button disabled={!txt||busy} onClick={go}>{busy?'…':'Text → STEP'}</button>
    <hr/><input type="file" accept="image/*" onChange={e=>img(e.target.files[0])}/>
  </div>);
}