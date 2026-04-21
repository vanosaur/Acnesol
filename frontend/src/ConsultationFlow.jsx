import React from 'react';
import { motion } from 'framer-motion';
import { ChevronLeft, ChevronRight, Upload } from 'lucide-react';

const STEPS = [
  { id: 1, section: 'STEP 01 / 07', title: 'Skin Scan' },
  { id: 2, section: 'STEP 02 / 07', title: 'Breakout Pattern' },
  { id: 3, section: 'STEP 03 / 07', title: 'Breakout Pattern' },
  { id: 4, section: 'STEP 04 / 07', title: 'Pain & Experience' },
  { id: 5, section: 'STEP 05 / 07', title: 'Skincare Habits' },
  { id: 6, section: 'STEP 06 / 07', title: 'Skincare Habits' },
  { id: 7, section: 'STEP 07 / 07', title: 'Lifestyle Triggers' },
];

function OptionButton({ label, selected, onClick }) {
  return (
    <button onClick={onClick} style={{
      padding: '14px 20px', borderRadius: '16px', border: `2px solid ${selected ? 'var(--primary)' : 'var(--glass-border)'}`,
      background: selected ? 'var(--primary)' : 'white', color: selected ? 'white' : 'var(--text-muted)',
      fontWeight: 700, cursor: 'pointer', transition: '0.2s', fontSize: '14px', textAlign: 'left', width: '100%'
    }}>
      {label}
    </button>
  );
}

function NavButtons({ onBack, onNext, nextDisabled, nextLabel = 'Continue' }) {
  return (
    <div style={{marginTop: '2.5rem', display: 'flex', gap: '1rem'}}>
      <button onClick={onBack} className="btn-ghost" style={{display: 'flex', alignItems: 'center', gap: '4px'}}>
        <ChevronLeft size={20}/> Back
      </button>
      <button onClick={onNext} disabled={nextDisabled} className="btn-primary" style={{flex:1, justifyContent:'center'}}>
        {nextLabel} <ChevronRight size={20}/>
      </button>
    </div>
  );
}

export default function ConsultationFlow({ step, setStep, formData, setFormData, onAnalyze, error }) {
  const upd = (key, val) => setFormData(f => ({...f, [key]: val}));

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => upd('imageBase64', reader.result);
      upd('image', URL.createObjectURL(file));
      reader.readAsDataURL(file);
    }
  };

  const info = STEPS.find(s => s.id === step) || STEPS[0];

  return (
    <motion.div initial={{opacity:0,x:40}} animate={{opacity:1,x:0}} exit={{opacity:0,x:-40}}
      style={{maxWidth:'580px', width:'100%', padding:'2.5rem'}} className="glass-panel">

      <div style={{fontSize:'11px',fontWeight:800,color:'var(--secondary)',letterSpacing:'0.1em',marginBottom:'8px'}}>{info.section}</div>
      <h2 style={{marginBottom:'0.5rem'}}>{info.title}</h2>

      {error && <div style={{padding:'12px 16px',background:'rgba(255,80,80,0.08)',border:'1px solid rgba(255,80,80,0.2)',borderRadius:'12px',color:'#c0392b',fontSize:'13px',marginBottom:'1.5rem'}}>{error}</div>}

      {/* Step 1: Image Upload */}
      {step === 1 && (
        <>
          <p style={{fontSize:'14px',color:'var(--text-muted)',marginBottom:'1.5rem'}}>Upload a clear photo of the concerned skin area. Use good lighting for better analysis.</p>
          <div style={{position:'relative',border:'2px dashed var(--glass-border)',borderRadius:'24px',padding:'3rem',textAlign:'center',background: formData.image ? 'rgba(74,153,223,0.05)' : 'white'}}>
            {formData.image
              ? <img src={formData.image} style={{maxHeight:'280px',borderRadius:'16px',boxShadow:'0 10px 30px rgba(0,0,0,0.1)'}} alt="Skin Preview"/>
              : <div style={{display:'flex',flexDirection:'column',alignItems:'center',gap:'1rem'}}>
                  <div style={{width:'64px',height:'64px',background:'rgba(74,153,223,0.1)',borderRadius:'50%',display:'flex',alignItems:'center',justifyContent:'center',color:'var(--primary)'}}><Upload size={32}/></div>
                  <p style={{fontWeight:700}}>Upload Photo</p>
                  <p style={{fontSize:'12px',color:'var(--text-light)'}}>JPG, PNG — use clear lighting</p>
                </div>
            }
            <input type="file" accept="image/*" onChange={handleFile} style={{position:'absolute',inset:0,opacity:0,cursor:'pointer'}}/>
          </div>
          <NavButtons onBack={() => setStep(0)} onNext={() => setStep(2)} nextDisabled={!formData.image} nextLabel="Next"/>
        </>
      )}

      {/* Step 2: Duration */}
      {step === 2 && (
        <>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'1.5rem',fontWeight:600}}>How long have you been dealing with this breakout?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
            {['A few days','A few weeks','A few months or more'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.duration===opt} onClick={() => upd('duration', opt)}/>
            ))}
          </div>
          <NavButtons onBack={() => setStep(1)} onNext={() => setStep(3)} nextDisabled={!formData.duration}/>
        </>
      )}

      {/* Step 3: Worsening */}
      {step === 3 && (
        <>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'1.5rem',fontWeight:600}}>Has it been getting worse recently?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
            {['Yes','No','Not sure'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.worsening===opt} onClick={() => upd('worsening', opt)}/>
            ))}
          </div>
          <NavButtons onBack={() => setStep(2)} onNext={() => setStep(4)} nextDisabled={!formData.worsening}/>
        </>
      )}

      {/* Step 4: Pain */}
      {step === 4 && (
        <>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'1.5rem',fontWeight:600}}>Does your acne feel painful or deep?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
            {['Not painful','Slightly painful','Painful / deep'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.pain_level===opt} onClick={() => upd('pain_level', opt)}/>
            ))}
          </div>
          <NavButtons onBack={() => setStep(3)} onNext={() => setStep(5)} nextDisabled={!formData.pain_level}/>
        </>
      )}

      {/* Step 5: Skincare Routine */}
      {step === 5 && (
        <>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'1.5rem',fontWeight:600}}>Do you currently use any skincare products?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
            {['Yes','No'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.skincare_routine===opt} onClick={() => upd('skincare_routine', opt)}/>
            ))}
          </div>
          <NavButtons onBack={() => setStep(4)} onNext={() => setStep(6)} nextDisabled={!formData.skincare_routine}/>
        </>
      )}

      {/* Step 6: New Products */}
      {step === 6 && (
        <>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'1.5rem',fontWeight:600}}>Have you started any new skincare product recently?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
            {['Yes','No'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.new_products===opt} onClick={() => upd('new_products', opt)}/>
            ))}
          </div>
          <NavButtons onBack={() => setStep(5)} onNext={() => setStep(7)} nextDisabled={!formData.new_products}/>
        </>
      )}

      {/* Step 7: Triggers */}
      {step === 7 && (
        <>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'0.5rem',fontWeight:600}}>Have you been more stressed than usual lately?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px',marginBottom:'1.5rem'}}>
            {['Yes','No'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.stress_change===opt} onClick={() => upd('stress_change', opt)}/>
            ))}
          </div>
          <p style={{fontSize:'15px',color:'var(--text-muted)',marginBottom:'0.5rem',fontWeight:600}}>Has your sleep routine changed recently?</p>
          <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
            {['Yes','No'].map(opt => (
              <OptionButton key={opt} label={opt} selected={formData.sleep_change===opt} onClick={() => upd('sleep_change', opt)}/>
            ))}
          </div>
          <NavButtons onBack={() => setStep(6)} onNext={onAnalyze} nextDisabled={!formData.stress_change || !formData.sleep_change} nextLabel="Analyze My Skin"/>
        </>
      )}
    </motion.div>
  );
}
