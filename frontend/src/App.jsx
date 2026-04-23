import React, { useState, useEffect, useRef } from 'react';
import { Sparkles, MessageCircle, ChevronRight, ChevronLeft, ShieldCheck, Activity, Upload, RefreshCw, Send, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ConsultationFlow from './ConsultationFlow';
import ResultsDashboard from './ResultsDashboard';

const API_BASE = import.meta.env.VITE_API_URL || '';

const DEFAULT_FORM = {
  duration: '', worsening: '', pain_level: '',
  skincare_routine: '', new_products: '',
  stress_change: '', sleep_change: '',
  image: null, imageBase64: null
};

export default function App() {
  const [step, setStep] = useState(() => { const s = sessionStorage.getItem('acnesol_step'); return s ? parseInt(s, 10) : 0; });
  const [groqKey, setGroqKey] = useState('');
  const [showGroqInput, setShowGroqInput] = useState(true);
  const [formData, setFormData] = useState(() => { const s = sessionStorage.getItem('acnesol_formData'); return s ? JSON.parse(s) : DEFAULT_FORM; });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(() => { const s = sessionStorage.getItem('acnesol_analysisResult'); return s ? JSON.parse(s) : null; });
  const [chatHistory, setChatHistory] = useState(() => { const s = sessionStorage.getItem('acnesol_chatHistory'); return s ? JSON.parse(s) : []; });
  const [chatInput, setChatInput] = useState('');
  const [isChatLoading, setIsChatLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => { if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight; }, [chatHistory]);
  useEffect(() => sessionStorage.setItem('acnesol_step', step), [step]);
  useEffect(() => sessionStorage.setItem('acnesol_formData', JSON.stringify(formData)), [formData]);
  useEffect(() => { if (analysisResult) sessionStorage.setItem('acnesol_analysisResult', JSON.stringify(analysisResult)); }, [analysisResult]);
  useEffect(() => sessionStorage.setItem('acnesol_chatHistory', JSON.stringify(chatHistory)), [chatHistory]);

  const handleAnalyze = async () => {
    setStep(8); setIsLoading(true); setError(null);
    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          duration: formData.duration, worsening: formData.worsening,
          pain_level: formData.pain_level, skincare_routine: formData.skincare_routine,
          new_products: formData.new_products, stress_change: formData.stress_change,
          sleep_change: formData.sleep_change, image_base64: formData.imageBase64,
          groq_api_key: groqKey
        })
      });
      const data = await response.json();
      if (data.success) { setAnalysisResult(data); setStep(9); }
      else throw new Error(data.detail || 'Analysis failed');
    } catch (err) { setError(err.message); setStep(1); }
    finally { setIsLoading(false); }
  };

  const handleChat = async (e) => {
    e.preventDefault();
    if (!chatInput.trim() || isChatLoading) return;
    const userMsg = { role: 'user', content: chatInput };
    setChatHistory(prev => [...prev, userMsg]); setChatInput(''); setIsChatLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.content, history: chatHistory, groq_api_key: groqKey, analysis: analysisResult })
      });
      const data = await res.json();
      if (data.success) setChatHistory(prev => [...prev, { role: 'assistant', content: data.answer }]);
    } catch { setChatHistory(prev => [...prev, { role: 'assistant', content: 'Error connecting to AI.' }]); }
    finally { setIsChatLoading(false); }
  };

  const handleRestart = () => {
    sessionStorage.clear(); setStep(0); setFormData(DEFAULT_FORM);
    setAnalysisResult(null); setChatHistory([]);
  };

  const handleBackToForm = () => {
    setAnalysisResult(null); setStep(7);
  };

  return (
    <div id="root">
      <nav className="p-6 flex justify-between items-center" style={{zIndex: 100}}>
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setStep(0)}>
          <div className="nav-logo-box"><Sparkles size={20} /></div>
          <span style={{fontWeight: 800, fontSize: '1.25rem', letterSpacing: '-0.02em'}}>AcneSol</span>
          <span style={{fontSize: '10px', padding: '4px 10px', background: 'rgba(146,191,232,0.15)', borderRadius: '20px', color: 'var(--primary)', fontWeight: 700, border: '1px solid rgba(146,191,232,0.2)'}}>AI SKINCARE</span>
        </div>
        <div className="flex items-center gap-4">
          {showGroqInput ? (
            <div style={{display:'flex', background:'rgba(255,255,255,0.5)', border:'1px solid var(--glass-border)', padding:'4px 12px', borderRadius:'40px', alignItems:'center', gap:'8px'}}>
              <input type="password" placeholder="Groq API Key (Optional)..." style={{background:'transparent',border:'none',outline:'none',fontSize:'12px',width:'150px'}} value={groqKey} onChange={e => setGroqKey(e.target.value)} />
              <button onClick={() => setShowGroqInput(false)} style={{background:'none',border:'none',color:'var(--primary)',cursor:'pointer'}}><ShieldCheck size={16}/></button>
            </div>
          ) : (
            <button onClick={() => setShowGroqInput(true)} style={{width:'36px',height:'36px',borderRadius:'50%',background:'rgba(74,153,223,0.1)',border:'none',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer',color:'var(--primary)'}}><ShieldCheck size={18}/></button>
          )}
        </div>
      </nav>

      <main className="flex-1 container py-12 flex items-center justify-center" style={{paddingTop:'2rem'}}>
        <AnimatePresence mode="wait">
          {step === 0 && <LandingPage key="landing" onStart={() => setStep(1)} />}
          {step >= 1 && step <= 7 && (
            <ConsultationFlow key="consult" step={step} setStep={setStep} formData={formData} setFormData={setFormData} onAnalyze={handleAnalyze} error={error} />
          )}
          {step === 8 && <AnalyzingState key="analyzing" />}
          {step === 9 && (
            <ResultsDashboard key="results" result={analysisResult} chatHistory={chatHistory} chatInput={chatInput} setChatInput={setChatInput} onChat={handleChat} isChatLoading={isChatLoading} scrollRef={scrollRef} onRestart={handleRestart} onBackToForm={handleBackToForm} />
          )}
        </AnimatePresence>
      </main>

      {step < 9 && (
        <footer className="p-8 text-center" style={{fontSize:'11px',color:'var(--text-light)',fontWeight:600,letterSpacing:'0.1em',borderTop:'1px solid var(--glass-border)'}}>
          © 2025 ACNESOL · INTELLIGENT DERMATOLOGY ASSISTANT
        </footer>
      )}
    </div>
  );
}

function LandingPage({ onStart }) {
  return (
    <motion.div initial={{opacity:0,y:30}} animate={{opacity:1,y:0}} exit={{opacity:0,y:-30}} className="max-w-4xl text-center">
      <div style={{display:'inline-flex',alignItems:'center',gap:'8px',background:'rgba(74,153,223,0.1)',border:'1px solid rgba(74,153,223,0.2)',padding:'6px 16px',borderRadius:'30px',marginBottom:'2rem'}}>
        <Activity size={14} style={{color:'var(--primary)'}}/><span style={{fontSize:'11px',fontWeight:800,letterSpacing:'0.05em',color:'var(--primary)'}}>SKIN INTELLIGENCE ENGINE</span>
      </div>
      <h1>Your AI Partner for <span className="text-gradient">Clear Skin</span></h1>
      <p className="description">AcneSol runs a guided, clinical-style consultation combining image AI with your personal skin history to deliver highly personalized advice.</p>
      <button onClick={onStart} className="btn-primary" style={{margin:'0 auto'}}>Start Consultation <ChevronRight size={20}/></button>
    </motion.div>
  );
}

function AnalyzingState() {
  return (
    <div style={{textAlign:'center'}}>
      <div style={{width:'80px',height:'80px',border:'4px solid rgba(74,153,223,0.2)',borderTopColor:'var(--primary)',borderRadius:'50%',animation:'spin 1s linear infinite',margin:'0 auto 2rem'}}></div>
      <h2>Running Your Consultation...</h2>
      <p style={{color:'var(--text-light)',fontStyle:'italic',marginTop:'0.5rem'}}>Analyzing image, pattern, and lifestyle signals</p>
      <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
