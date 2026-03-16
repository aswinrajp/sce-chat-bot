from flask import Flask, request, jsonify
import anthropic, os, json
from datetime import datetime
from groq import Groq

app = Flask(__name__)

# ══════════════════════════════════════════════════════
#  STEP 1: PASTE YOUR API KEY BELOW
#  Get it free from: console.anthropic.com
# ══════════════════════════════════════════════════════
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

# ══════════════════════════════════════════════════════
#  STEP 2: COLLEGE DATA (edit anytime)
# ══════════════════════════════════════════════════════
COLLEGE_DATA = """
COLLEGE NAME: Solamalai College of Engineering (SCE)
FORMERLY: Raja College of Engineering and Technology
ESTABLISHED: 1995
CHAIRMAN: Mr. V.S.P. Solamalai Pitchai, B.Sc
EXECUTIVE DIRECTOR: Mr. S.P. Aravind
LOCATION: S.V. Raja Nagar, Veerapanjan, Madurai - 625020, Tamil Nadu, India
DISTANCE: 6 km from Anna Bus Stand on Madurai-Sivagangai Road
CAMPUS AREA: 10 acres
PHONE: 04522429346, 04522429280, +91-9698044566, 8056351641
EMAIL: info@solamalaice.ac.in
WEBSITE: www.solamalaice.ac.in
RATING: 4.0/5 on Justdial (295 reviews), 4.5/5 Campus Life on Shiksha

ACCREDITATION:
- Affiliated to Anna University, Chennai
- Approved by AICTE, New Delhi
- Accredited by NAAC with A Grade
- ISO Certified Institution
- UGC Section 2(f) approved
- Autonomous status by UGC
- 2nd oldest engineering college in Madurai District
- Nodal Center for BMW Skill Next Program
- PMKVY affiliated center
- MHRD supported e-Yantra Robotics Lab
- Recognized by TNSDC
- Unnat Bharat Abhiyan nodal center

ABOUT SCE:
Solamalai College of Engineering is the 2nd oldest engineering college in Madurai District, established in 1995. Formerly Raja College of Engineering and Technology, acquired by Solamalai Group in 2016. The Solamalai Group has been active since 1962 in FMCG, transport, infrastructure, and cinema with 1400+ employees and 600 crore annual turnover.

VISION: Premier institute for higher education, nurturing youth as global, socially responsible citizens through academic, technical and innovative excellence.

UG PROGRAMS (573 total seats):
- B.E. Computer Science and Engineering (CSE)
- B.E. Electronics and Communication Engineering (ECE)
- B.E. Electrical and Electronics Engineering (EEE)
- B.E. Mechanical Engineering
- B.E. Civil Engineering
- B.Tech Artificial Intelligence and Data Science (AI and DS)
- B.Tech Computer Science and Business Systems (CSBS)
- B.Tech Information Technology (IT)
- BCA (Bachelor of Computer Applications)
- BBA (Bachelor of Business Administration)

PG PROGRAMS:
- M.E. CAD/CAM
- M.E. Power Electronics and Drives
- M.E. Embedded System Technologies
- M.Tech Computer Science and Engineering
- MBA (2 years)

ADMISSION:
- B.E./B.Tech: TNEA counselling based on 10+2 marks
- MBA: TANCET conducted by Anna University
- PG Engineering: GATE or CEETA-PG
- UG eligibility: 10+2 with Physics, Chemistry, Maths, minimum 50%
- Reservation fee: Rs. 3,000
- Admissions open January-February for August-September academic year

FEES:
- B.E./B.Tech Government quota: Rs. 50,000 to Rs. 70,000 per year
- B.E./B.Tech Management quota: Rs. 1,50,000 to Rs. 2,00,000 per year
- MBA: Rs. 35,000 per year
- Hostel fee: Rs. 3,800 per month including accommodation and mess
- Total fee range: Rs. 35,000 to Rs. 2,00,000 per year
- Scholarships for merit students and SC/ST/OBC category

LIBRARY:
- 400 sq.m spacious library
- 25,000+ books, national and international journals
- E-library and digital resources
- Veranda Learning Solutions study materials for competitive exams
- Students describe it as huge and one of the best libraries

LABORATORIES:
- Fully equipped advanced labs in all departments
- MHRD-supported e-Yantra Robotics Lab (Top 25 at IIT Bombay eLSI Hackathon)
- AI and Data Science lab, Embedded Systems lab
- Complete tools for CSE, ECE, EEE, Mechanical, Civil, IT

HOSTEL:
- 2 boys hostels plus 2 girls hostels on campus
- Fee: Rs. 3,800 per month including accommodation and all meals
- Free 24-hour Wi-Fi
- Food rated awesome by students
- 24-hour security

CAMPUS:
- 10-acre eco-friendly campus with huge garden
- Free Wi-Fi across all buildings 24 hours
- Modern classrooms, auditorium, sports ground
- Canteen with very good quality food

TRANSPORT:
- Buses covering routes across Madurai
- Routes: Usilampatti, Thirumangalam, Alanganallur, Melur, Kariapatti,
  Sivagangai, Manamadurai, Periyar Bus Stand, Kadachanendhal and more

SPORTS AND ACTIVITIES:
- Cricket, football, basketball, volleyball courts
- YI Club, Rotaract Club, GDG Club, ECO Club, Literary Club, Cultural Club
- Annual cultural fest Viyugam and Bazaar
- NSS unit, inter-college tournaments, Annual Sports Day

PLACEMENTS:
- Dedicated Training and Placement Cell
- Companies: TCS, Infosys, Wipro, HCL, Cognizant, Accenture, Reliance,
  Tata Motors, Zoho, Freshworks, Neeyamo, Solartis and more
- Training: aptitude, soft skills, mock interviews, coding bootcamps
- Accu Services recruited Graduate Engineer Trainees in 2024

RESEARCH AND INNOVATION:
- Solamalai Foundation for Start-up Incubation (SFSI) February 2024
- e-Yantra team Top 25 at eLSI Hackathon IIT Bombay 2024
- Project Expo 2024 and Idea Hackathon-24 held March 2024
- 9th State Level Project Expo: 180+ participants from 15+ polytechnics

STUDENT STRENGTH:
- Students: 388, Faculty: 78, Ratio 5:1, Programs: 12
"""

def ask_ai(question, extra=""):
    data = extra.strip() if extra.strip() else COLLEGE_DATA
    sys_prompt = (
        "You are SCE-BOT, official AI assistant for Solamalai College of Engineering (SCE), Madurai.\n"
        "Answer questions accurately using the college data below. Be clear and helpful.\n"
        "Use bullet points for lists.\n"
        "If info is not available say: Contact SCE at info@solamalaice.ac.in or 04522429346\n"
        "Never invent information.\n\nSCE DATA:\n" + data
    )
    r = client.chat.completions.create(
    model="llama-3.3-70b-versatile",

    max_tokens=1024,
    messages=[
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": question}
    ]
)
    return r.choices[0].message.content
    


@app.route("/")
def index():
    safe_data = json.dumps(COLLEGE_DATA)
    return HTML.replace("__COLLEGE_DATA__", safe_data)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        d = request.get_json()
        q = d.get("question", "").strip()
        if not q:
            return jsonify({"error": "empty"}), 400
        return jsonify({"answer": ask_ai(q, d.get("extra_data", ""))})
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"answer": "Error: " + str(e)}), 500

# ══════════════════════════════════════════════════════
#  HTML UI — everything embedded, no external files
# ══════════════════════════════════════════════════════
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SCE-BOT | Solamalai College of Engineering</title>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;600;700&family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#020c1b;--bg2:#0a1628;--cyan:#00f5ff;--green:#00ff88;--purple:#7c3aed;--pink:#ff0080;--yellow:#ffd700;--text:#ccd6f6;--muted:#8892b0;--border:rgba(0,245,255,0.15)}
html,body{height:100%;overflow:hidden}
body{background:var(--bg);font-family:'Inter',sans-serif;color:var(--text)}
#bgCanvas{position:fixed;inset:0;z-index:0;opacity:0.15}
#splash{position:fixed;inset:0;z-index:100;background:var(--bg);display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity 0.9s ease}
#splash.out{opacity:0;pointer-events:none}
.scan-line{position:absolute;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,rgba(0,245,255,0.5),transparent);animation:scan 3s linear infinite;top:-2px}
@keyframes scan{0%{top:-2px}100%{top:100%}}
.splash-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,245,255,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(0,245,255,0.04) 1px,transparent 1px);background-size:50px 50px}
.sc{position:relative;z-index:2;text-align:center;animation:fu 0.8s ease forwards}
@keyframes fu{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.lw{width:130px;height:130px;margin:0 auto 24px;position:relative}
.lr{position:absolute;inset:-10px;border:1px solid rgba(0,245,255,0.25);border-radius:50%;animation:sp 8s linear infinite}
.lr2{position:absolute;inset:-20px;border:1px dashed rgba(0,245,255,0.12);border-radius:50%;animation:sp 14s linear infinite reverse}
.lr3{position:absolute;inset:-4px;border:2px solid rgba(0,245,255,0.08);border-radius:50%;animation:sp 5s linear infinite}
@keyframes sp{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
.lc{width:130px;height:130px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#1a3a6b,#060f1e);border:2px solid rgba(0,245,255,0.5);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;box-shadow:0 0 40px rgba(0,245,255,0.25),inset 0 0 40px rgba(0,0,0,0.6)}
.lc::before{content:'';position:absolute;inset:0;background:radial-gradient(circle at 50% 0%,rgba(0,245,255,0.12),transparent 60%)}
.lsvg{width:90px;height:90px;position:relative;z-index:1}
.sn{font-family:'Orbitron',monospace;font-size:clamp(20px,3.5vw,34px);font-weight:900;color:#fff;letter-spacing:2px;line-height:1.2;margin-bottom:4px;text-shadow:0 0 30px rgba(0,245,255,0.4)}
.sn span{color:var(--cyan)}
.bgs{display:flex;align-items:center;gap:10px;justify-content:center;margin:14px 0 8px;flex-wrap:wrap}
.bg{font-family:'JetBrains Mono',monospace;font-size:10px;padding:4px 10px;border:1px solid var(--cyan);color:var(--cyan);border-radius:3px;letter-spacing:1px;text-shadow:0 0 6px var(--cyan)}
.dv{width:80px;height:1px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);margin:14px auto}
.bt{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--green);margin-bottom:28px;text-align:left;width:340px;max-width:90vw;min-height:76px}
.bl{display:block;opacity:0;animation:ti 0.1s ease forwards}
@keyframes ti{to{opacity:1}}
.eb{font-family:'Orbitron',monospace;font-size:12px;font-weight:700;letter-spacing:3px;text-transform:uppercase;padding:13px 44px;background:transparent;color:var(--cyan);border:1px solid var(--cyan);border-radius:2px;cursor:pointer;position:relative;overflow:hidden;transition:all 0.3s;text-shadow:0 0 10px var(--cyan);display:none}
.eb::before{content:'';position:absolute;inset:0;background:var(--cyan);transform:translateX(-100%);transition:transform 0.3s}
.eb:hover{color:var(--bg)}.eb:hover::before{transform:translateX(0)}
.eb.show{display:inline-block}
.sg{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--yellow);margin-top:14px;text-shadow:0 0 10px rgba(255,215,0,0.4)}
#app{position:fixed;inset:0;z-index:10;display:none;flex-direction:column;opacity:0;transition:opacity 0.6s ease}
#app.show{display:flex;opacity:1}
.hdr{height:56px;background:rgba(2,12,27,0.97);border-bottom:1px solid var(--border);display:flex;align-items:center;padding:0 18px;gap:12px;backdrop-filter:blur(10px);flex-shrink:0;position:relative;z-index:20}
.hdr::after{content:'';position:absolute;bottom:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);opacity:0.4}
.hl{width:36px;height:36px;border-radius:50%;background:radial-gradient(circle,#1a3a6b,#060f1e);border:1px solid rgba(0,245,255,0.4);display:flex;align-items:center;justify-content:center;flex-shrink:0;box-shadow:0 0 12px rgba(0,245,255,0.2)}
.ht{font-family:'Orbitron',monospace;font-size:13px;font-weight:700;color:var(--cyan);text-shadow:0 0 10px rgba(0,245,255,0.4);letter-spacing:1px}
.hs{font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--muted);letter-spacing:1px}
.hsp{flex:1}
.sd{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:bk 2s ease-in-out infinite;flex-shrink:0}
@keyframes bk{0%,100%{opacity:1}50%{opacity:0.3}}
.st{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--green);letter-spacing:1px}
.edb{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:1px;padding:5px 11px;background:rgba(0,245,255,0.05);color:var(--cyan);border:1px solid rgba(0,245,255,0.25);border-radius:3px;cursor:pointer;transition:all 0.2s;text-transform:uppercase}
.edb:hover{background:rgba(0,245,255,0.1)}
.body{flex:1;display:flex;overflow:hidden}
.sb{width:210px;flex-shrink:0;background:rgba(10,22,40,0.92);border-right:1px solid var(--border);display:flex;flex-direction:column;overflow-y:auto;backdrop-filter:blur(10px)}
.sb::-webkit-scrollbar{width:3px}.sb::-webkit-scrollbar-thumb{background:rgba(0,245,255,0.1)}
.ss{padding:14px 10px 6px}
.sl{font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:8px;display:flex;align-items:center;gap:6px}
.sl::after{content:'';flex:1;height:1px;background:var(--border)}
.chip{display:block;width:100%;font-family:'JetBrains Mono',monospace;font-size:11px;padding:7px 10px;background:transparent;color:var(--text);border:1px solid rgba(255,255,255,0.05);border-radius:2px;cursor:pointer;text-align:left;transition:all 0.2s;margin-bottom:3px}
.chip:hover{background:rgba(0,245,255,0.07);color:var(--cyan);border-color:rgba(0,245,255,0.25);padding-left:14px}
.ib{margin:6px 10px;padding:10px;background:rgba(0,245,255,0.03);border:1px solid rgba(0,245,255,0.1);border-radius:3px}
.ir{font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--muted);margin-bottom:4px;display:flex;justify-content:space-between}
.ir span{color:var(--cyan)}
.cw{flex:1;display:flex;flex-direction:column;overflow:hidden}
.gb{padding:9px 18px;background:linear-gradient(135deg,rgba(124,58,237,0.12),rgba(0,245,255,0.06));border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.gt{font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--yellow);text-shadow:0 0 8px rgba(255,215,0,0.3)}
.gt span{color:var(--muted);font-size:10px;display:block;margin-top:2px}
.td{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted)}
.msgs{flex:1;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:14px;scrollbar-width:thin;scrollbar-color:rgba(0,245,255,0.15) transparent}
.msgs::-webkit-scrollbar{width:4px}.msgs::-webkit-scrollbar-thumb{background:rgba(0,245,255,0.15);border-radius:2px}
.mw{display:flex;gap:10px;align-items:flex-start;animation:mi 0.3s ease}
@keyframes mi{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.mw.user{flex-direction:row-reverse}
.av{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:2px;font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:700}
.av.bot{background:radial-gradient(circle,#1a3a6b,#060f1e);border:1px solid rgba(0,245,255,0.4);color:var(--cyan);box-shadow:0 0 8px rgba(0,245,255,0.12)}
.av.user{background:radial-gradient(circle,#3b1d6b,#160a28);border:1px solid rgba(124,58,237,0.4);color:#a78bfa}
.mb{max-width:74%;padding:11px 15px;border-radius:2px;font-size:13px;line-height:1.7;white-space:pre-wrap;word-break:break-word;position:relative}
.mb.bot{background:rgba(8,20,40,0.95);color:var(--text);border:1px solid rgba(0,245,255,0.12);border-left:2px solid var(--cyan)}
.mb.bot::before{content:'SCE-BOT';display:block;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;color:var(--cyan);opacity:0.55;margin-bottom:5px}
.mb.user{background:rgba(124,58,237,0.1);color:var(--text);border:1px solid rgba(124,58,237,0.2);border-right:2px solid #7c3aed}
.mb.user::before{content:'YOU';display:block;font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:1px;color:#a78bfa;opacity:0.55;margin-bottom:5px;text-align:right}
.tyb{background:rgba(8,20,40,0.95);border:1px solid rgba(0,245,255,0.12);border-left:2px solid var(--cyan);border-radius:2px;padding:13px 15px;display:flex;gap:5px;align-items:center}
.dot{width:6px;height:6px;border-radius:50%;background:var(--cyan);animation:bn 1.2s infinite;box-shadow:0 0 4px var(--cyan)}
.dot:nth-child(2){animation-delay:.2s}.dot:nth-child(3){animation-delay:.4s}
@keyframes bn{0%,80%,100%{transform:translateY(0)}40%{transform:translateY(-6px)}}
.ia{padding:10px 16px;background:rgba(2,12,27,0.97);border-top:1px solid var(--border);display:flex;gap:10px;align-items:center;flex-shrink:0;position:relative}
.ia::before{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,var(--cyan),transparent);opacity:0.25}
.pr{font-family:'JetBrains Mono',monospace;font-size:14px;color:var(--green);flex-shrink:0;text-shadow:0 0 6px var(--green)}
.inp{flex:1;background:transparent;border:none;outline:none;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--text);caret-color:var(--cyan)}
.inp::placeholder{color:rgba(136,146,176,0.35)}
.sb2{width:36px;height:36px;background:rgba(0,245,255,0.07);border:1px solid rgba(0,245,255,0.25);border-radius:2px;color:var(--cyan);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:16px;transition:all 0.2s;flex-shrink:0}
.sb2:hover{background:rgba(0,245,255,0.18);box-shadow:0 0 12px rgba(0,245,255,0.25)}
.sb2:disabled{opacity:0.3;cursor:not-allowed}
#ap{display:none;position:fixed;inset:0;z-index:200;background:rgba(2,12,27,0.92);align-items:center;justify-content:center;backdrop-filter:blur(8px)}
#ap.open{display:flex}
.ab{background:var(--bg2);border:1px solid rgba(0,245,255,0.2);border-radius:4px;width:90%;max-width:680px;max-height:85vh;display:flex;flex-direction:column;overflow:hidden}
.ah{padding:14px 20px;background:rgba(0,245,255,0.04);border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}
.ah h3{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--cyan);letter-spacing:1px}
.ac{background:rgba(255,0,128,0.08);border:1px solid rgba(255,0,128,0.25);color:var(--pink);width:28px;height:28px;border-radius:3px;cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center}
.ac:hover{background:rgba(255,0,128,0.18)}
.abody{padding:18px 20px;flex:1;overflow-y:auto}
.abody p{font-family:'JetBrains Mono',monospace;font-size:11px;color:var(--muted);margin-bottom:12px;line-height:1.6}
.abody textarea{width:100%;height:280px;background:rgba(2,12,27,0.8);border:1px solid rgba(0,245,255,0.18);border-radius:3px;padding:12px;font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--text);resize:vertical;outline:none;line-height:1.6}
.abody textarea:focus{border-color:rgba(0,245,255,0.45)}
.af{padding:12px 20px;border-top:1px solid var(--border);display:flex;gap:10px;justify-content:flex-end}
.bsv{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;padding:8px 22px;background:rgba(0,245,255,0.08);color:var(--cyan);border:1px solid rgba(0,245,255,0.25);border-radius:3px;cursor:pointer}
.bsv:hover{background:rgba(0,245,255,0.18)}
.bcn{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:1px;text-transform:uppercase;padding:8px 16px;background:transparent;color:var(--muted);border:1px solid rgba(255,255,255,0.07);border-radius:3px;cursor:pointer}
.toast{display:none;position:fixed;bottom:22px;right:22px;z-index:9999;background:rgba(0,255,136,0.08);border:1px solid rgba(0,255,136,0.25);color:var(--green);padding:10px 20px;border-radius:3px;font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:1px}
@media(max-width:600px){.sb{display:none}.sn{font-size:18px}}
</style>
</head>
<body>
<canvas id="bgCanvas"></canvas>
<div id="splash">
  <div class="scan-line"></div>
  <div class="splash-grid"></div>
  <div class="sc">
    <div class="lw">
      <div class="lr"></div><div class="lr2"></div><div class="lr3"></div>
      <div class="lc">
        <svg class="lsvg" viewBox="0 0 90 90" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <filter id="glow"><feGaussianBlur stdDeviation="2.5" result="b"/><feComposite in="SourceGraphic" in2="b" operator="over"/></filter>
            <filter id="glow2"><feGaussianBlur stdDeviation="1" result="b"/><feComposite in="SourceGraphic" in2="b" operator="over"/></filter>
          </defs>
          <path d="M45 5 L76 19 L76 46 C76 64 61 77 45 82 C29 77 14 64 14 46 L14 19 Z" fill="rgba(0,245,255,0.04)" stroke="#00f5ff" stroke-width="1.5" opacity="0.75"/>
          <path d="M45 13 L68 25 L68 46 C68 60 57 70 45 74 C33 70 22 60 22 46 L22 25 Z" fill="rgba(0,245,255,0.03)" stroke="#00f5ff" stroke-width="1" opacity="0.4"/>
          <text x="45" y="54" font-family="Orbitron,monospace" font-size="30" font-weight="900" fill="#00f5ff" text-anchor="middle" filter="url(#glow)">S</text>
          <text x="45" y="68" font-family="JetBrains Mono,monospace" font-size="10" fill="rgba(0,245,255,0.55)" text-anchor="middle" letter-spacing="4" filter="url(#glow2)">CE</text>
          <circle cx="45" cy="8" r="1.5" fill="#00f5ff" opacity="0.7"/>
          <circle cx="35" cy="11" r="1" fill="#00f5ff" opacity="0.4"/>
          <circle cx="55" cy="11" r="1" fill="#00f5ff" opacity="0.4"/>
          <line x1="32" y1="72" x2="58" y2="72" stroke="rgba(0,245,255,0.3)" stroke-width="0.5"/>
        </svg>
      </div>
    </div>
    <div class="sn">Solamalai College<br>of <span>Engineering</span></div>
    <div class="bgs">
      <span class="bg">EST. 1995</span>
      <span class="bg">NAAC A</span>
      <span class="bg">ANNA UNIV</span>
      <span class="bg">MADURAI</span>
    </div>
    <div class="dv"></div>
    <div class="bt" id="bootText"></div>
    <button class="eb" id="enterBtn" onclick="enterApp()">&#9654; LAUNCH SCE-BOT</button>
    <div class="sg" id="greetLine"></div>
  </div>
</div>
<div id="app">
  <div class="hdr">
    <div class="hl">
      <svg width="22" height="22" viewBox="0 0 90 90" fill="none">
        <path d="M45 5 L76 19 L76 46 C76 64 61 77 45 82 C29 77 14 64 14 46 L14 19 Z" fill="none" stroke="#00f5ff" stroke-width="2" opacity="0.9"/>
        <text x="45" y="56" font-family="Orbitron,monospace" font-size="34" font-weight="900" fill="#00f5ff" text-anchor="middle">S</text>
      </svg>
    </div>
    <div><div class="ht">SCE-BOT v2.0</div><div class="hs">SOLAMALAI COLLEGE OF ENGINEERING &#183; MADURAI</div></div>
    <div class="hsp"></div>
    <div class="sd"></div>
    <div class="st">ONLINE</div>
    <button class="edb" onclick="openAdmin()">&#9998; EDIT INFO</button>
  </div>
  <div class="body">
    <div class="sb">
      <div class="ss">
        <div class="sl">Quick Access</div>
        <button class="chip" onclick="ask('What courses are offered at SCE?')">&#128218; Courses</button>
        <button class="chip" onclick="ask('What is the fee structure for all programs?')">&#128176; Fees</button>
        <button class="chip" onclick="ask('Hostel facilities and monthly fee')">&#127968; Hostel</button>
        <button class="chip" onclick="ask('Library details')">&#128216; Library</button>
        <button class="chip" onclick="ask('Placement companies and packages')">&#128188; Placements</button>
        <button class="chip" onclick="ask('Transport bus routes available')">&#128652; Transport</button>
        <button class="chip" onclick="ask('Lab facilities and equipment')">&#128300; Labs</button>
        <button class="chip" onclick="ask('How to get admission in SCE?')">&#128203; Admission</button>
        <button class="chip" onclick="ask('Sports and student clubs at SCE')">&#9917; Sports &amp; Clubs</button>
        <button class="chip" onclick="ask('Research and startup at SCE')">&#128161; Research</button>
        <button class="chip" onclick="ask('Contact details and address of SCE')">&#128222; Contact</button>
      </div>
      <div class="ss">
        <div class="sl">College Stats</div>
        <div class="ib">
          <div class="ir">Status <span>AUTONOMOUS</span></div>
          <div class="ir">Affil. <span>ANNA UNIV</span></div>
          <div class="ir">Grade <span>NAAC A</span></div>
          <div class="ir">Est. <span>1995</span></div>
          <div class="ir">Campus <span>10 ACRES</span></div>
          <div class="ir">Students <span>388</span></div>
          <div class="ir">Faculty <span>78</span></div>
          <div class="ir">Programs <span>12</span></div>
        </div>
      </div>
    </div>
    <div class="cw">
      <div class="gb">
        <div class="gt" id="gBar">&#9654; Welcome to SCE-BOT!<span>Ask anything about Solamalai College of Engineering</span></div>
        <div class="td" id="timeD">--:--:--</div>
      </div>
      <div class="msgs" id="msgs">
        <div class="mw">
          <div class="av bot">BOT</div>
          <div class="mb bot">System initialized. SCE Knowledge Base loaded successfully.

&#9679; Institution: Solamalai College of Engineering, Madurai
&#9679; Accreditation: NAAC A Grade | Anna University | AICTE
&#9679; Data: Latest 2024 information loaded
&#9679; Status: ALL SYSTEMS OPERATIONAL

Ready to answer any question about SCE.
Type below or select a topic from the sidebar.</div>
        </div>
      </div>
      <div class="ia">
        <span class="pr">&gt;_</span>
        <input class="inp" id="inp" type="text" placeholder="Ask anything about SCE, Madurai..." onkeydown="if(event.key==='Enter')send()">
        <button class="sb2" id="sendBtn" onclick="send()">&#10148;</button>
      </div>
    </div>
  </div>
</div>
<div id="ap">
  <div class="ab">
    <div class="ah">
      <h3>// EDIT COLLEGE DATA</h3>
      <button class="ac" onclick="closeAdmin()">&#10005;</button>
    </div>
    <div class="abody">
      <p>// Edit or add any college information below. Changes apply immediately.<br>// Add new fees, events, rules, anything you want.</p>
      <textarea id="adminText"></textarea>
    </div>
    <div class="af">
      <button class="bcn" onclick="closeAdmin()">CANCEL</button>
      <button class="bsv" onclick="saveInfo()">&#10003; SAVE &amp; APPLY</button>
    </div>
  </div>
</div>
<div class="toast" id="toast">&#10003; DATA UPDATED SUCCESSFULLY</div>
<script>
(function(){
  var c=document.getElementById('bgCanvas'),ctx=c.getContext('2d');
  function r(){c.width=window.innerWidth;c.height=window.innerHeight}r();
  window.addEventListener('resize',r);
  var cols=Math.floor(window.innerWidth/20),drops=Array(cols).fill(1);
  var ch='SCEAICTEMADURAI0123456789ABCDEFXYZ><{}[]';
  setInterval(function(){
    ctx.fillStyle='rgba(2,12,27,0.05)';ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle='rgba(0,245,255,0.3)';ctx.font='13px JetBrains Mono,monospace';
    for(var i=0;i<drops.length;i++){
      ctx.fillText(ch[Math.floor(Math.random()*ch.length)],i*20,drops[i]*20);
      if(drops[i]*20>c.height&&Math.random()>0.975)drops[i]=0;
      drops[i]++;
    }
  },55);
})();
var lines=['> Initializing SCE-BOT v2.0...','> Connecting to AI engine...','> Loading college database...','> Verifying NAAC A Grade data...','> Knowledge base: LOADED','> All systems: ONLINE','> Ready to assist students.'];
var bEl=document.getElementById('bootText');
function boot(i){
  if(i>=lines.length){document.getElementById('enterBtn').classList.add('show');return}
  var s=document.createElement('span');s.className='bl';
  s.style.animationDelay=(i*0.05)+'s';
  s.style.color=(lines[i].indexOf('LOADED')>-1||lines[i].indexOf('ONLINE')>-1||lines[i].indexOf('Ready')>-1)?'#00ff88':'#00f5ff';
  s.textContent=lines[i];bEl.appendChild(s);
  setTimeout(function(){boot(i+1)},300);
}
setTimeout(function(){boot(0)},500);
function pad(x){return x.toString().padStart(2,'0')}
function tick(){var n=new Date();var el=document.getElementById('timeD');if(el)el.textContent=pad(n.getHours())+':'+pad(n.getMinutes())+':'+pad(n.getSeconds())}
setInterval(tick,1000);tick();
var h=new Date().getHours();
var gr=h<12?'Good Morning':h<17?'Good Afternoon':h<21?'Good Evening':'Good Night';
var sb=h<12?'Rise and code!':h<17?'Keep building!':h<21?'Evening session!':'Late night coder!';
document.getElementById('greetLine').textContent=gr+' \u2014 '+sb;
var gbEl=document.getElementById('gBar');
if(gbEl)gbEl.innerHTML='&#9654; '+gr+', welcome to SCE-BOT!<span>'+sb+' \u2014 Ask anything about Solamalai College of Engineering</span>';
var collegeInfo=__COLLEGE_DATA__;
function enterApp(){
  document.getElementById('splash').classList.add('out');
  setTimeout(function(){
    document.getElementById('splash').style.display='none';
    var a=document.getElementById('app');a.style.display='flex';
    setTimeout(function(){a.classList.add('show')},50);
  },900);
}
function send(){var i=document.getElementById('inp'),q=i.value.trim();if(!q)return;i.value='';ask(q)}
function ask(q){
  var msgs=document.getElementById('msgs'),btn=document.getElementById('sendBtn');
  msgs.innerHTML+='<div class="mw user"><div class="av user">YOU</div><div class="mb user">'+esc(q)+'</div></div>';
  var t=document.createElement('div');t.className='mw';t.id='typing';
  t.innerHTML='<div class="av bot">BOT</div><div class="tyb"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>';
  msgs.appendChild(t);msgs.scrollTop=msgs.scrollHeight;btn.disabled=true;
  fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q,extra_data:collegeInfo})})
  .then(function(r){return r.json()}).then(function(d){
    var e=document.getElementById('typing');if(e)e.remove();
    msgs.innerHTML+='<div class="mw"><div class="av bot">BOT</div><div class="mb bot">'+esc(d.answer)+'</div></div>';
    msgs.scrollTop=msgs.scrollHeight;btn.disabled=false;
  }).catch(function(){
    var e=document.getElementById('typing');if(e)e.remove();
    msgs.innerHTML+='<div class="mw"><div class="av bot">BOT</div><div class="mb bot">ERROR: Check your API key in app.py and restart the server.</div></div>';
    msgs.scrollTop=msgs.scrollHeight;btn.disabled=false;
  });
}
function esc(t){return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\\n/g,'<br>')}
function openAdmin(){document.getElementById('adminText').value=collegeInfo;document.getElementById('ap').classList.add('open')}
function closeAdmin(){document.getElementById('ap').classList.remove('open')}
function saveInfo(){collegeInfo=document.getElementById('adminText').value;closeAdmin();var t=document.getElementById('toast');t.style.display='block';setTimeout(function(){t.style.display='none'},3000)}
</script>
</body>
</html>"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
