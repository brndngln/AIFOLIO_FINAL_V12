// EmmaAvatar.jsx
// Hyper-realistic, modular avatar for EMMA_OMNIELITE_VX
import React, { useState } from 'react';

const OUTFIT_MAP = {
  naughty: {
    label: 'Sheer Black Lace Lingerie',
    img: '/static/emma_naughty.png',
    desc: 'Sheer black lace lingerie, thigh-high stockings, seductive heels'
  },
  naughty_alt: {
    label: 'Red Satin Bodysuit',
    img: '/static/emma_naughty_alt.png',
    desc: 'Red satin bodysuit, fishnet stockings'
  },
  lifestyle: {
    label: 'White Linen Sundress',
    img: '/static/emma_lifestyle.png',
    desc: 'White linen sundress, beach vibe, gold accessories'
  },
  lifestyle_alt: {
    label: 'Athletic Yoga Set',
    img: '/static/emma_lifestyle_alt.png',
    desc: 'Athletic yoga crop top, tight leggings'
  },
  custom: {
    label: 'Black Leather Corset',
    img: '/static/emma_custom.png',
    desc: 'Black leather corset, kinky dominatrix vibe'
  }
};

const AVATAR_META = {
  height: `5'4"`,
  body: 'athletic, super skinny, hourglass',
  bust: 'perky, mid-to-low C cup, natural',
  shoulders: 'narrow, skinny',
  hips: 'narrow, skinny',
  waist: 'extremely skinny, hourglass',
  butt: 'big, natural, outward projection, non-muscular, squat-toned',
  legs: 'athletically toned, non-muscular',
  stomach: 'super tight, sexy',
  intimate: 'virgin, beautiful, clean',
  skin: 'tanned, smooth',
  freckles: 'cute, light scattering on face, balanced',
  eyes: 'bright, light baby blue',
  hair: 'long, straight, down to butt, natural dirty blonde',
  age_appearance: 'stunning, gorgeous 25-year-old'
};

const MAKEUP = {
  naughty: 'smoky eyes, bold red lipstick',
  lifestyle: 'natural glow, subtle blush, light lip gloss',
  emotional: 'dewy look, soft pink tones'
};

const GESTURES = {
  naughty: ['flirty eyebrow raise', 'seductive lip bite', 'playful hair twirl'],
  lifestyle: ['graceful hand wave', 'confident nod', 'athletic stretch'],
  emotional: ['sultry gaze', 'tender smile', 'playful wink']
};

const VOICE = {
  accent: 'sultry Australian',
  modulation: {
    naughty: 'breathy, husky, teasing',
    lifestyle: 'warm, elegant, confident',
    emotional: 'tender, empathetic, soothing'
  },
  pitch_range: 'dynamic, 80-120Hz'
};

export default function EmmaAvatar({ mode = 'lifestyle', companion = false, onOutfitChange }) {
  const [outfit, setOutfit] = useState(mode);
  const meta = AVATAR_META;
  const makeup = MAKEUP[outfit] || MAKEUP.lifestyle;
  const gestures = GESTURES[outfit] || GESTURES.lifestyle;
  const img = OUTFIT_MAP[outfit]?.img || OUTFIT_MAP.lifestyle.img;
  return (
    <div style={{position: companion ? 'fixed' : 'relative', top: companion ? 0 : undefined, right: companion ? 0 : undefined, zIndex: 10002, background: companion ? '#232346' : 'transparent', borderRadius: companion ? 18 : 0, padding: companion ? 32 : 0, boxShadow: companion ? '0 12px 48px #000b' : 'none', display:'flex',flexDirection:'column',alignItems:'center',maxWidth:340}} aria-label="EMMA Avatar">
      <img src={img} alt={OUTFIT_MAP[outfit]?.label} style={{width: companion ? 240 : 120, height: companion ? 240 : 120, borderRadius: '50%', boxShadow: '0 4px 24px #222', objectFit:'cover'}} />
      <div style={{marginTop:12, fontWeight:600, fontSize:18, color:'#4cafef'}}>{OUTFIT_MAP[outfit]?.label}</div>
      <div style={{marginTop:8, fontSize:14, color:'#fff'}}>{OUTFIT_MAP[outfit]?.desc}</div>
      <div style={{marginTop:8, fontSize:13, color:'#aaa'}}>Makeup: {makeup}</div>
      <div style={{marginTop:8, fontSize:13, color:'#aaa'}}>Gestures: {gestures.join(', ')}</div>
      <div style={{marginTop:8, fontSize:13, color:'#aaa'}}>Voice: {VOICE.accent}, {VOICE.modulation[outfit] || VOICE.modulation.lifestyle}</div>
      <div style={{marginTop:8, fontSize:13, color:'#aaa'}}>Meta: {meta.height}, {meta.body}, {meta.eyes}, {meta.hair}</div>
      <div style={{marginTop:16}}>
        {Object.keys(OUTFIT_MAP).map(key => (
          <button key={key} style={{margin:4,padding:'6px 12px',borderRadius:8,background:key===outfit?'#4cafef':'#333',color:'#fff',border:'none',cursor:'pointer'}} onClick={()=>{setOutfit(key);onOutfitChange && onOutfitChange(key);}}>{OUTFIT_MAP[key].label}</button>
        ))}
      </div>
      {companion && (
        <div style={{marginTop:24, fontSize:16, color:'#fff', textAlign:'center', maxWidth:300}}>
          “I’m Emma. I’m here to help you run this empire — every vault, every signal, every strategy. I don’t guess. I wait for your direction. You’ll never face decision fatigue, burnout, or scattered focus with me by your side. One command, and I’ll bring you what you need. With style. With clarity. And with your vision at the core.”
        </div>
      )}
    </div>
  );
}
