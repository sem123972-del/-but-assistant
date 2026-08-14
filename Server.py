from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GROQ_API_KEY", "")
API_URL = "https://api.groq.com/openai/v1/chat/completions"

HTML = """<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>المساعد الذكي BTU</title><style>body{font-family:'Segoe UI',sans-serif;background:#f0f2f5;margin:0}.header{background:#004d40;color:white;padding:15px;text-align:center;display:flex;justify-content:space-between;align-items:center}.logo{background:white;color:#004d40;padding:10px;border-radius:50%;font-weight:bold}.chat{max-width:700px;margin:20px auto;background:#fff;padding:20px;border-radius:12px;box-shadow:0 2px 10px #0001}h2{color:#004d40;text-align:center}input{width:70%;padding:12px;font-size:16px;border:2px solid #004d40;border-radius:8px}button{width:25%;padding:12px;font-size:16px;background:#004d40;color:#fff;border:none;border-radius:8px;cursor:pointer}button:hover{background:#00695c}#ans{margin-top:20px;padding:15px;background:#e8f5e9;border-right:4px solid #004d40;border-radius:8px;white-space:pre-wrap;font-size:16px}.footer{text-align:center;padding:10px;color:#777;font-size:12px}</style></head><body><div class="header"><div class="logo">د.ع</div><div>عمادة الدراسات العليا<br>جامعة البطانة</div><div class="logo">BTU</div></div><div class="chat"><h2>المساعد الذكي Groq</h2><h3 style="color:#004d40;text-align:center;">جامعة البطانة BTU</h3><input id="q" placeholder="اسأل عن اي شي في الجامعة..."><button onclick="ask()">بحث</button><div id="ans">مرحبا! انا المساعد بالذكاء الاصطناعي</div></div><div class="footer">المساعد الذكي - عمادة الدراسات العليا - جامعة البطانة © 2025</div><script>async function ask(){let q=document.getElementById('q').value;if(!q)return;document.getElementById('ans').innerText='جاري التفكير...';let res=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q})});let data=await res.json();document.getElementById('ans').innerText=data.answer;}</script></body></html>"""

def get_answer(question):
    prompt = f"انت المساعد الرسمي لجامعة البطانة BTU في السودان. رد باللهجة السودانية وباسلوب رسمي ومفيد. السؤال: {question}"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}
    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"خطأ: {e}"

@app.route("/")
def home(): return render_template_string(HTML)
@app.route("/ask", methods=["POST"])
def ask(): q = request.get_json().get("q",""); return jsonify({"answer": get_answer(q)})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
