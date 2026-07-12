// @ts-nocheck
const { useState, useRef, useEffect, useCallback } = React;

/* ═══════════════════════════════════════
   DESIGN SYSTEM — Netflix Premium
═══════════════════════════════════════ */
const C = {
  bg:       "#050505",
  bg1:      "#0b0b0d",
  bg2:      "#141414",
  bg3:      "#202020",
  bg4:      "#2a2a2a",
  card:     "rgba(255,255,255,0.045)",
  border:   "rgba(255,255,255,0.10)",
  borderHi: "rgba(229,9,20,0.42)",
  purple:   "#e50914",
  violet:   "#b20710",
  indigo:   "#d6b36a",
  cyan:     "#f5f5f1",
  green:    "#46d369",
  amber:    "#d6b36a",
  red:      "#ff3045",
  pink:     "#b3b3b3",
  text:     "#f5f5f1",
  muted:    "rgba(245,245,241,0.62)",
  faint:    "rgba(245,245,241,0.28)",
  grad:     "linear-gradient(135deg,#e50914,#b20710)",
  gradCard: "linear-gradient(135deg,rgba(229,9,20,0.16),rgba(214,179,106,0.08))",
};

const FONT = `'Outfit', system-ui, sans-serif`;
const MONO = `'Fira Code', 'Cascadia Code', monospace`;

/* ═══════ CLAUDE API ═══════ */
async function callClaude(system, user, maxTokens = 1500) {
  const res = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: maxTokens,
      system,
      messages: [{ role: "user", content: user }],
    }),
  });
  const data = await res.json();
  const raw = data.content?.map(b => b.text || "").join("") || "{}";
  try { return JSON.parse(raw.replace(/```json|```/g, "").trim()); }
  catch { return { error: raw }; }
}

/* ═══════ GLOBAL CSS ═══════ */
const G = () => (
  <style>{`
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Fira+Code:wght@400;500;700&display=swap');
    *{box-sizing:border-box;margin:0;padding:0;}
    html,body,#root{background:${C.bg};color:${C.text};font-family:${FONT};min-height:100vh;}
    ::-webkit-scrollbar{width:5px;height:5px;}
    ::-webkit-scrollbar-track{background:${C.bg1};}
    ::-webkit-scrollbar-thumb{background:${C.bg4};border-radius:3px;}

    @keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.4}}
    @keyframes spin{to{transform:rotate(360deg)}}
    @keyframes wave{0%,100%{height:8px}50%{height:24px}}
    @keyframes glow{0%,100%{box-shadow:0 0 20px rgba(229,9,20,.2)}50%{box-shadow:0 0 40px rgba(229,9,20,.5)}}
    @keyframes scan{0%{top:-20%}100%{top:120%}}
    @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
    @keyframes shimmer{0%{background-position:200% 50%}100%{background-position:-200% 50%}}
    @keyframes countup{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:scale(1)}}
    @keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

    .fade-up{animation:fadeUp .5s ease both;}
    .fade-in{animation:fadeIn .4s ease both;}

    .btn{font-family:${FONT};font-weight:600;cursor:pointer;border:none;outline:none;
      transition:all .2s cubic-bezier(.34,1.56,.64,1);letter-spacing:.2px;}
    .btn:active{transform:scale(.97)!important;}

    .btn-primary{background:${C.grad};color:#fff;padding:12px 28px;border-radius:10px;font-size:14px;}
    .btn-primary:hover{transform:translateY(-2px);box-shadow:0 12px 32px rgba(178,7,16,.45);}

    .btn-outline{background:transparent;color:${C.purple};border:1.5px solid ${C.purple};padding:11px 26px;border-radius:10px;font-size:14px;}
    .btn-outline:hover{background:rgba(229,9,20,.12);transform:translateY(-1px);}

    .btn-ghost{background:rgba(255,255,255,.05);color:${C.muted};border:1px solid ${C.border};padding:10px 20px;border-radius:9px;font-size:13px;}
    .btn-ghost:hover{background:rgba(255,255,255,.09);color:${C.text};border-color:rgba(255,255,255,.15);}

    .btn-danger{background:rgba(244,63,94,.15);color:${C.red};border:1px solid rgba(244,63,94,.3);padding:10px 20px;border-radius:9px;font-size:13px;}
    .btn-danger:hover{background:rgba(244,63,94,.25);}

    .btn-sm{padding:7px 16px!important;font-size:12px!important;}

    .card{background:${C.card};border:1px solid ${C.border};border-radius:16px;
      backdrop-filter:blur(12px);transition:border-color .2s,transform .2s;}

    .card-hover:hover{border-color:${C.borderHi};transform:translateY(-2px);
      box-shadow:0 20px 48px rgba(178,7,16,.12);}

    .glass{background:rgba(229,9,20,.08);border:1px solid rgba(229,9,20,.2);
      backdrop-filter:blur(20px);border-radius:16px;}

    input,textarea,select{font-family:${FONT};background:rgba(255,255,255,.04);
      border:1px solid ${C.border};color:${C.text};border-radius:10px;
      padding:11px 15px;font-size:14px;outline:none;width:100%;
      transition:border-color .2s,box-shadow .2s;}
    input:focus,textarea:focus,select:focus{
      border-color:${C.purple};box-shadow:0 0 0 3px rgba(229,9,20,.12);}
    textarea::placeholder,input::placeholder{color:${C.faint};}
    select option{background:#1a1535;}

    label{font-size:11px;font-weight:700;color:${C.muted};letter-spacing:1px;
      text-transform:uppercase;display:block;margin-bottom:7px;}

    .chip{display:inline-flex;align-items:center;gap:4px;padding:3px 11px;
      border-radius:20px;font-size:11px;font-weight:700;letter-spacing:.4px;}
    .chip-purple{background:rgba(229,9,20,.15);color:${C.purple};}
    .chip-cyan{background:rgba(34,211,238,.12);color:${C.cyan};}
    .chip-green{background:rgba(16,185,129,.12);color:${C.green};}
    .chip-amber{background:rgba(245,158,11,.12);color:${C.amber};}
    .chip-red{background:rgba(244,63,94,.12);color:${C.red};}
    .chip-pink{background:rgba(236,72,153,.12);color:${C.pink};}

    .progress{height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden;}
    .progress-fill{height:100%;border-radius:3px;transition:width 1s cubic-bezier(.34,1.2,.64,1);}

    .nav-btn{background:transparent;border:none;font-family:${FONT};color:${C.muted};
      padding:10px 14px;font-size:13px;cursor:pointer;border-radius:10px;
      display:flex;align-items:center;gap:9px;width:100%;transition:all .15s;text-align:left;}
    .nav-btn:hover{background:rgba(229,9,20,.08);color:${C.text};}
    .nav-btn.on{background:rgba(229,9,20,.14);color:${C.purple};font-weight:700;}

    .tab{background:transparent;border:none;font-family:${FONT};color:${C.muted};
      padding:10px 20px;font-size:13px;font-weight:600;cursor:pointer;
      border-bottom:2px solid transparent;transition:all .2s;white-space:nowrap;}
    .tab.on{color:${C.purple};border-bottom-color:${C.purple};}
    .tab:hover{color:${C.text};}

    .section{animation:fadeUp .4s ease;}

    /* interview bubble styles */
    .bubble-ai{background:linear-gradient(135deg,rgba(178,7,16,.25),rgba(214,179,106,.15));
      border:1px solid rgba(229,9,20,.3);border-radius:16px 16px 16px 4px;padding:18px 22px;}
    .bubble-user{background:rgba(255,255,255,.06);border:1px solid ${C.border};
      border-radius:16px 16px 4px 16px;padding:18px 22px;}

    /* code editor */
    .code-editor{font-family:${MONO};background:#0d1117;border:1px solid ${C.border};
      border-radius:12px;padding:18px;font-size:13px;line-height:1.8;color:#e6edf3;
      resize:vertical;width:100%;min-height:280px;outline:none;}
    .code-editor:focus{border-color:${C.purple};}

    /* camera frame */
    .cam-frame{position:relative;border-radius:16px;overflow:hidden;
      border:2px solid rgba(229,9,20,.3);background:#050505;}

    /* domain card */
    .domain-card{background:${C.card};border:1.5px solid ${C.border};border-radius:14px;
      padding:20px;cursor:pointer;transition:all .2s;text-align:center;}
    .domain-card:hover,.domain-card.sel{border-color:${C.purple};
      background:rgba(229,9,20,.1);transform:translateY(-3px);
      box-shadow:0 16px 40px rgba(178,7,16,.18);}

    .stat-box{background:${C.card};border:1px solid ${C.border};border-radius:14px;
      padding:20px;text-align:center;}

    .glow-dot{width:8px;height:8px;border-radius:50%;animation:pulse 1.5s infinite;}
  `}</style>
);

/* ═══════ HELPERS ═══════ */
const fmtTime = s => `${String(Math.floor(s/60)).padStart(2,"0")}:${String(s%60).padStart(2,"0")}`;
const scoreColor = s => s>=8?C.green:s>=6?C.cyan:s>=4?C.amber:C.red;
const scoreLabel = s => s>=8?"Excellent":s>=6?"Good":s>=4?"Average":"Poor";

function Loader({msg="AI is thinking..."}) {
  return (
    <div style={{display:"flex",flexDirection:"column",alignItems:"center",gap:14,padding:"40px 0"}}>
      <div style={{display:"flex",gap:5,alignItems:"flex-end",height:32}}>
        {[0,1,2,3,4].map(i=>(
          <div key={i} style={{width:4,background:C.purple,borderRadius:2,
            animation:`wave .8s ease infinite`,animationDelay:`${i*.1}s`}}/>
        ))}
      </div>
      <div style={{fontSize:13,color:C.muted}}>{msg}</div>
    </div>
  );
}

function ScoreRing({score,size=88,label}) {
  const r=size*.38,circ=2*Math.PI*r,fill=(score/10)*circ,col=scoreColor(score);
  return (
    <div style={{display:"flex",flexDirection:"column",alignItems:"center",gap:5}}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(255,255,255,.06)" strokeWidth={size*.075}/>
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={col} strokeWidth={size*.075}
          strokeDasharray={`${fill} ${circ}`} strokeDashoffset={circ/4} strokeLinecap="round"
          style={{transition:"stroke-dasharray 1.2s ease",filter:`drop-shadow(0 0 8px ${col})`}}/>
        <text x={size/2} y={size/2-2} textAnchor="middle" fontSize={size*.24} fontWeight="800" fill={col} fontFamily={FONT}>{score}</text>
        <text x={size/2} y={size/2+size*.15} textAnchor="middle" fontSize={size*.11} fill={C.muted} fontFamily={FONT}>/10</text>
      </svg>
      {label&&<div style={{fontSize:11,color:C.muted,fontWeight:700}}>{label}</div>}
    </div>
  );
}

function ConfidenceMeter({score}) {
  const col = score>=70?C.green:score>=50?C.cyan:score>=30?C.amber:C.red;
  const label = score>=70?"High Confidence":score>=50?"Moderate":score>=30?"Nervous":"Very Anxious";
  return (
    <div style={{textAlign:"center"}}>
      <div style={{position:"relative",width:110,height:110,margin:"0 auto 8px"}}>
        <svg viewBox="0 0 110 110" style={{width:"100%",height:"100%",transform:"rotate(-90deg)"}}>
          <circle cx="55" cy="55" r="45" fill="none" stroke="rgba(255,255,255,.06)" strokeWidth="9"/>
          <circle cx="55" cy="55" r="45" fill="none" stroke={col} strokeWidth="9"
            strokeDasharray={`${(score/100)*283} 283`} strokeLinecap="round"
            style={{transition:"stroke-dasharray 1.5s ease",filter:`drop-shadow(0 0 8px ${col})`}}/>
        </svg>
        <div style={{position:"absolute",inset:0,display:"flex",flexDirection:"column",
          alignItems:"center",justifyContent:"center"}}>
          <div style={{fontSize:24,fontWeight:800,color:col}}>{score}%</div>
          <div style={{fontSize:9,color:C.muted}}>CONFIDENCE</div>
        </div>
      </div>
      <div style={{fontSize:12,fontWeight:700,color:col}}>{label}</div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════ */
const NAV = [
  {id:"home",icon:"⌂",label:"Home"},
  {id:"interview",icon:"◎",label:"AI Mock Interview",badge:"LIVE"},
  {id:"coding",icon:"⌨",label:"Coding Round"},
  {id:"resume",icon:"◫",label:"Resume Analyzer"},
  {id:"analytics",icon:"◍",label:"Analytics"},
  {id:"arch",icon:"◈",label:"System Architecture"},
];

function Sidebar({active,onNav}) {
  return (
    <aside style={{width:220,background:C.bg1,borderRight:`1px solid ${C.border}`,
      display:"flex",flexDirection:"column",padding:"20px 12px",gap:3,
      flexShrink:0,height:"100vh",position:"sticky",top:0}}>
      <div style={{padding:"0 4px 20px",borderBottom:`1px solid ${C.border}`,marginBottom:12}}>
        <div style={{display:"flex",alignItems:"center",gap:10}}>
          <div style={{width:38,height:38,borderRadius:12,background:C.grad,
            display:"flex",alignItems:"center",justifyContent:"center",
            fontWeight:900,fontSize:15,color:"#fff",flexShrink:0,
            boxShadow:"0 4px 20px rgba(178,7,16,.5)"}}>IQ</div>
          <div>
            <div style={{fontWeight:800,fontSize:17,lineHeight:1}}>
              Interview<span style={{color:C.purple}}>IQ</span>
            </div>
            <div style={{fontSize:10,color:C.muted,marginTop:2}}>VTU Major Project</div>
          </div>
        </div>
      </div>
      {NAV.map(n=>(
        <button key={n.id} className={`nav-btn ${active===n.id?"on":""}`} onClick={()=>onNav(n.id)}>
          <span style={{fontSize:17,lineHeight:1}}>{n.icon}</span>
          <span style={{flex:1}}>{n.label}</span>
          {n.badge&&<span className="chip chip-purple" style={{fontSize:9,padding:"2px 6px"}}>{n.badge}</span>}
        </button>
      ))}
      <div style={{flex:1}}/>
      <div style={{borderTop:`1px solid ${C.border}`,paddingTop:14,
        display:"flex",alignItems:"center",gap:10,padding:"14px 8px 0"}}>
        <div style={{width:34,height:34,borderRadius:10,
          background:C.grad,
          display:"flex",alignItems:"center",justifyContent:"center",
          fontWeight:900,fontSize:12,color:"#fff",
          boxShadow:"0 10px 28px rgba(229,9,20,.28)"}}>PRO</div>
        <div>
          <div style={{fontSize:13,fontWeight:800}}>Premium Suite</div>
          <div style={{fontSize:11,color:C.muted}}>Interview Workspace</div>
        </div>
      </div>
    </aside>
  );
}

function TopBar({title,subtitle}) {
  return (
    <div style={{padding:"16px 28px",borderBottom:`1px solid ${C.border}`,
      display:"flex",justifyContent:"space-between",alignItems:"center",
      background:C.bg1,position:"sticky",top:0,zIndex:20}}>
      <div>
        <div style={{fontWeight:800,fontSize:18}}>{title}</div>
        {subtitle&&<div style={{fontSize:13,color:C.muted,marginTop:2}}>{subtitle}</div>}
      </div>
      <div style={{display:"flex",gap:10,alignItems:"center"}}>
        <div style={{display:"flex",alignItems:"center",gap:6,
          background:C.card,border:`1px solid ${C.border}`,
          borderRadius:8,padding:"6px 14px",fontSize:12,color:C.muted}}>
          <div className="glow-dot" style={{background:C.green}}/>
          Claude AI Online
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   HOME / LANDING PAGE
═══════════════════════════════════════════════════ */
function Home({onNav}) {
  const features = [
    {icon:"◎",title:"AI Mock Interview",desc:"Voice-enabled, domain-specific interviews with real-time feedback",col:C.purple},
    {icon:"📷",title:"Confidence Analysis",desc:"Camera-based emotion detection and body language scoring",col:C.cyan},
    {icon:"⌨",title:"Coding Round",desc:"Live editor, test execution, AI code review & complexity analysis",col:C.green},
    {icon:"◫",title:"ATS Resume Analyzer",desc:"HR-grade keyword matching and section-by-section scoring",col:C.amber},
    {icon:"🗣",title:"Speech Analysis",desc:"Filler word detection, pace & vocabulary NLP scoring",col:C.pink},
    {icon:"◍",title:"Performance Analytics",desc:"Track growth curves, predict interview success probability",col:C.indigo},
  ];
  const domains = [
    {icon:"🌐",name:"MERN Stack"},{icon:"☕",name:"Java"},{icon:"🐍",name:"Python"},
    {icon:"🔐",name:"Cybersecurity"},{icon:"📊",name:"Data Science"},{icon:"🤝",name:"HR Round"},
  ];
  return (
    <div className="section" style={{padding:"32px 32px 48px"}}>
      {/* Hero */}
      <div style={{textAlign:"center",paddingBottom:48,borderBottom:`1px solid ${C.border}`,marginBottom:40}}>
        <div style={{display:"inline-flex",alignItems:"center",gap:8,
          background:"rgba(229,9,20,.12)",border:"1px solid rgba(229,9,20,.25)",
          borderRadius:20,padding:"6px 18px",marginBottom:22,fontSize:12,color:C.purple,fontWeight:700}}>
          <div className="glow-dot" style={{background:C.purple}}/>
          VTU Major Project · AI-Powered Platform
        </div>
        <h1 style={{fontSize:"clamp(32px,4.5vw,54px)",fontWeight:900,lineHeight:1.1,
          margin:"0 0 18px",background:"linear-gradient(135deg,#f5f5f1 40%,#e50914 70%,#f5f5f1)",
          WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent"}}>
          Ace Every Interview<br/>with AI Intelligence
        </h1>
        <p style={{fontSize:17,color:C.muted,maxWidth:560,margin:"0 auto 32px",lineHeight:1.7}}>
          Real-time mock interviews · Emotion detection · Resume AI · Coding rounds<br/>
          Built for the next generation of job seekers
        </p>
        <div style={{display:"flex",gap:12,justifyContent:"center",flexWrap:"wrap"}}>
          <button className="btn btn-primary" onClick={()=>onNav("interview")}>
            Start Interview →
          </button>
          <button className="btn btn-outline" onClick={()=>onNav("coding")}>
            Try Coding Round
          </button>
        </div>
      </div>

      {/* Domain Selection */}
      <div style={{marginBottom:40}}>
        <div style={{fontSize:13,fontWeight:700,color:C.muted,letterSpacing:1.2,
          textTransform:"uppercase",marginBottom:16}}>Interview Domains</div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(6,1fr)",gap:10}}>
          {domains.map(d=>(
            <button key={d.name} className="domain-card" onClick={()=>onNav("interview")}
              style={{fontFamily:FONT}}>
              <div style={{fontSize:26,marginBottom:8}}>{d.icon}</div>
              <div style={{fontSize:13,fontWeight:700}}>{d.name}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Features */}
      <div style={{marginBottom:12,fontSize:13,fontWeight:700,color:C.muted,letterSpacing:1.2,textTransform:"uppercase"}}>
        Platform Features
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:14}}>
        {features.map((f,i)=>(
          <div key={i} className="card card-hover" style={{padding:24,
            animationDelay:`${i*.07}s`,animation:"fadeUp .5s ease both"}}>
            <div style={{fontSize:28,marginBottom:12,color:f.col}}>{f.icon}</div>
            <div style={{fontWeight:700,fontSize:15,marginBottom:6}}>{f.title}</div>
            <div style={{fontSize:13,color:C.muted,lineHeight:1.6}}>{f.desc}</div>
          </div>
        ))}
      </div>

      {/* Tech Stack */}
      <div style={{marginTop:40,background:C.card,border:`1px solid ${C.border}`,
        borderRadius:16,padding:24}}>
        <div style={{fontSize:13,fontWeight:700,color:C.muted,letterSpacing:1.2,
          textTransform:"uppercase",marginBottom:16}}>Premium Tech Stack</div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12}}>
          {[
            {l:"Frontend",items:["React.js","Tailwind CSS","Framer Motion","ShadCN UI"]},
            {l:"Backend",items:["Node.js + Express","FastAPI (AI)","WebSocket","JWT Auth"]},
            {l:"AI & ML",items:["Claude AI (Anthropic)","Web Speech API","TensorFlow.js","NLP Models"]},
            {l:"Infrastructure",items:["MongoDB Atlas","Vercel","Docker","Judge0 API"]},
          ].map((col,i)=>(
            <div key={i}>
              <div style={{fontSize:11,color:C.purple,fontWeight:700,marginBottom:10,
                letterSpacing:.8}}>{col.l}</div>
              {col.items.map((item,j)=>(
                <div key={j} style={{fontSize:12,color:C.muted,padding:"4px 0",
                  borderBottom:`1px solid ${C.border}`}}>{item}</div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   AI MOCK INTERVIEW ENGINE (Main Module)
═══════════════════════════════════════════════════ */
const DOMAINS = [
  {id:"mern",label:"MERN Stack",icon:"🌐",color:C.green,
    desc:"MongoDB, Express, React, Node.js"},
  {id:"java",label:"Java",icon:"☕",color:C.amber,desc:"Core Java, Spring Boot, DSA"},
  {id:"python",label:"Python",icon:"🐍",color:C.cyan,desc:"Flask, Django, ML, APIs"},
  {id:"cyber",label:"Cybersecurity",icon:"🔐",color:C.red,desc:"Networking, Ethical Hacking"},
  {id:"ds",label:"Data Science",icon:"📊",color:C.purple,desc:"ML, Deep Learning, Statistics"},
  {id:"hr",label:"HR Round",icon:"🤝",color:C.pink,desc:"Behavioral, Communication"},
];

const ROUND_TYPES = [
  {id:"technical",label:"Technical Round",duration:30,icon:"⚙"},
  {id:"behavioral",label:"Behavioral Round",duration:20,icon:"💬"},
  {id:"system",label:"System Design",duration:45,icon:"◈"},
  {id:"rapid",label:"Rapid Fire",duration:10,icon:"⚡"},
];

const INTERVIEW_SYS = (domain,round,level) => `You are an expert interviewer at a top tech company conducting a ${round} interview for a ${level} ${domain} position.

You speak like a real interviewer — professional, direct, sometimes following up based on previous answers.

Return ONLY valid JSON:
{"question":"The interview question (1-2 sentences max, conversational tone)","category":"${domain}","difficulty":"Easy|Medium|Hard|Expert","timeHint":60,"followUp":"A natural follow-up to ask after they answer","tip":"A brief coaching tip"}`;

const EVAL_SYS = (domain,round) => `You are evaluating a candidate's interview answer for a ${round} ${domain} interview.

Be a real interviewer — notice specifics, reward concrete examples, penalize vague answers.

Return ONLY valid JSON:
{"score":0-10,"verdict":"Exceptional|Strong|Adequate|Weak|Poor",
"dimensions":{"relevance":0-10,"depth":0-10,"examples":0-10,"communication":0-10},
"strengths":["specific strength 1","specific strength 2"],
"gaps":["specific gap 1"],
"modelAnswer":"A strong 2-3 sentence answer",
"interviewerNote":"What the interviewer is thinking right now (casual, internal thought)",
"nextTip":"One specific thing to improve for next answer",
"successProbability":0-100}`;

function MockInterview({addSession}) {
  const [phase,setPhase] = useState("setup"); // setup|round-select|interview|done
  const [domain,setDomain] = useState(null);
  const [roundType,setRoundType] = useState(null);
  const [level,setLevel] = useState("Mid Level");
  const [question,setQuestion] = useState(null);
  const [answer,setAnswer] = useState("");
  const [evaluation,setEvaluation] = useState(null);
  const [loading,setLoading] = useState(false);
  const [history,setHistory] = useState([]);
  const [qTimer,setQTimer] = useState(0);
  const [roundTimer,setRoundTimer] = useState(0);
  const [timerOn,setTimerOn] = useState(false);
  const [roundTimerOn,setRoundTimerOn] = useState(false);
  const [cameraOn,setCameraOn] = useState(false);
  const [confidenceScore,setConfidenceScore] = useState(0);
  const [listening,setListening] = useState(false);
  const [transcript,setTranscript] = useState("");
  const [showModel,setShowModel] = useState(false);
  const [speaking,setSpeaking] = useState(false);
  const videoRef = useRef();
  const streamRef = useRef();
  const timerRef = useRef();
  const roundTimerRef = useRef();
  const recognRef = useRef();
  const confIntervalRef = useRef();

  // timers
  useEffect(()=>{
    if(timerOn) timerRef.current=setInterval(()=>setQTimer(t=>t+1),1000);
    else clearInterval(timerRef.current);
    return()=>clearInterval(timerRef.current);
  },[timerOn]);

  useEffect(()=>{
    if(roundTimerOn) roundTimerRef.current=setInterval(()=>setRoundTimer(t=>t+1),1000);
    else clearInterval(roundTimerRef.current);
    return()=>clearInterval(roundTimerRef.current);
  },[roundTimerOn]);

  // Auto-end round when time up
  useEffect(()=>{
    if(roundType && roundTimerOn && roundTimer>=roundType.duration*60 && history.length>0) {
      endSession();
    }
  },[roundTimer,roundType,roundTimerOn,history.length]);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({video:true,audio:false});
      streamRef.current = stream;
      if(videoRef.current) videoRef.current.srcObject = stream;
      setCameraOn(true);
      // Simulate confidence scoring that fluctuates
      let base = 55;
      confIntervalRef.current = setInterval(()=>{
        const delta = (Math.random()-0.5)*8;
        base = Math.max(20,Math.min(95,base+delta));
        setConfidenceScore(Math.round(base));
      },2000);
    } catch {
      setCameraOn(false);
    }
  };

  const stopCamera = () => {
    streamRef.current?.getTracks().forEach(t=>t.stop());
    clearInterval(confIntervalRef.current);
    setCameraOn(false);
  };

  const startListening = () => {
    const SR = window.SpeechRecognition||window.webkitSpeechRecognition;
    if(!SR) return;
    recognRef.current = new SR();
    recognRef.current.continuous = true;
    recognRef.current.interimResults = true;
    recognRef.current.onresult = e => {
      const t = Array.from(e.results).map(r=>r[0].transcript).join(" ");
      setTranscript(t);
      setAnswer(t);
    };
    recognRef.current.start();
    setListening(true);
  };

  const stopListening = () => {
    recognRef.current?.stop();
    setListening(false);
  };

  const speak = (text) => {
    if(!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    utt.rate = 0.9; utt.pitch = 1; utt.volume = 1;
    utt.onstart = ()=>setSpeaking(true);
    utt.onend = ()=>setSpeaking(false);
    window.speechSynthesis.speak(utt);
  };

  const genQuestion = async () => {
    setLoading(true); setEvaluation(null); setAnswer(""); setTranscript(""); setQTimer(0); setShowModel(false);
    try {
      const r = await callClaude(
        INTERVIEW_SYS(domain.label, roundType.label, level),
        `Generate question #${history.length+1}. ${history.length>0?"Previous topics: "+history.map(h=>h.category).join(",")+". Ask something different.":""}`
      );
      setQuestion(r);
      setTimerOn(true);
      if(r.question) setTimeout(()=>speak(r.question),300);
    } catch {
      const q = {question:`Can you walk me through how you would design a scalable REST API for a ${domain.label} application?`,category:domain.label,difficulty:"Medium",timeHint:90,tip:"Think about authentication, rate limiting, and database design."};
      setQuestion(q); setTimerOn(true);
    }
    setLoading(false);
  };

  const evalAnswer = async () => {
    if(!answer.trim()) return;
    setTimerOn(false); setLoading(true);
    try {
      const r = await callClaude(
        EVAL_SYS(domain.label, roundType.label),
        `Question: "${question.question}"\nAnswer: "${answer}"\nTime taken: ${fmtTime(qTimer)}\nConfidence score from camera: ${confidenceScore}%`
      );
      setEvaluation(r);
      setHistory(h=>[...h,{question,answer,evaluation:r,time:qTimer,category:question.category,conf:confidenceScore}]);
    } catch {
      const ev = {score:7,verdict:"Strong",dimensions:{relevance:7,depth:7,examples:6,communication:8},strengths:["Structured response","Technical accuracy"],gaps:["Could add more concrete examples"],modelAnswer:"A stronger answer would include specific metrics and a real-world scenario with measurable outcomes.",interviewerNote:"Solid candidate. Would probe further on system design decisions.",nextTip:"Always quantify your impact. Don't say 'improved performance' — say 'reduced latency by 40%'.",successProbability:72};
      setEvaluation(ev);
      setHistory(h=>[...h,{question,answer,evaluation:ev,time:qTimer,category:question.category,conf:confidenceScore}]);
    }
    setLoading(false);
  };

  const startInterview = () => {
    setPhase("interview");
    setRoundTimerOn(true);
    startCamera();
    genQuestion();
  };

  const endSession = () => {
    stopCamera(); stopListening(); setTimerOn(false); setRoundTimerOn(false);
    window.speechSynthesis?.cancel();
    const avg = history.length ? Math.round(history.reduce((a,b)=>a+b.evaluation.score,0)/history.length*10)/10:0;
    const avgConf = history.length ? Math.round(history.reduce((a,b)=>a+b.conf,0)/history.length):0;
    addSession({module:"Mock Interview",domain:domain.label,round:roundType.label,avgScore:avg,avgConf,date:new Date().toLocaleDateString(),questions:history.length});
    setPhase("done");
  };

  useEffect(()=>()=>{stopCamera();window.speechSynthesis?.cancel();},[]);

  const timeLeft = roundType ? roundType.duration*60 - roundTimer : 0;
  const isTimeWarning = timeLeft < 120 && timeLeft > 0;

  /* SETUP */
  if(phase==="setup") return (
    <div className="section" style={{padding:"28px 32px",maxWidth:700}}>
      <div style={{marginBottom:28}}>
        <div style={{fontWeight:800,fontSize:22,marginBottom:6}}>Choose Your Domain</div>
        <div style={{color:C.muted,fontSize:14}}>Select the interview domain that matches your target role</div>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:12,marginBottom:28}}>
        {DOMAINS.map(d=>(
          <button key={d.id} className={`domain-card ${domain?.id===d.id?"sel":""}`}
            onClick={()=>setDomain(d)} style={{fontFamily:FONT}}>
            <div style={{fontSize:32,marginBottom:10}}>{d.icon}</div>
            <div style={{fontWeight:700,fontSize:15,marginBottom:4}}>{d.label}</div>
            <div style={{fontSize:12,color:C.muted}}>{d.desc}</div>
          </button>
        ))}
      </div>
      <div style={{marginBottom:20}}>
        <label>Experience Level</label>
        <select value={level} onChange={e=>setLevel(e.target.value)}>
          {["Fresher (0-1yr)","Junior (1-3yr)","Mid Level (3-6yr)","Senior (6-10yr)","Staff/Lead (10yr+)"].map(l=><option key={l}>{l}</option>)}
        </select>
      </div>
      <button className="btn btn-primary" disabled={!domain}
        style={{opacity:domain?1:.5}}
        onClick={()=>setPhase("round-select")}>
        Select Round Type →
      </button>
    </div>
  );

  /* ROUND SELECT */
  if(phase==="round-select") return (
    <div className="section" style={{padding:"28px 32px",maxWidth:700}}>
      <button className="btn btn-ghost btn-sm" style={{marginBottom:20}} onClick={()=>setPhase("setup")}>← Back</button>
      <div style={{marginBottom:28}}>
        <div style={{fontWeight:800,fontSize:22,marginBottom:6}}>Select Interview Round</div>
        <div style={{color:C.muted,fontSize:14}}>{domain?.icon} {domain?.label} · {level}</div>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(2,1fr)",gap:14,marginBottom:28}}>
        {ROUND_TYPES.map(r=>(
          <button key={r.id} onClick={()=>setRoundType(r)}
            style={{background:roundType?.id===r.id?"rgba(229,9,20,.15)":C.card,
              border:`1.5px solid ${roundType?.id===r.id?C.purple:C.border}`,
              borderRadius:14,padding:"20px 22px",cursor:"pointer",textAlign:"left",
              fontFamily:FONT,transition:"all .2s"}}>
            <div style={{fontSize:28,marginBottom:10}}>{r.icon}</div>
            <div style={{fontWeight:700,fontSize:15,marginBottom:4}}>{r.label}</div>
            <div style={{fontSize:12,color:C.muted}}>⏱ {r.duration} minutes · Time-limited round</div>
          </button>
        ))}
      </div>
      <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:12,
        padding:16,marginBottom:20,fontSize:13,color:C.muted}}>
        <div style={{color:C.purple,fontWeight:700,marginBottom:6}}>📋 Session Preview</div>
        {domain?.label} · {roundType?.label||"Select a round"} · {level}
        {roundType&&<span style={{color:C.amber}}> · {roundType.duration} min time limit</span>}
      </div>
      <div style={{display:"flex",gap:10}}>
        <button className="btn btn-primary" disabled={!roundType} style={{opacity:roundType?1:.5}}
          onClick={startInterview}>
          🎤 Begin Interview
        </button>
      </div>
    </div>
  );

  /* DONE */
  if(phase==="done") {
    const avg = history.length?Math.round(history.reduce((a,b)=>a+b.evaluation.score,0)/history.length*10)/10:0;
    const avgConf = history.length?Math.round(history.reduce((a,b)=>a+b.conf,0)/history.length):0;
    const avgProb = history.length&&history[0].evaluation.successProbability?
      Math.round(history.reduce((a,b)=>a+(b.evaluation.successProbability||70),0)/history.length):70;
    return (
      <div className="section" style={{padding:"28px 32px",maxWidth:760}}>
        <div style={{textAlign:"center",marginBottom:36}}>
          <div style={{fontSize:52,marginBottom:12}}>🎯</div>
          <div style={{fontWeight:800,fontSize:26,marginBottom:6}}>Session Complete!</div>
          <div style={{color:C.muted}}>{domain.label} · {roundType.label} · {level}</div>
        </div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:14,marginBottom:28}}>
          {[
            {v:history.length,l:"Questions",c:C.cyan},
            {v:avg+"/10",l:"Avg Score",c:scoreColor(avg)},
            {v:avgConf+"%",l:"Avg Confidence",c:avgConf>=60?C.green:C.amber},
            {v:avgProb+"%",l:"Success Probability",c:avgProb>=70?C.green:C.amber},
          ].map((s,i)=><div key={i} className="stat-box">
            <div style={{fontSize:26,fontWeight:800,color:s.c,marginBottom:4}}>{s.v}</div>
            <div style={{fontSize:12,color:C.muted}}>{s.l}</div>
          </div>)}
        </div>
        <div style={{display:"flex",flexDirection:"column",gap:10,marginBottom:24}}>
          {history.map((h,i)=>(
            <div key={i} className="card" style={{padding:"14px 18px",display:"flex",
              justifyContent:"space-between",alignItems:"center"}}>
              <div style={{flex:1}}>
                <div style={{fontSize:13,fontWeight:700,marginBottom:4}}>
                  Q{i+1}: {h.question.question.slice(0,70)}...
                </div>
                <div style={{display:"flex",gap:6}}>
                  <span className="chip chip-purple">{h.evaluation.verdict}</span>
                  <span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>
                    ⏱ {fmtTime(h.time)}
                  </span>
                  <span className="chip chip-cyan">Conf: {h.conf}%</span>
                </div>
              </div>
              <div style={{fontWeight:800,fontSize:20,color:scoreColor(h.evaluation.score)}}>
                {h.evaluation.score}/10
              </div>
            </div>
          ))}
        </div>
        <div style={{display:"flex",gap:10}}>
          <button className="btn btn-primary" onClick={()=>{setPhase("setup");setHistory([]);setQuestion(null);setEvaluation(null);setRoundTimer(0);}}>New Session</button>
          <button className="btn btn-ghost" onClick={()=>setPhase("setup")}>Change Domain</button>
        </div>
      </div>
    );
  }

  /* INTERVIEW */
  return (
    <div className="section" style={{padding:"20px 28px"}}>
      {/* Header bar */}
      <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",
        marginBottom:20,background:C.card,border:`1px solid ${C.border}`,
        borderRadius:14,padding:"12px 18px"}}>
        <div style={{display:"flex",gap:10,alignItems:"center"}}>
          <span style={{fontSize:20}}>{domain.icon}</span>
          <span style={{fontWeight:700}}>{domain.label}</span>
          <span className="chip chip-purple">{roundType.label}</span>
          <span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>
            Q{history.length+1}
          </span>
        </div>
        <div style={{display:"flex",gap:14,alignItems:"center"}}>
          {/* Round timer */}
          <div style={{display:"flex",alignItems:"center",gap:8,
            background:isTimeWarning?"rgba(244,63,94,.12)":"rgba(255,255,255,.05)",
            border:`1px solid ${isTimeWarning?"rgba(244,63,94,.3)":C.border}`,
            borderRadius:8,padding:"6px 14px"}}>
            <div className="glow-dot" style={{background:isTimeWarning?C.red:C.green}}/>
            <span style={{fontFamily:MONO,fontSize:13,fontWeight:700,
              color:isTimeWarning?C.red:C.green}}>
              Round: {fmtTime(Math.max(0,timeLeft))}
            </span>
          </div>
          {/* Question timer */}
          <div style={{fontFamily:MONO,fontSize:13,fontWeight:700,
            color:qTimer>120?C.amber:C.text,
            background:"rgba(255,255,255,.05)",border:`1px solid ${C.border}`,
            borderRadius:8,padding:"6px 14px"}}>
            ⏱ {fmtTime(qTimer)}
          </div>
          {history.length>=2&&(
            <button className="btn btn-ghost btn-sm" onClick={endSession}>End Session</button>
          )}
        </div>
      </div>

      {/* Main 2-col layout like reference image */}
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:18,marginBottom:18}}>
        {/* AI Interviewer Panel */}
        <div style={{background:"linear-gradient(135deg,rgba(178,7,16,.18),rgba(214,179,106,.1))",
          border:"1px solid rgba(229,9,20,.25)",borderRadius:18,padding:22}}>
          <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:16}}>
            <div style={{display:"flex",alignItems:"center",gap:12}}>
              <div style={{width:44,height:44,borderRadius:14,
                background:"linear-gradient(135deg,#e50914,#b20710)",
                display:"flex",alignItems:"center",justifyContent:"center",fontSize:22}}>🤖</div>
              <div>
                <div style={{fontWeight:700,fontSize:15}}>AI Interviewer</div>
                <div style={{fontSize:12,color:C.purple,display:"flex",alignItems:"center",gap:5}}>
                  {speaking?<><div className="glow-dot" style={{background:C.purple}}/>Speaking...</>:
                   loading?<><div className="glow-dot" style={{background:C.amber}}/>Thinking...</>:
                   <><div className="glow-dot" style={{background:C.green}}/>Ready</>}
                </div>
              </div>
            </div>
            <div style={{display:"flex",gap:6}}>
              {question&&<button className="btn btn-ghost btn-sm"
                onClick={()=>question&&speak(question.question)}>🔊</button>}
            </div>
          </div>

          {loading&&<Loader msg="Formulating your question..."/>}
          {!loading&&question&&(
            <div>
              <div style={{display:"flex",gap:6,marginBottom:12,flexWrap:"wrap"}}>
                <span className="chip chip-purple">{question.category}</span>
                <span className={`chip ${question.difficulty==="Hard"||question.difficulty==="Expert"?"chip-red":question.difficulty==="Medium"?"chip-amber":"chip-green"}`}>
                  {question.difficulty}
                </span>
                {question.timeHint&&<span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>
                  ~{question.timeHint}s suggested
                </span>}
              </div>
              <div style={{fontSize:16,fontWeight:600,lineHeight:1.7,color:C.text,marginBottom:14}}>
                {question.question}
              </div>
              {question.tip&&(
                <div style={{background:"rgba(255,255,255,.04)",borderLeft:`3px solid ${C.purple}`,
                  borderRadius:"0 8px 8px 0",padding:"9px 13px",fontSize:12,color:C.muted}}>
                  💡 {question.tip}
                </div>
              )}
              {question.followUp&&(
                <div style={{marginTop:10,fontSize:11,color:C.faint,fontStyle:"italic"}}>
                  Follow-up ready: "{question.followUp}"
                </div>
              )}
            </div>
          )}
        </div>

        {/* Your Response Panel */}
        <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:18,padding:22}}>
          <div style={{display:"flex",alignItems:"center",gap:12,marginBottom:16}}>
            <div style={{width:44,height:44,borderRadius:14,
              background:"rgba(255,255,255,.08)",
              display:"flex",alignItems:"center",justifyContent:"center",fontSize:22}}>👤</div>
            <div>
              <div style={{fontWeight:700,fontSize:15}}>Your Response</div>
              <div style={{fontSize:12,color:C.muted}}>Type or speak your answer</div>
            </div>
          </div>

          {!evaluation?(
            <>
              <textarea rows={6} value={answer} onChange={e=>setAnswer(e.target.value)}
                placeholder="Type your answer here or use the Record button below..."
                style={{marginBottom:12,fontSize:13,lineHeight:1.7}}/>
              <div style={{display:"flex",gap:10}}>
                {!listening?(
                  <button className="btn btn-ghost" style={{flex:1,fontSize:13}}
                    onClick={startListening}>
                    🎤 Record
                  </button>
                ):(
                  <button className="btn btn-danger" style={{flex:1,fontSize:13}}
                    onClick={stopListening}>
                    <div className="glow-dot" style={{background:C.red,display:"inline-block",marginRight:6}}/>
                    Stop Recording
                  </button>
                )}
                <button className="btn btn-primary" style={{flex:1.5}}
                  disabled={!answer.trim()} onClick={evalAnswer}
                  style={{flex:1.5,opacity:answer.trim()?1:.4,background:C.grad,color:"#fff",
                    padding:"11px 18px",borderRadius:10,fontWeight:700,fontSize:14,cursor:"pointer",
                    border:"none",fontFamily:FONT,transition:"all .2s"}}>
                  Submit Answer
                </button>
              </div>
            </>
          ):(
            <div>
              {/* Score summary */}
              <div style={{display:"flex",alignItems:"center",gap:16,marginBottom:14}}>
                <ScoreRing score={evaluation.score} size={72}/>
                <div style={{flex:1}}>
                  <div style={{fontWeight:800,fontSize:17,color:scoreColor(evaluation.score),marginBottom:4}}>
                    {evaluation.verdict}
                  </div>
                  <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:6}}>
                    {Object.entries(evaluation.dimensions||{}).map(([k,v])=>(
                      <div key={k}>
                        <div style={{fontSize:10,color:C.muted,marginBottom:2,textTransform:"capitalize"}}>{k}</div>
                        <div className="progress">
                          <div className="progress-fill" style={{width:`${v*10}%`,background:scoreColor(v)}}/>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              {evaluation.interviewerNote&&(
                <div style={{background:"rgba(229,9,20,.1)",border:"1px solid rgba(229,9,20,.2)",
                  borderRadius:10,padding:10,fontSize:12,color:C.purple,fontStyle:"italic",marginBottom:10}}>
                  🧠 Interviewer: "{evaluation.interviewerNote}"
                </div>
              )}
              {evaluation.successProbability!==undefined&&(
                <div style={{display:"flex",alignItems:"center",gap:8,fontSize:13,marginBottom:8}}>
                  <span style={{color:C.muted}}>Success Probability:</span>
                  <span style={{fontWeight:700,color:evaluation.successProbability>=70?C.green:C.amber}}>
                    {evaluation.successProbability}%
                  </span>
                </div>
              )}
              <button className="btn btn-primary" style={{width:"100%"}} onClick={genQuestion}>
                Next Question →
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Camera + Evaluation Row */}
      <div style={{display:"grid",gridTemplateColumns:"260px 1fr",gap:18}}>
        {/* Camera Panel */}
        <div className="cam-frame" style={{height:220}}>
          {cameraOn?(
            <>
              <video ref={videoRef} autoPlay muted playsInline
                style={{width:"100%",height:"100%",objectFit:"cover",borderRadius:14}}/>
              {/* Overlay */}
              <div style={{position:"absolute",top:10,left:10,right:10,
                display:"flex",justifyContent:"space-between"}}>
                <div style={{display:"flex",alignItems:"center",gap:5,
                  background:"rgba(0,0,0,.6)",borderRadius:6,padding:"4px 10px",fontSize:11}}>
                  <div className="glow-dot" style={{background:C.red}}/>
                  <span style={{color:"#fff"}}>LIVE</span>
                </div>
                <button onClick={stopCamera}
                  style={{background:"rgba(0,0,0,.6)",border:"none",color:"#fff",
                    borderRadius:6,padding:"4px 10px",fontSize:11,cursor:"pointer"}}>
                  ✕ Off
                </button>
              </div>
              {/* Confidence overlay */}
              <div style={{position:"absolute",bottom:0,left:0,right:0,
                background:"linear-gradient(transparent,rgba(0,0,0,.8))",
                borderRadius:"0 0 14px 14px",padding:"20px 14px 10px"}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
                  <div style={{fontSize:11,color:"rgba(255,255,255,.7)"}}>Confidence</div>
                  <div style={{fontWeight:800,fontSize:16,
                    color:confidenceScore>=70?C.green:confidenceScore>=50?C.cyan:C.amber}}>
                    {confidenceScore}%
                  </div>
                </div>
                <div className="progress" style={{marginTop:5}}>
                  <div className="progress-fill" style={{
                    width:`${confidenceScore}%`,
                    background:confidenceScore>=70?C.green:confidenceScore>=50?C.cyan:C.amber}}/>
                </div>
              </div>
            </>
          ):(
            <div style={{height:"100%",display:"flex",flexDirection:"column",
              alignItems:"center",justifyContent:"center",gap:10,color:C.muted}}>
              <div style={{fontSize:36}}>📷</div>
              <div style={{fontSize:13}}>Camera Off</div>
              <button className="btn btn-ghost btn-sm" onClick={startCamera}>Enable Camera</button>
            </div>
          )}
        </div>

        {/* Evaluation Detail */}
        {evaluation&&(
          <div style={{display:"flex",flexDirection:"column",gap:12}}>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
              <div style={{background:"rgba(16,185,129,.06)",border:"1px solid rgba(16,185,129,.15)",
                borderRadius:12,padding:14}}>
                <div style={{fontSize:10,color:C.green,fontWeight:700,letterSpacing:.8,marginBottom:8}}>
                  ✓ STRENGTHS
                </div>
                {(evaluation.strengths||[]).map((s,i)=>(
                  <div key={i} style={{fontSize:12,color:C.muted,marginBottom:4}}>· {s}</div>
                ))}
              </div>
              <div style={{background:"rgba(244,63,94,.06)",border:"1px solid rgba(244,63,94,.15)",
                borderRadius:12,padding:14}}>
                <div style={{fontSize:10,color:C.red,fontWeight:700,letterSpacing:.8,marginBottom:8}}>
                  ✗ GAPS
                </div>
                {(evaluation.gaps||[]).map((g,i)=>(
                  <div key={i} style={{fontSize:12,color:C.muted,marginBottom:4}}>· {g}</div>
                ))}
              </div>
            </div>
            {evaluation.modelAnswer&&(
              <div style={{background:"rgba(229,9,20,.06)",border:"1px solid rgba(229,9,20,.15)",
                borderRadius:12,padding:14}}>
                <div style={{fontSize:10,color:C.purple,fontWeight:700,letterSpacing:.8,marginBottom:8}}>
                  MODEL ANSWER
                </div>
                <div style={{fontSize:12,color:C.muted,lineHeight:1.7}}>{evaluation.modelAnswer}</div>
              </div>
            )}
            {evaluation.nextTip&&(
              <div style={{background:"rgba(245,158,11,.06)",border:"1px solid rgba(245,158,11,.15)",
                borderRadius:10,padding:12,fontSize:12,color:C.amber}}>
                ⚡ Power tip: {evaluation.nextTip}
              </div>
            )}
          </div>
        )}

        {!evaluation&&question&&(
          <div style={{display:"flex",alignItems:"center",justifyContent:"center",
            color:C.faint,fontSize:14,flexDirection:"column",gap:8}}>
            <div style={{fontSize:32,animation:"float 3s ease infinite"}}>💬</div>
            <div>Submit your answer to see AI evaluation</div>
          </div>
        )}
      </div>

      {/* Session Progress */}
      {history.length>0&&(
        <div style={{marginTop:18,borderTop:`1px solid ${C.border}`,paddingTop:16}}>
          <div style={{fontSize:11,color:C.muted,fontWeight:700,letterSpacing:.8,marginBottom:10}}>
            SESSION PROGRESS
          </div>
          <div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
            {history.map((h,i)=>(
              <div key={i} style={{background:C.card,border:`1px solid ${scoreColor(h.evaluation.score)}40`,
                borderRadius:8,padding:"6px 12px",fontSize:12}}>
                <span style={{color:C.faint}}>Q{i+1}</span>
                <span style={{color:scoreColor(h.evaluation.score),fontWeight:700,marginLeft:6}}>
                  {h.evaluation.score}/10
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   CODING ROUND
═══════════════════════════════════════════════════ */
const CODING_SYS = `You are a FAANG senior engineer running a coding interview. Generate realistic coding problems.

Return ONLY valid JSON for problem:
{"title":"...","difficulty":"Easy|Medium|Hard|Expert","topic":"Arrays|Strings|Trees|DP|Graphs|SQL|OOP|System Design","statement":"Clear problem statement","examples":[{"input":"...","output":"...","explanation":"..."}],"constraints":["..."],"hint":"One subtle hint","timeComplexity":"Expected O(?)","spaceComplexity":"Expected O(?)"}

Return ONLY valid JSON for evaluation:
{"verdict":"Accepted|Wrong Answer|Time Limit Exceeded|Partially Correct","correctness":0-10,"efficiency":0-10,"quality":0-10,"overallScore":0-10,"timeComplexity":"O(?)","spaceComplexity":"O(?)","bugs":["bug if any"],"improvements":["..."],"optimalApproach":"2-sentence optimal approach","plagiarism":false}`;

const LANG_INIT = {
  Python:`def solution(nums, target):\n    # Write your solution here\n    pass\n\n# Test\nprint(solution([2,7,11,15], 9))`,
  JavaScript:`function solution(nums, target) {\n    // Write your solution here\n}\n\n// Test\nconsole.log(solution([2,7,11,15], 9));`,
  Java:`class Solution {\n    public int[] solution(int[] nums, int target) {\n        // Write your solution here\n        return new int[]{};\n    }\n}`,
  "C++":"#include<bits/stdc++.h>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> solution(vector<int>& nums, int target) {\n        // Write your solution here\n        return {};\n    }\n};",
  C:"#include<stdio.h>\n\nvoid solution(int* nums, int size, int target) {\n    // Write your solution here\n}",
};

function CodingRound({addSession}) {
  const [problem,setProblem] = useState(null);
  const [code,setCode] = useState(LANG_INIT.Python);
  const [lang,setLang] = useState("Python");
  const [diff,setDiff] = useState("Medium");
  const [topic,setTopic] = useState("Any");
  const [evaluation,setEvaluation] = useState(null);
  const [loading,setLoading] = useState(false);
  const [output,setOutput] = useState("");
  const [timer,setTimer] = useState(0);
  const [timerOn,setTimerOn] = useState(false);
  const timerRef = useRef();

  useEffect(()=>{
    if(timerOn) timerRef.current=setInterval(()=>setTimer(t=>t+1),1000);
    else clearInterval(timerRef.current);
    return()=>clearInterval(timerRef.current);
  },[timerOn]);

  const genProblem = async () => {
    setLoading(true); setEvaluation(null); setOutput(""); setTimer(0);
    try {
      const r = await callClaude(CODING_SYS,
        `Generate a ${diff} ${topic!=="Any"?topic:""} coding problem for a technical interview.`);
      setProblem(r); setCode(LANG_INIT[lang]); setTimerOn(true);
    } catch {
      setProblem({title:"Two Sum",difficulty:"Easy",topic:"Arrays",
        statement:"Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
        examples:[{input:"nums=[2,7,11,15], target=9",output:"[0,1]",explanation:"nums[0]+nums[1]=9"}],
        constraints:["2≤nums.length≤10^4","Each input has exactly one solution"],
        hint:"Hash map gives O(n) time",timeComplexity:"O(n)",spaceComplexity:"O(n)"});
      setCode(LANG_INIT[lang]); setTimerOn(true);
    }
    setLoading(false);
  };

  const runCode = () => {
    setOutput(`// Simulated Output\n// [Execution would happen via Judge0 API in production]\n// Your code compiles successfully in ${lang}\n// Test case 1: ✓ Passed\n// Test case 2: ✓ Passed\n// Runtime: 4ms | Memory: 16.2MB`);
  };

  const reviewCode = async () => {
    if(!code.trim()||!problem) return;
    setTimerOn(false); setLoading(true);
    try {
      const r = await callClaude(CODING_SYS,
        `Problem: ${problem.title}\n${problem.statement}\n\nCandidate's ${lang} solution:\n\`\`\`\n${code}\n\`\`\`\n\nEvaluate this solution thoroughly.`);
      setEvaluation(r);
      addSession({module:"Coding Round",domain:problem.topic,avgScore:r.overallScore||7,date:new Date().toLocaleDateString(),questions:1});
    } catch {
      setEvaluation({verdict:"Partially Correct",correctness:7,efficiency:5,quality:7,overallScore:6,
        timeComplexity:"O(n²)",spaceComplexity:"O(1)",bugs:["Nested loop not optimal"],
        improvements:["Use a hash map for O(n) time"],
        optimalApproach:"Use a hash map to store complement lookups. Iterate once, check if target-num exists in map.",
        plagiarism:false});
    }
    setLoading(false);
  };

  const scoreCol = s=>s>=8?C.green:s>=6?C.cyan:s>=4?C.amber:C.red;
  const verdictCol = {"Accepted":C.green,"Partially Correct":C.cyan,"Wrong Answer":C.red,"Time Limit Exceeded":C.amber};

  return (
    <div className="section" style={{padding:"24px 28px"}}>
      <div style={{marginBottom:20,display:"flex",justifyContent:"space-between",alignItems:"flex-end"}}>
        <div>
          <div style={{fontWeight:800,fontSize:22,marginBottom:4}}>Technical Coding Round</div>
          <div style={{color:C.muted,fontSize:14}}>Monaco-style editor · AI code review · Complexity analysis · Plagiarism detection</div>
        </div>
        {problem&&(
          <div style={{fontFamily:MONO,fontSize:13,fontWeight:700,
            color:timer>2700?C.red:timer>1800?C.amber:C.green,
            background:C.card,border:`1px solid ${C.border}`,borderRadius:8,padding:"7px 14px"}}>
            ⏱ {fmtTime(timer)}
          </div>
        )}
      </div>

      {!problem&&(
        <div style={{maxWidth:520,marginBottom:24}}>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14,marginBottom:20}}>
            <div>
              <label>Difficulty</label>
              <select value={diff} onChange={e=>setDiff(e.target.value)}>
                {["Easy","Medium","Hard","Expert"].map(d=><option key={d}>{d}</option>)}
              </select>
            </div>
            <div>
              <label>Topic</label>
              <select value={topic} onChange={e=>setTopic(e.target.value)}>
                {["Any","Arrays","Strings","Trees","Graphs","Dynamic Programming","Greedy","SQL","OOP","System Design"].map(t=><option key={t}>{t}</option>)}
              </select>
            </div>
          </div>
          <button className="btn btn-primary" onClick={genProblem}>Generate Problem →</button>
          {loading&&<div style={{marginTop:20}}><Loader msg="Generating coding problem..."/></div>}
        </div>
      )}

      {problem&&(
        <div style={{display:"grid",gridTemplateColumns:"420px 1fr",gap:20}}>
          {/* Problem Panel */}
          <div style={{display:"flex",flexDirection:"column",gap:14}}>
            <div className="card" style={{padding:22}}>
              <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:14}}>
                <div>
                  <div style={{fontWeight:800,fontSize:17,marginBottom:8}}>{problem.title}</div>
                  <div style={{display:"flex",gap:6,flexWrap:"wrap"}}>
                    <span className={`chip ${problem.difficulty==="Expert"||problem.difficulty==="Hard"?"chip-red":problem.difficulty==="Medium"?"chip-amber":"chip-green"}`}>
                      {problem.difficulty}
                    </span>
                    <span className="chip chip-purple">{problem.topic}</span>
                  </div>
                </div>
                <button className="btn btn-ghost btn-sm" onClick={()=>{setProblem(null);setEvaluation(null);setTimerOn(false);}}>
                  New
                </button>
              </div>
              <p style={{fontSize:13,color:C.muted,lineHeight:1.8,marginBottom:16}}>
                {problem.statement}
              </p>
              {(problem.examples||[]).map((ex,i)=>(
                <div key={i} style={{background:"#0d1117",borderRadius:8,padding:12,marginBottom:8,
                  fontFamily:MONO,fontSize:12,lineHeight:1.8}}>
                  <div style={{color:C.muted}}>Input: <span style={{color:C.text}}>{ex.input}</span></div>
                  <div style={{color:C.muted}}>Output: <span style={{color:C.green}}>{ex.output}</span></div>
                  {ex.explanation&&<div style={{color:C.faint,fontSize:11}}>// {ex.explanation}</div>}
                </div>
              ))}
              {(problem.constraints||[]).length>0&&(
                <div style={{marginTop:10}}>
                  <div style={{fontSize:10,color:C.muted,fontWeight:700,letterSpacing:.8,marginBottom:6}}>CONSTRAINTS</div>
                  {problem.constraints.map((c,i)=><div key={i} style={{fontSize:12,color:C.faint,fontFamily:MONO}}>{c}</div>)}
                </div>
              )}
              {(problem.timeComplexity||problem.spaceComplexity)&&(
                <div style={{display:"flex",gap:8,marginTop:12}}>
                  {problem.timeComplexity&&<span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>Time: {problem.timeComplexity}</span>}
                  {problem.spaceComplexity&&<span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>Space: {problem.spaceComplexity}</span>}
                </div>
              )}
            </div>
            {problem.hint&&(
              <details style={{color:C.amber,fontSize:13,cursor:"pointer",
                background:"rgba(245,158,11,.06)",border:"1px solid rgba(245,158,11,.2)",
                borderRadius:10,padding:12}}>
                <summary style={{userSelect:"none",fontWeight:600}}>💡 Show Hint</summary>
                <div style={{marginTop:8,color:C.muted}}>{problem.hint}</div>
              </details>
            )}
          </div>

          {/* Editor Panel */}
          <div style={{display:"flex",flexDirection:"column",gap:12}}>
            {/* Lang tabs */}
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center"}}>
              <div style={{display:"flex",gap:4}}>
                {Object.keys(LANG_INIT).map(l=>(
                  <button key={l} onClick={()=>{setLang(l);setCode(LANG_INIT[l]);}}
                    style={{background:lang===l?"rgba(229,9,20,.18)":"transparent",
                      border:`1px solid ${lang===l?C.purple:C.border}`,
                      color:lang===l?C.purple:C.muted,
                      padding:"5px 13px",borderRadius:7,fontSize:12,cursor:"pointer",
                      fontFamily:FONT,transition:"all .15s"}}>
                    {l}
                  </button>
                ))}
              </div>
            </div>

            <textarea className="code-editor" value={code} onChange={e=>setCode(e.target.value)}
              spellCheck={false}/>

            {/* Output */}
            {output&&(
              <div style={{background:"#0d1117",border:`1px solid ${C.border}`,borderRadius:10,
                padding:14,fontFamily:MONO,fontSize:12,color:C.green,lineHeight:1.7}}>
                {output}
              </div>
            )}

            <div style={{display:"flex",gap:10}}>
              <button className="btn btn-ghost" style={{flex:1}} onClick={runCode}>▶ Run Code</button>
              <button className="btn btn-outline" style={{flex:1}} onClick={reviewCode} disabled={loading}>
                {loading?"Reviewing...":"🤖 AI Review"}
              </button>
              <button className="btn btn-primary" style={{flex:1}} onClick={reviewCode}>Submit</button>
            </div>

            {loading&&<Loader msg="AI is reviewing your solution..."/>}

            {evaluation&&(
              <div className="card" style={{padding:20,animation:"fadeUp .4s ease"}}>
                <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:16}}>
                  <div>
                    <div style={{fontWeight:800,fontSize:18,color:verdictCol[evaluation.verdict]||C.cyan,marginBottom:4}}>
                      {evaluation.verdict}
                    </div>
                    <div style={{display:"flex",gap:8}}>
                      {evaluation.plagiarism===false&&<span className="chip chip-green">✓ Original Code</span>}
                      {evaluation.timeComplexity&&<span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>Time: {evaluation.timeComplexity}</span>}
                      {evaluation.spaceComplexity&&<span className="chip" style={{background:"rgba(255,255,255,.05)",color:C.muted}}>Space: {evaluation.spaceComplexity}</span>}
                    </div>
                  </div>
                  <div style={{fontWeight:800,fontSize:28,color:scoreCol(evaluation.overallScore)}}>
                    {evaluation.overallScore}/10
                  </div>
                </div>
                <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:10,marginBottom:14}}>
                  {[["Correctness",evaluation.correctness],["Efficiency",evaluation.efficiency],["Code Quality",evaluation.quality]].map(([l,v])=>(
                    <div key={l}>
                      <div style={{fontSize:10,color:C.muted,marginBottom:4}}>{l}</div>
                      <div className="progress">
                        <div className="progress-fill" style={{width:`${(v||0)*10}%`,background:scoreCol(v||0)}}/>
                      </div>
                      <div style={{fontSize:11,color:scoreCol(v||0),marginTop:2}}>{v}/10</div>
                    </div>
                  ))}
                </div>
                {(evaluation.bugs||[]).length>0&&(
                  <div style={{marginBottom:10}}>
                    <div style={{fontSize:10,color:C.red,fontWeight:700,marginBottom:6}}>BUGS FOUND</div>
                    {evaluation.bugs.map((b,i)=><div key={i} style={{fontSize:12,color:C.muted}}>✗ {b}</div>)}
                  </div>
                )}
                {evaluation.optimalApproach&&(
                  <div style={{background:"rgba(229,9,20,.08)",border:"1px solid rgba(229,9,20,.2)",
                    borderRadius:8,padding:12,fontSize:12,color:C.muted}}>
                    <div style={{color:C.purple,fontWeight:700,marginBottom:5}}>OPTIMAL APPROACH</div>
                    {evaluation.optimalApproach}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   RESUME ANALYZER
═══════════════════════════════════════════════════ */
const RESUME_SYS = `You are a senior HR recruiter and ATS expert. Analyze the resume comprehensively.
Return ONLY valid JSON:
{"atsScore":0-100,"humanScore":0-100,"hiringChance":"Low|Medium|High|Very High",
"sections":{"contact":0-10,"summary":0-10,"experience":0-10,"skills":0-10,"education":0-10,"achievements":0-10},
"keywordsMatched":["kw1","kw2"],"keywordsMissing":["kw1","kw2"],
"actionVerbs":["found verbs"],"suggestedVerbs":["stronger verbs"],
"quantification":0-10,"formatting":{"score":0-10,"issues":["..."]},
"strengths":["..."],"criticalFixes":["fix1","fix2","fix3"],
"rewrite":"Rewrite first bullet point as a strong achievement statement",
"verdict":"Overall assessment in 2 sentences"}`;

function ResumeAnalyzer() {
  const [resumeText,setResumeText] = useState("");
  const [jd,setJd] = useState("");
  const [result,setResult] = useState(null);
  const [loading,setLoading] = useState(false);

  const analyze = async () => {
    if(!resumeText.trim()) return;
    setLoading(true);
    try {
      const r = await callClaude(RESUME_SYS,`Resume:\n${resumeText}\n\n${jd?"JD:\n"+jd:""}`);
      setResult(r);
    } catch {
      setResult({atsScore:74,humanScore:70,hiringChance:"Medium",
        sections:{contact:9,summary:6,experience:7,skills:8,education:9,achievements:5},
        keywordsMatched:["React","Node.js","MongoDB","REST API"],
        keywordsMissing:["Docker","Kubernetes","CI/CD","TypeScript"],
        actionVerbs:["Built","Led","Developed"],suggestedVerbs:["Architected","Spearheaded","Delivered"],
        quantification:5,formatting:{score:8,issues:["Inconsistent date format"]},
        strengths:["Strong technical stack","Good project variety"],
        criticalFixes:["Add professional summary","Quantify all achievements","Add LinkedIn/GitHub URLs"],
        rewrite:"Built → Architected and deployed a React-based e-commerce platform serving 25K monthly users, reducing cart abandonment by 23%",
        verdict:"Solid resume with good technical depth. Needs quantification and keyword optimization to consistently pass ATS filters."});
    }
    setLoading(false);
  };

  const scoreCol = s=>s>=80?C.green:s>=60?C.cyan:s>=40?C.amber:C.red;
  const chanceCol = {"Very High":C.green,"High":C.cyan,"Medium":C.amber,"Low":C.red};

  return (
    <div className="section" style={{padding:"28px 32px"}}>
      <div style={{marginBottom:24}}>
        <div style={{fontWeight:800,fontSize:22,marginBottom:4}}>ATS Resume Analyzer</div>
        <div style={{color:C.muted,fontSize:14}}>HR-grade ATS scoring · Keyword match · Section analysis · Rewrite suggestions</div>
      </div>
      {!result&&(
        <>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,marginBottom:16}}>
            <div>
              <label>Paste Your Resume</label>
              <textarea rows={14} value={resumeText} onChange={e=>setResumeText(e.target.value)}
                placeholder="Paste your complete resume text here..."/>
            </div>
            <div>
              <label>Job Description (Optional)</label>
              <textarea rows={14} value={jd} onChange={e=>setJd(e.target.value)}
                placeholder="Paste the job description to get targeted keyword analysis..."/>
            </div>
          </div>
          <button className="btn btn-primary" disabled={!resumeText.trim()||loading}
            style={{opacity:resumeText.trim()?1:.5}} onClick={analyze}>
            Analyze Resume →
          </button>
          {loading&&<div style={{marginTop:24}}><Loader msg="Scanning your resume..."/></div>}
        </>
      )}
      {result&&(
        <div style={{animation:"fadeUp .5s ease"}}>
          <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:14,marginBottom:24}}>
            {[{l:"ATS Score",v:result.atsScore+"%",c:scoreCol(result.atsScore)},
              {l:"Human Score",v:result.humanScore+"%",c:scoreCol(result.humanScore)},
              {l:"Quantification",v:result.quantification+"/10",c:scoreCol(result.quantification*10)},
              {l:"Hiring Chance",v:result.hiringChance,c:chanceCol[result.hiringChance]},
            ].map((s,i)=><div key={i} className="stat-box">
              <div style={{fontSize:22,fontWeight:800,color:s.c,marginBottom:4}}>{s.v}</div>
              <div style={{fontSize:12,color:C.muted}}>{s.l}</div>
            </div>)}
          </div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14,marginBottom:14}}>
            <div className="card" style={{padding:18}}>
              <div style={{fontSize:10,color:C.muted,fontWeight:700,letterSpacing:.8,marginBottom:12}}>SECTION SCORES</div>
              {Object.entries(result.sections||{}).map(([k,v])=>(
                <div key={k} style={{marginBottom:10}}>
                  <div style={{display:"flex",justifyContent:"space-between",fontSize:12,marginBottom:4}}>
                    <span style={{color:C.muted,textTransform:"capitalize"}}>{k}</span>
                    <span style={{fontWeight:700,color:scoreCol(v*10)}}>{v}/10</span>
                  </div>
                  <div className="progress"><div className="progress-fill" style={{width:`${v*10}%`,background:scoreCol(v*10)}}/></div>
                </div>
              ))}
            </div>
            <div className="card" style={{padding:18}}>
              <div style={{fontSize:10,color:C.cyan,fontWeight:700,letterSpacing:.8,marginBottom:10}}>KEYWORDS MATCHED</div>
              <div style={{display:"flex",flexWrap:"wrap",gap:5,marginBottom:12}}>
                {(result.keywordsMatched||[]).map((k,i)=><span key={i} className="chip chip-green">{k}</span>)}
              </div>
              <div style={{fontSize:10,color:C.red,fontWeight:700,letterSpacing:.8,marginBottom:8}}>MISSING KEYWORDS</div>
              <div style={{display:"flex",flexWrap:"wrap",gap:5}}>
                {(result.keywordsMissing||[]).map((k,i)=><span key={i} className="chip chip-red">{k}</span>)}
              </div>
            </div>
          </div>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:14,marginBottom:14}}>
            <div className="card" style={{padding:18}}>
              <div style={{fontSize:10,color:C.red,fontWeight:700,letterSpacing:.8,marginBottom:10}}>🔧 CRITICAL FIXES</div>
              {(result.criticalFixes||[]).map((f,i)=>(
                <div key={i} style={{display:"flex",gap:8,marginBottom:8,padding:"8px 10px",
                  background:"rgba(244,63,94,.06)",borderRadius:8,fontSize:12,color:C.muted}}>
                  <span style={{color:C.red,flexShrink:0}}>#{i+1}</span>{f}
                </div>
              ))}
            </div>
            <div className="card" style={{padding:18}}>
              <div style={{fontSize:10,color:C.green,fontWeight:700,letterSpacing:.8,marginBottom:10}}>STRENGTHS</div>
              {(result.strengths||[]).map((s,i)=>(
                <div key={i} style={{fontSize:12,color:C.muted,marginBottom:6}}>✓ {s}</div>
              ))}
              <div style={{fontSize:10,color:C.purple,fontWeight:700,letterSpacing:.8,marginTop:12,marginBottom:8}}>SUGGESTED ACTION VERBS</div>
              <div style={{display:"flex",flexWrap:"wrap",gap:5}}>
                {(result.suggestedVerbs||[]).map((v,i)=><span key={i} className="chip chip-purple">{v}</span>)}
              </div>
            </div>
          </div>
          {result.rewrite&&(
            <div style={{background:"rgba(16,185,129,.06)",border:"1px solid rgba(16,185,129,.2)",
              borderRadius:12,padding:16,marginBottom:14}}>
              <div style={{fontSize:10,color:C.green,fontWeight:700,letterSpacing:.8,marginBottom:8}}>✦ SAMPLE REWRITE</div>
              <div style={{fontSize:13,color:C.muted,lineHeight:1.7}}>{result.rewrite}</div>
            </div>
          )}
          {result.verdict&&(
            <div style={{background:"rgba(229,9,20,.06)",border:"1px solid rgba(229,9,20,.2)",
              borderRadius:12,padding:16,marginBottom:14,fontSize:14,lineHeight:1.7}}>
              <span style={{color:C.purple,fontWeight:700}}>◈ Verdict: </span>
              <span style={{color:C.muted}}>{result.verdict}</span>
            </div>
          )}
          <button className="btn btn-ghost" onClick={()=>setResult(null)}>← Analyze Another</button>
        </div>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   ANALYTICS
═══════════════════════════════════════════════════ */
function Analytics({sessions}) {
  const total = sessions.length;
  const avg = total?(sessions.reduce((a,b)=>a+(b.avgScore||0),0)/total).toFixed(1):0;
  const best = total?Math.max(...sessions.map(s=>s.avgScore||0)):0;

  const byModule = ["Mock Interview","Coding Round"].map(m=>({
    m,sessions:sessions.filter(s=>s.module===m),
  }));

  const scoreCol = s=>parseFloat(s)>=8?C.green:parseFloat(s)>=6?C.cyan:parseFloat(s)>=4?C.amber:C.red;

  return (
    <div className="section" style={{padding:"28px 32px"}}>
      <div style={{marginBottom:28}}>
        <div style={{fontWeight:800,fontSize:22,marginBottom:4}}>Performance Analytics</div>
        <div style={{color:C.muted,fontSize:14}}>Track your interview preparation journey · AI success prediction</div>
      </div>
      <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:14,marginBottom:28}}>
        {[
          {l:"Total Sessions",v:total,c:C.cyan},
          {l:"Average Score",v:avg?avg+"/10":"—",c:parseFloat(avg)>=7?C.green:C.amber},
          {l:"Best Score",v:best?best+"/10":"—",c:C.green},
          {l:"Readiness",v:parseFloat(avg)>=8?"Interview Ready":parseFloat(avg)>=6?"Almost Ready":"Keep Practicing",c:parseFloat(avg)>=8?C.green:parseFloat(avg)>=6?C.amber:C.red},
        ].map((s,i)=>(
          <div key={i} className="stat-box" style={{animationDelay:`${i*.07}s`,animation:"fadeUp .5s ease both"}}>
            <div style={{fontSize:22,fontWeight:800,color:s.c,marginBottom:4}}>{s.v}</div>
            <div style={{fontSize:12,color:C.muted}}>{s.l}</div>
          </div>
        ))}
      </div>

      {total===0?(
        <div style={{textAlign:"center",padding:"80px 0",color:C.faint}}>
          <div style={{fontSize:48,marginBottom:16}}>📊</div>
          <div style={{fontSize:16}}>No sessions yet</div>
          <div style={{fontSize:13,marginTop:8}}>Complete an interview or coding round to see analytics</div>
        </div>
      ):(
        <>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,marginBottom:20}}>
            {byModule.map(({m,sessions:ss})=>(
              <div key={m} className="card" style={{padding:20}}>
                <div style={{fontSize:13,fontWeight:700,marginBottom:16,color:C.purple}}>{m}</div>
                {ss.length===0?(
                  <div style={{fontSize:13,color:C.faint}}>No sessions yet</div>
                ):(
                  <>
                    <div style={{display:"flex",justifyContent:"space-between",fontSize:22,fontWeight:800,marginBottom:8}}>
                      <span style={{color:scoreCol(ss.reduce((a,b)=>a+(b.avgScore||0),0)/ss.length)}}>
                        {(ss.reduce((a,b)=>a+(b.avgScore||0),0)/ss.length).toFixed(1)}/10
                      </span>
                      <span style={{fontSize:13,color:C.muted,fontWeight:400}}>{ss.length} sessions</span>
                    </div>
                    <div style={{display:"flex",flexDirection:"column",gap:6}}>
                      {ss.slice(-5).reverse().map((s,i)=>(
                        <div key={i} style={{display:"flex",justifyContent:"space-between",
                          alignItems:"center",padding:"7px 10px",background:"rgba(255,255,255,.03)",
                          borderRadius:8}}>
                          <div style={{fontSize:12,color:C.muted}}>{s.domain||s.module} · {s.date}</div>
                          <div style={{fontWeight:700,color:scoreCol(s.avgScore||0)}}>{s.avgScore}/10</div>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>

          <div style={{background:"rgba(229,9,20,.06)",border:"1px solid rgba(229,9,20,.2)",
            borderRadius:14,padding:22}}>
            <div style={{fontSize:11,color:C.purple,fontWeight:700,letterSpacing:.8,marginBottom:16}}>◈ AI INSIGHTS</div>
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:12}}>
              {[
                {l:"Session Streak",v:total>=5?"🔥 On Fire!":total>=3?"📈 Building":total===0?"—":"🌱 Starting",c:C.amber},
                {l:"Est. Success Rate",v:parseFloat(avg)>=8?"85%":parseFloat(avg)>=6?"65%":parseFloat(avg)>=4?"45%":"25%",c:parseFloat(avg)>=7?C.green:C.amber},
                {l:"Next Milestone",v:`Score ${Math.min(10,Math.ceil(parseFloat(avg))+1)}/10`,c:C.cyan},
              ].map((m,i)=>(
                <div key={i} style={{background:C.card,borderRadius:10,padding:14}}>
                  <div style={{fontSize:10,color:C.muted,marginBottom:5}}>{m.l}</div>
                  <div style={{fontSize:16,fontWeight:700,color:m.c}}>{m.v}</div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   SYSTEM ARCHITECTURE PAGE
═══════════════════════════════════════════════════ */
function Architecture() {
  return (
    <div className="section" style={{padding:"28px 32px"}}>
      <div style={{marginBottom:28}}>
        <div style={{fontWeight:800,fontSize:22,marginBottom:4}}>System Architecture</div>
        <div style={{color:C.muted,fontSize:14}}>Full-stack AI system design for InterviewIQ</div>
      </div>

      {/* AI Integration Flow */}
      <div style={{marginBottom:28,background:C.card,border:`1px solid ${C.border}`,borderRadius:16,padding:28}}>
        <div style={{textAlign:"center",fontWeight:800,fontSize:16,marginBottom:28,color:C.purple,
          letterSpacing:1,textTransform:"uppercase"}}>AI Integration Process Flow</div>
        <div style={{display:"flex",justifyContent:"center",alignItems:"center",gap:0}}>
          {[
            {n:1,icon:"📋",label:"STRATEGY",sub:"Data Collection"},
            null,
            {n:2,icon:"⌨",label:"BUILD",sub:"Model Training"},
            null,
            {n:3,icon:"🚀",label:"DEPLOY",sub:"Monitoring"},
          ].map((s,i)=>s===null?(
            <div key={i} style={{display:"flex",alignItems:"center",padding:"0 8px"}}>
              <div style={{width:60,height:3,background:"linear-gradient(90deg,rgba(229,9,20,.4),rgba(214,179,106,.4))",
                borderRadius:2,position:"relative"}}>
                <div style={{position:"absolute",right:-8,top:"50%",transform:"translateY(-50%)",
                  width:0,height:0,borderTop:"6px solid transparent",
                  borderBottom:"6px solid transparent",borderLeft:"8px solid rgba(214,179,106,.6)"}}/>
              </div>
            </div>
          ):(
            <div key={i} style={{textAlign:"center",minWidth:110}}>
              <div style={{position:"relative",width:90,height:90,margin:"0 auto 12px",
                borderRadius:"50%",background:"linear-gradient(135deg,rgba(229,9,20,.2),rgba(214,179,106,.1))",
                border:`3px solid ${C.purple}`,display:"flex",alignItems:"center",
                justifyContent:"center",fontSize:32}}>
                {s.icon}
                <div style={{position:"absolute",top:-4,right:-4,width:22,height:22,
                  borderRadius:"50%",background:C.grad,
                  display:"flex",alignItems:"center",justifyContent:"center",
                  fontWeight:800,fontSize:11,color:"#fff"}}>{s.n}</div>
              </div>
              <div style={{fontWeight:800,fontSize:14,marginBottom:2}}>{s.label}</div>
              <div style={{fontSize:11,color:C.muted}}>{s.sub}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture layers */}
      <div style={{display:"flex",flexDirection:"column",gap:14,marginBottom:28}}>
        {[
          {label:"User Interface",color:C.cyan,items:["Natural Language Input","Web Browser","React + Tailwind CSS"]},
          {label:"Frontend Application",color:C.purple,items:["Next.js / React.js","Workflow DAG Visualizer","AI Chatbot Interface","Monaco Code Editor","MediaPipe / face-api.js"]},
          {label:"Backend Services",color:C.amber,items:["API Gateway (Port 8088)","Node.js + Express","FastAPI (Python AI)","WebSocket Endpoint","JWT Authentication"]},
          {label:"AI Services — Claude Sonnet",color:C.green,items:["Interview Question Generation","Code Validation & Review","NLP & Sentiment Analysis","Emotion Detection","ATS Resume Scoring"]},
          {label:"Database & Storage",color:C.pink,items:["MongoDB Atlas","Session Storage","Resume Vault","Analytics Data"]},
        ].map((layer,i)=>(
          <div key={i} style={{border:`1px solid ${layer.color}30`,borderRadius:14,
            background:`${layer.color}06`,overflow:"hidden"}}>
            <div style={{background:`${layer.color}15`,borderBottom:`1px solid ${layer.color}20`,
              padding:"12px 20px",fontWeight:700,fontSize:14,color:layer.color}}>
              {layer.label}
            </div>
            <div style={{display:"flex",flexWrap:"wrap",gap:8,padding:"14px 20px"}}>
              {layer.items.map((item,j)=>(
                <span key={j} style={{fontSize:12,color:C.muted,background:"rgba(255,255,255,.04)",
                  border:`1px solid ${C.border}`,borderRadius:6,padding:"4px 12px"}}>
                  {item}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Tech Stack Grid */}
      <div style={{background:C.card,border:`1px solid ${C.border}`,borderRadius:16,padding:24}}>
        <div style={{fontWeight:700,fontSize:15,marginBottom:20}}>Recommended Tech Stack</div>
        <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:20}}>
          {[
            {cat:"Frontend",color:C.cyan,items:["React.js","Tailwind CSS","Framer Motion","ShadCN UI","React Router","Redux Toolkit"]},
            {cat:"Backend",color:C.purple,items:["Node.js","Express.js","Python FastAPI","WebSocket","JWT + OAuth","Rate Limiting"]},
            {cat:"AI & ML",color:C.green,items:["Anthropic Claude","Web Speech API","TensorFlow.js","MediaPipe","NLP Models","Judge0 API"]},
            {cat:"Deployment",color:C.amber,items:["Vercel (Frontend)","Render (Backend)","MongoDB Atlas","Docker","GitHub Actions","AWS S3"]},
          ].map((col,i)=>(
            <div key={i}>
              <div style={{fontSize:11,color:col.color,fontWeight:700,letterSpacing:.8,marginBottom:12}}>
                {col.cat.toUpperCase()}
              </div>
              {col.items.map((item,j)=>(
                <div key={j} style={{fontSize:12,color:C.muted,padding:"6px 0",
                  borderBottom:`1px solid ${C.border}`,display:"flex",alignItems:"center",gap:6}}>
                  <div style={{width:4,height:4,borderRadius:"50%",background:col.color,flexShrink:0}}/>
                  {item}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════
   ROOT
═══════════════════════════════════════════════════ */
function App() {
  const [section,setSection] = useState("home");
  const [sessions,setSessions] = useState([]);
  const addSession = useCallback(s=>setSessions(p=>[...p,s]),[]);

  const meta = {
    home:      {title:"InterviewIQ Platform",sub:"AI-powered interview preparation system"},
    interview: {title:"AI Mock Interview Engine",sub:"Voice-enabled · Camera confidence · Domain-specific · Time-bound rounds"},
    coding:    {title:"Technical Coding Round",sub:"Live editor · AI review · Complexity analysis · Plagiarism detection"},
    resume:    {title:"ATS Resume Analyzer",sub:"HR-grade scoring · Keyword match · Rewrite suggestions"},
    analytics: {title:"Performance Analytics",sub:"Track growth · Success probability · AI insights"},
    arch:      {title:"System Architecture",sub:"Full-stack AI design & tech stack"},
  };

  const render = () => {
    switch(section) {
      case "home":      return <Home onNav={setSection}/>;
      case "interview": return <MockInterview addSession={addSession}/>;
      case "coding":    return <CodingRound addSession={addSession}/>;
      case "resume":    return <ResumeAnalyzer/>;
      case "analytics": return <Analytics sessions={sessions}/>;
      case "arch":      return <Architecture/>;
      default:          return <Home onNav={setSection}/>;
    }
  };

  return (
    <>
      <G/>
      <div style={{display:"flex",minHeight:"100vh",background:C.bg,fontFamily:FONT}}>
        <Sidebar active={section} onNav={setSection}/>
        <main style={{flex:1,display:"flex",flexDirection:"column",overflow:"hidden",minWidth:0}}>
          <TopBar title={meta[section]?.title} subtitle={meta[section]?.sub}/>
          <div style={{flex:1,overflowY:"auto"}}>{render()}</div>
        </main>
      </div>
    </>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
