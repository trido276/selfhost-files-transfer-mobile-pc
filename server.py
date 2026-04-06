import os
import time
import uuid
import socket
import io

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse

import qrcode

# ================== CONFIG ==================
UPLOAD_DIR = "shared"
TOKEN_TTL_SECONDS = 300  # 5 phút
PORT = 8080
# ===========================================

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()
active_tokens = {}
last_qr_token = None

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

    
@app.get("/exists")
def file_exists(name: str):
    path = os.path.join(UPLOAD_DIR, name)
    return {"exists": os.path.exists(path)}

@app.get("/refresh")
def refresh_token():
    token = uuid.uuid4().hex
    active_tokens[token] = time.time() + TOKEN_TTL_SECONDS
    return {"token": token}

@app.get("/", response_class=HTMLResponse)
def index():
    global last_qr_token

    token = uuid.uuid4().hex
    active_tokens[token] = time.time() + TOKEN_TTL_SECONDS
    last_qr_token = token

    ip = get_local_ip()
    upload_url = f"http://{ip}:{PORT}/upload?token={token}"

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>QR Upload</title>
<style>
body {
  font-family: system-ui, sans-serif;
  text-align: center;
  padding: 20px;
}
button {
  padding: 12px 18px;
  font-size: 16px;
  margin-top: 12px;
}
.debug {
  font-size: 12px;
  color: #555;
  margin-top: 10px;
  word-break: break-all;
}
</style>
</head>
<body>

<h2>Scan QR with your phone</h2>

        <img id="qr" src="/qr" style="width:260px;height:260px"><br><br>

        <button onclick="refreshQR()" style="padding:10px 20px;font-size:16px">
            🔄 Refresh QR Code
        </button>
    
        
        <button onclick="openDebug()">🔗 Open upload page (debug)</button>

  <div class="debug">
<b>Token:</b><br>
__TOKEN__<br><br>
Valid for 5 minutes
</div>

<script>
function refreshQR() {
            fetch("/refresh")
              .then(() => {
                const img = document.getElementById("qr");
                img.src = "/qr?ts=" + new Date().getTime(); // tránh cache
              });
        }
function openDebug() {
  window.open("__UPLOAD_URL__", "_blank");
}
</script>

</body>
</html>
"""

    html = html.replace("__TOKEN__", token)
    html = html.replace("__UPLOAD_URL__", upload_url)

    return html

@app.get("/qr")
def qr_image():
    if not last_qr_token:
        raise HTTPException(status_code=404)

    url = f"http://{get_local_ip()}:{PORT}/upload?token={last_qr_token}"

    qr = qrcode.make(url)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

@app.get("/upload", response_class=HTMLResponse)
def upload_page(token: str):
    if token not in active_tokens or active_tokens[token] < time.time():
        raise HTTPException(status_code=403)

    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Multi Upload</title>
<style>
body{font-family:system-ui;background:#f2f2f2;padding:20px}
.card{background:#fff;padding:20px;border-radius:10px}
.progress{width:100%;height:10px;background:#ddd;border-radius:5px}
.bar{height:100%;width:0%;background:#4CAF50}
.file{margin-top:12px}
button{width:100%;padding:12px;font-size:16px;margin-top:10px}
small{font-size:12px}
</style>
</head>

<body>
<div class="card">
<h3>Upload files</h3>

<input type="file" id="files" multiple><br><br>

<label>
  <input type="checkbox" id="parallel"> Upload song song
</label>

<div class="progress"><div class="bar" id="totalBar"></div></div>
<small id="totalInfo"></small>

<div id="list"></div>

<button id="uploadBtn" onclick="startUpload()">Upload</button>
</div>

<script>
let TOKEN = "__TOKEN__";
let uploadedNames=new Set();
let uploading=false;
let totalUploaded=0;

function formatBytes(b) {
  const u = ["B","KB","MB","GB"];
  let i = 0;
  while (b >= 1024 && i < u.length - 1) { b /= 1024; i++; }
  return b.toFixed(2) + " " + u[i];
}

let totalSize = 0;
let uploaded = 0;
let startTime = 0;

function startUpload() {
  completed = 0;
  totalUploaded = 0;
  startTime = Date.now();
  document.getElementById('totalBar').style.width = '0%';
  document.getElementById('totalInfo').innerText = '';

    if(uploading) return;
 const input=document.getElementById("files");
 if(!input.files.length) return;

 uploading=true;
 document.getElementById("uploadBtn").disabled=true;

 const files=[...input.files].filter(f=>!uploadedNames.has(f.name));
 if(!files.length){done();return;}

 checkDuplicates(files).then(ok=>{
  completed = 0;
  totalUploaded = 0;
  startTime = Date.now();

  if(!ok){reset();return;}
  refreshToken().then(t=>{
    TOKEN=t;
    prepareAndUpload(files);
  });
 });
}

async function checkDuplicates(files) {
  for (let i = files.length - 1; i >= 0; i--) {
    const f = files[i];
    const r = await fetch("/exists?name=" + encodeURIComponent(f.name));
    const j = await r.json();

    if (j.exists) {
     if(!confirm('File '+f.name+' đã tồn tại. Ghi đè?')){
        files.splice(i, 1);
      }
      // remove file khỏi danh sách upload
    }
  }
  return true;
}


function refreshToken(){
 return fetch("/refresh").then(r=>r.json()).then(j=>j.token);
}

function prepareAndUpload(files){
  const list = document.getElementById("list");
  list.innerHTML = "";

  files.forEach((f, i) => {
    const d = document.createElement("div");
    d.className = "file";
    d.innerHTML = `
      <b>📄 ${f.name}</b><br>
      ${formatBytes(f.size)}
      <div class="progress">
        <div class="bar" id="bar_${i}"></div>
      </div>
      <small id="info_${i}"></small>
    `;
    list.appendChild(d);
  });

  const parallel = document.getElementById("parallel").checked;
  if (parallel) {
    files.forEach((f,i) => uploadFile(f,i,files.length));
  } else {
    uploadSeq(files,0);
  }
}

function uploadSeq(files,i){
 if(i>=files.length){done();return;}
 uploadFile(files[i],i,files.length,()=>uploadSeq(files,i+1));
}

let completed=0;

function uploadFile(file,i,total,next){
 const xhr=new XMLHttpRequest();
 const bar=document.getElementById('bar_'+i);
 const info=document.getElementById('info_'+i);
 const fd=new FormData();
 fd.append('file',file);

xhr.upload.onprogress = e => {
  if (e.lengthComputable) {
    const percent = (e.loaded / e.total) * 100;
    bar.style.width = percent + '%';

    const now = Date.now();
    const elapsed = (now - startTime) / 1000;
    const currentUploaded = totalUploaded + e.loaded;

    if (elapsed > 0) {
      const speed = currentUploaded / elapsed;
      document.getElementById('totalInfo').innerText = Math.round((completed + e.loaded / e.total) * 100) + '% —' + formatBytes(speed) + '/s';
    }
  }
};

 xhr.onload=()=>{
  if(xhr.status===200){
    totalUploaded+=file.size;
    uploadedNames.add(file.name);
    info.innerText="✅ Done";
    completed++;
    document.getElementById("totalBar").style.width=(completed/total*100)+"%";

    const speed = totalUploaded / ((Date.now()-startTime)/1000);
    document.getElementById("totalInfo").innerText=completed+"/"+total+" files";

    if(next) next();
    if(completed===total) done();
  }else{
    info.innerText="❌ Failed";
  }
 };

 xhr.open("POST","/upload?token="+TOKEN);
 xhr.send(fd);
}

function reset(){
 uploading=false;
 document.getElementById("uploadBtn").disabled=false;
}

function done(){
  uploading=false;
  document.getElementById("uploadBtn").disabled=false;
  document.getElementById("totalInfo").innerText="✅ Upload completed";
}
</script>
</body>
</html>
"""
    return html.replace("__TOKEN__", token)

@app.post("/upload")
async def upload_file(token: str, file: UploadFile = File(...)):
    if token not in active_tokens or active_tokens[token] < time.time():
        raise HTTPException(status_code=403)

    filename = file.filename.replace("/", "_").replace("\\", "_")
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(await file.read())

    return {"status": "ok"}