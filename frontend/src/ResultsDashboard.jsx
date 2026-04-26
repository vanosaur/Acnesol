import React, { useState } from 'react';
import { MessageCircle, RefreshCw, Send, Zap, AlertTriangle, CheckCircle, ChevronLeft, Pencil } from 'lucide-react';

const ACNE_TYPES = ['Blackheads', 'Cyst', 'Papules', 'Pustules', 'Whiteheads'];

function Metric({ label, value, highlight }) {
  return (
    <div style={{padding:'12px',background:'white',borderRadius:'16px',border:`1px solid ${highlight ? 'rgba(74,153,223,0.35)' : 'var(--glass-border)'}`,textAlign:'center',background: highlight ? 'rgba(74,153,223,0.05)' : 'white'}}>
      <div style={{fontSize:'9px',fontWeight:800,color:'var(--text-light)',marginBottom:'4px',letterSpacing:'0.05em'}}>{label}</div>
      <div style={{fontSize:'13px',fontWeight:900,color: highlight ? 'var(--primary)' : 'var(--text-main)',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap'}}>{value || 'N/A'}</div>
    </div>
  );
}

function ConfidenceBadge({ label }) {
  const colors = { High: '#22c55e', Medium: '#f59e0b', Low: '#ef4444' };
  const color = colors[label] || '#94a3b8';
  return (
    <span style={{display:'inline-flex',alignItems:'center',gap:'5px',padding:'4px 12px',borderRadius:'20px',background:`${color}18`,border:`1px solid ${color}40`,fontSize:'12px',fontWeight:700,color}}>
      <Zap size={11}/> {label || 'N/A'} Confidence
    </span>
  );
}

function TriggerBadge({ trigger }) {
  const isWarning = trigger && trigger !== 'General Acne Factors';
  return (
    <div style={{display:'flex',alignItems:'center',gap:'8px',padding:'10px 16px',borderRadius:'12px',background: isWarning ? 'rgba(245,158,11,0.08)' : 'rgba(74,153,223,0.06)',border:`1px solid ${isWarning ? 'rgba(245,158,11,0.25)' : 'rgba(74,153,223,0.15)'}`,marginBottom:'1rem'}}>
      {isWarning ? <AlertTriangle size={15} style={{color:'#f59e0b',flexShrink:0}}/> : <CheckCircle size={15} style={{color:'var(--primary)',flexShrink:0}}/>}
      <span style={{fontSize:'13px',fontWeight:700,color: isWarning ? '#92400e' : 'var(--text-main)'}}>Main Trigger: {trigger || 'N/A'}</span>
    </div>
  );
}

export default function ResultsDashboard({ result, chatHistory, chatInput, setChatInput, onChat, isChatLoading, scrollRef, onRestart, onBackToForm, onOverrideType }) {
  const [showOverride, setShowOverride] = useState(false);
  return (
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit, minmax(300px, 1fr))',gap:'2rem',width:'100%',maxWidth:'1200px',alignItems:'start'}} className="p-mobile-0">

      {/* Left panel */}
      <div className="glass-panel p-8 p-mobile-6">
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'flex-start',marginBottom:'1.5rem'}} className="flex-col md:flex-row gap-4">
          <h2 style={{fontSize:'1.5rem'}}>Your Report</h2>
          <div style={{display:'flex', gap:'8px'}} className="w-full md:w-auto">
            <button onClick={onBackToForm} className="btn-ghost" style={{flex:1, fontSize:'11px', fontWeight:800, padding:'8px 12px', border:'1px solid var(--glass-border)', borderRadius:'12px'}}>
              <ChevronLeft size={14}/> BACK TO EDIT
            </button>
            <button onClick={onRestart} className="btn-ghost" style={{flex:1, fontSize:'11px', fontWeight:800, padding:'8px 12px', border:'1px solid var(--glass-border)', borderRadius:'12px', color:'var(--primary)'}}>
              <RefreshCw size={14}/> START NEW
            </button>
          </div>
        </div>

        {/* Confidence + Trigger */}
        <div style={{marginBottom:'1rem'}}>
          <ConfidenceBadge label={result.confidence_label}/>
        </div>
        <TriggerBadge trigger={result.main_trigger}/>

        {/* Metrics */}
        <div style={{gap:'10px',marginBottom:'1.5rem'}} className="grid-2 grid-2-mobile-1">
          <div style={{position:'relative'}}>
            <Metric label="DETECTED TYPE" value={result.predicted_class}/>
            <button 
              onClick={() => setShowOverride(!showOverride)}
              style={{position:'absolute', top:'8px', right:'8px', background:'rgba(74,153,223,0.1)', border:'none', color:'var(--primary)', cursor:'pointer', padding:'4px 8px', borderRadius:'8px', display:'flex', alignItems:'center', gap:'4px'}}
              title="Not correct? Edit type"
            >
              <span style={{fontSize:'10px', fontWeight:800}}>EDIT</span>
              <Pencil size={12}/>
            </button>
            
            {showOverride && (
              <div style={{
                position:'absolute', 
                top:'100%', 
                left:0, 
                right:0, 
                zIndex:100, 
                marginTop:'8px', 
                padding:'12px', 
                background:'#ffffff', 
                borderRadius:'16px', 
                boxShadow:'0 15px 35px rgba(0,0,0,0.2)',
                border:'1px solid var(--glass-border)',
                display:'flex',
                flexDirection:'column',
                gap:'4px'
              }}>
                <p style={{fontSize:'11px', fontWeight:800, marginBottom:'8px', color:'var(--text-muted)'}}>SELECT CORRECT TYPE:</p>
                <div style={{display:'flex', flexDirection:'column', gap:'4px'}}>
                  {ACNE_TYPES.filter(t => t !== result.predicted_class).map(type => (
                    <button 
                      key={type}
                      onClick={() => { onOverrideType(type); setShowOverride(false); }}
                      className="btn-ghost"
                      style={{justifyContent:'flex-start', padding:'8px 12px', fontSize:'13px', textAlign:'left', color:'var(--text-main)', borderRadius:'8px'}}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
          <Metric label="IMAGE SEVERITY" value={result.image_severity}/>
          <Metric label="LIFESTYLE IMPACT" value={result.lifestyle} highlight/>
          <Metric label="PAIN LEVEL" value={result.pain_level}/>
        </div>

        {/* What we considered */}
        <div style={{padding:'1rem 1.25rem',background:'rgba(74,153,223,0.04)',borderRadius:'14px',border:'1px solid rgba(74,153,223,0.1)',marginBottom:'1.5rem'}}>
          <p style={{fontSize:'11px',fontWeight:800,color:'var(--primary)',marginBottom:'8px',letterSpacing:'0.05em'}}>🧠 WHAT WE CONSIDERED</p>
          <div style={{display:'flex',flexWrap:'wrap',gap:'6px'}}>
            {['📸 Image Analysis','📅 Breakout Pattern','💊 Pain Level','🧴 Skincare Habits','🌿 Lifestyle Triggers'].map(tag => (
              <span key={tag} style={{padding:'4px 10px',background:'white',borderRadius:'20px',fontSize:'11px',fontWeight:600,border:'1px solid var(--glass-border)',color:'var(--text-muted)'}}>{tag}</span>
            ))}
          </div>
        </div>

        {/* AI Summary */}
        <div style={{padding:'1.5rem',background:'rgba(74,153,223,0.05)',borderRadius:'16px',border:'1px solid rgba(74,153,223,0.1)'}}>
          <p style={{fontSize:'13px',fontWeight:800,color:'var(--primary)',marginBottom:'10px'}}>AI CONSULTATION REPORT</p>
          <p style={{fontSize:'14px',lineHeight:'1.75',color:'var(--text-main)',whiteSpace:'pre-wrap'}}>{result.final}</p>
        </div>
      </div>

      {/* Chat panel */}
      <div className="glass-panel" style={{height:'min(640px, 80vh)',display:'flex',flexDirection:'column',overflow:'hidden'}}>
        <div style={{padding:'1.25rem 1.5rem',borderBottom:'1px solid var(--glass-border)',fontWeight:800,display:'flex',alignItems:'center',gap:'10px'}}>
          <MessageCircle size={18} style={{color:'var(--primary)'}}/> SKIN ADVISOR CHAT
        </div>
        <div style={{padding:'1rem 1.5rem',background:'rgba(74,153,223,0.04)',borderBottom:'1px solid var(--glass-border)',fontSize:'12px',color:'var(--text-muted)'}}>
          Ask me anything about your results, routine, or products. I know your full consultation profile.
        </div>
        <div ref={scrollRef} style={{flex:1,padding:'1.5rem',overflowY:'auto',display:'flex',flexDirection:'column',gap:'1rem'}}>
          {chatHistory.length === 0 && (
            <div style={{textAlign:'center',color:'var(--text-light)',fontSize:'13px',marginTop:'2rem',fontStyle:'italic'}}>
              Ask a follow-up question about your skin or routine...
            </div>
          )}
          {chatHistory.map((m, i) => (
            <div key={i} style={{
              alignSelf: m.role==='user' ? 'flex-end' : 'flex-start',
              maxWidth:'85%',padding:'12px 16px',borderRadius:'20px',
              background: m.role==='user' ? 'var(--primary)' : 'white',
              color: m.role==='user' ? 'white' : 'var(--text-main)',
              border: m.role==='user' ? 'none' : '1px solid var(--glass-border)',
              fontSize:'14px',whiteSpace:'pre-wrap',lineHeight:'1.6'
            }}>{m.content}</div>
          ))}
          {isChatLoading && <div style={{fontSize:'12px',color:'var(--text-light)',fontStyle:'italic'}}>Advisor is thinking...</div>}
        </div>
        <form onSubmit={onChat} style={{padding:'1rem',background:'rgba(255,255,255,0.5)',borderTop:'1px solid var(--glass-border)',display:'flex',gap:'10px'}}>
          <input value={chatInput} onChange={e => setChatInput(e.target.value)} placeholder="Ask anything..." style={{flex:1,padding:'12px 20px',borderRadius:'30px',border:'1px solid var(--glass-border)',outline:'none',fontSize:'14px'}}/>
          <button type="submit" style={{width:'44px',height:'44px',borderRadius:'50%',background:'var(--primary)',border:'none',color:'white',display:'flex',alignItems:'center',justifyContent:'center',cursor:'pointer'}}><Send size={18}/></button>
        </form>
      </div>
    </div>
  );
}
