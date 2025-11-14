function chatbotToggle(){ const box=document.getElementById('chatbot-box'); box.style.display = (box.style.display==='block')?'none':'block';}
async function chatbotSend(){
  const input=document.getElementById('chatbot-input'); const text=input.value.trim(); if(!text) return;
  const messages=document.getElementById('chatbot-messages');
  messages.innerHTML += `<div class="user-msg">${escapeHtml(text)}</div>`;
  input.value=''; messages.scrollTop = messages.scrollHeight;
  try{
    const res = await fetch('/chatbot/reply/', { method:'POST', headers:{ 'Content-Type':'application/x-www-form-urlencoded', 'X-CSRFToken': getCookie('csrftoken') }, body: 'message='+encodeURIComponent(text) });
    const data = await res.json();
    messages.innerHTML += `<div class="bot-msg">${escapeHtml(data.response)}</div>`;
    messages.scrollTop = messages.scrollHeight;
  }catch(e){
    messages.innerHTML += `<div class="bot-msg">Error contacting server.</div>`;
  }
}
function escapeHtml(unsafe){ return unsafe.replace(/[&<"']/g, function(m){ return {'&':'&amp;','<':'&lt;','"':'&quot;',"'":"&#039;"}[m]; }); }
function getCookie(name){ let v=null; if(document.cookie){ const c=document.cookie.split(';'); for(let i=0;i<c.length;i++){ const pair=c[i].trim().split('='); if(pair[0]===name) v=decodeURIComponent(pair[1]); } } return v; }
