import streamlit as st
import html, os, urllib.request, json
st.set_page_config(page_title="Wakimbizi AI — Msaada kwa Wakimbizi Kenya", page_icon="🌍", layout="centered")
st.markdown("""<style>.stApp{background:#0a0c10;color:#e8edf5}
.w-card{background:#0d1117;border:1px solid #30363d;border-radius:10px;padding:14px 18px;margin:8px 0}
.stButton>button{background:#0d47a1;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)
def _secret(name):
    """Read a Streamlit secret, falling back to the environment; never crash when no secrets file exists."""
    try:
        v = st.secrets.get(name)
    except Exception:
        v = None
    return v or os.environ.get(name, "")

API_KEY = _secret("GOOGLE_API_KEY") or _secret("GEMINI_API_KEY")
MODEL = _secret("GEMINI_MODEL") or "gemini-3.5-flash-lite"  # the 1.5 Flash model this app used was retired by Google
# ── Public-facing service availability check ──────────────────────────────────
if not API_KEY:
    st.warning(
        "⚠️ **Huduma hii haipo tayari katika toleo hili la majaribio.**\n\n"
        "Tunaendelea kuboresha. Rudi baadaye au wasiliana na msimamizi.\n\n"
        "_This service is not yet available in this demo version. "
        "We are working on it — please check back soon._"
    )
    st.stop()

SYS = "Wewe ni mshauri wa haki za wakimbizi Kenya. Jibu kwa Kiswahili na Kiingereza. Toa habari za UNHCR, Refugee Act Kenya, haki za kisheria, na huduma zinazofaa. Kuwa na huruma."
def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
    body={"contents":[{"role":"user","parts":[{"text":q}]}],"systemInstruction":{"parts":[{"text":SYS}]},"generationConfig":{"temperature":0.2,"maxOutputTokens":700}}
    try:
        req=urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","x-goog-api-key":API_KEY},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r: return html.escape(json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"])
    except Exception as e: return html.escape(f"❌ {e}")
st.markdown("# 🌍 Wakimbizi AI"); st.markdown("**Msaada kwa Wakimbizi na Waomba Hifadhi Kenya**")
st.info("Kenya inachukua wakimbizi 500,000+ kutoka Somalia, South Sudan, DRC, na nchi nyingine.")
tab1,tab2,tab3=st.tabs(["📋 Usajili wa UNHCR","⚖️ Haki za Kisheria","🏥 Huduma za Muhimu"])
with tab1:
    q_reg=st.selectbox("Swali lako:",["Jinsi ya kusajiliwa UNHCR Kenya","Nini kinatokea baada ya usajili","Ninaweza kwenda Nairobi kutoka Kakuma?","Muda wa kusubiri — resettlement","Hati zangu zimepotea — nifanye nini"])
    if st.button("📋 Niambie",key="w1"):
        with st.spinner("..."): r=ask(q_reg+" Kenya UNHCR Refugee Act 2021.")
        st.markdown(f'<div class="w-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab2:
    q_legal=st.selectbox("Haki yako:",["Haki zangu kama mkimbizi Kenya","Je, ninaweza kufanya kazi Kenya?","Watoto wangu wanaweza kwenda shule?","Polisi wananizuia bila sababu — nifanye nini","Kupata hati za kusafiri (travel document)"])
    if st.button("⚖️ Haki Zangu",key="w2"):
        with st.spinner("..."): r=ask(q_legal+" chini ya Kenya Refugee Act 2021 na 1951 Refugee Convention.")
        st.markdown(f'<div class="w-card">{r.replace(chr(10),"<br>")}</div>',unsafe_allow_html=True)
with tab3:
    st.markdown("### Mawasiliano Muhimu")
    contacts=[("UNHCR Kenya","Helpline 1517 (bure, saa 24, lugha nyingi)","help.unhcr.org/kenya"),
              ("DRC Kenya","Danish Refugee Council — angalia drc.ngo","drc.ngo"),
              ("IRC Kenya","Int'l Rescue Committee — angalia rescue.org","rescue.org/kenya"),
              ("Kituo cha Sheria","Legal Aid: +254 20 387 4191","kituochasheria.or.ke"),
              ("NRC Kenya","Norwegian RC: nairobi@nrc.no","nrc.no/kenya")]
    for name,phone,web in contacts:
        st.markdown(f'<div class="w-card"><b>{name}</b><br>📞 {phone} | 🌐 {web}</div>',unsafe_allow_html=True)
st.markdown("---"); st.caption("🌍 Wakimbizi AI v1.0 | UNHCR: unhcr.org/kenya | Habari za elimu tu | MIT")
