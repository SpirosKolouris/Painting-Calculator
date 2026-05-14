import streamlit as st

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Pro Painter Estimator",
    page_icon="🎨",
    layout="centered",
)

# ─── Custom CSS (The "Beautiful" Look) ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

.main-header {
    text-align: center;
    padding: 2rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.main-header h1 { color: #f5c842; font-size: 2.6rem; margin-bottom: 0.3rem; }

.section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
}

.result-box {
    background: linear-gradient(135deg, rgba(245,200,66,0.15), rgba(245,200,66,0.05));
    border: 1px solid #f5c842;
    border-radius: 16px;
    padding: 1.8rem;
    margin-top: 1rem;
}

.result-total-value {
    color: #f5c842;
    font-size: 2.2rem;
    font-weight: 700;
    text-align: center;
}

/* Styling Buttons & Inputs */
.stButton > button {
    background: linear-gradient(135deg, #f5c842, #f0a500) !important;
    color: #1a1a2e !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    width: 100% !important;
}
input { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header"><h1>🎨 Pro Painter Estimator</h1><p>Υπολογισμός με Τρέχον Μέτρο (Περίμετρος)</p></div>', unsafe_allow_html=True)

# ─── 1. Wall Settings ──────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🧱 Διαστάσεις Τοίχου")
col1, col2, col3 = st.columns(3)
wall_h = col1.number_input("Ύψος (m)", value=2.0, step=0.1)
wall_w = col2.number_input("Πλάτος (m)", value=10.0, step=0.1)
price_per_m = col3.select_slider("Τιμή €/m", options=[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0], value=6.0)
st.markdown('</div>', unsafe_allow_html=True)

# ─── 2. Openings Section ──────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🪟 Παράθυρα & Πόρτες")

if 'openings' not in st.session_state:
    st.session_state.openings = []

col_add, col_clear = st.columns([2, 1])
if col_add.button("➕ Προσθήκη Ανοίγματος"):
    st.session_state.openings.append({"h": 1.0, "w": 1.0, "qty": 1})
if col_clear.button("🗑️ Καθαρισμός"):
    st.session_state.openings = []
    st.rerun()

total_openings_m = 0.0
for i, op in enumerate(st.session_state.openings):
    c1, c2, c3, c4 = st.columns([1, 1, 1, 0.5])
    op['h'] = c1.number_input(f"Ύψος {i+1}", value=op['h'], key=f"h{i}")
    op['w'] = c2.number_input(f"Πλάτος {i+1}", value=op['w'], key=f"w{i}")
    op['qty'] = c3.number_input(f"Ποσότητα {i+1}", min_value=1, value=op['qty'], key=f"q{i}")
    total_openings_m += (2 * (op['h'] + op['w'])) * op['qty']
st.markdown('</div>', unsafe_allow_html=True)

# ─── 3. Calculations ──────────────────────────────────────────────────────────
wall_m = 2 * (wall_h + wall_w)
total_m = wall_m + total_openings_m
final_cost = total_m * price_per_m

# ─── 4. Result Display ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="result-box">
    <div style="display: flex; justify-content: space-between; color: #e2e8f0; margin-bottom: 8px;">
        <span>Τρέχοντα Μέτρα Τοίχου:</span>
        <span>{wall_m:.2f} m</span>
    </div>
    <div style="display: flex; justify-content: space-between; color: #e2e8f0; margin-bottom: 8px;">
        <span>Τρέχοντα Μέτρα Ανοιγμάτων:</span>
        <span>{total_openings_m:.2f} m</span>
    </div>
    <div style="display: flex; justify-content: space-between; color: #f5c842; font-weight: 600; font-size: 1.1rem; border-top: 1px solid rgba(245,200,66,0.3); padding-top: 10px;">
        <span>Συνολικά Μέτρα:</span>
        <span>{total_m:.2f} m</span>
    </div>
    <div style="margin-top: 20px;">
        <div style="color: #f5c842; text-align: center; font-family: 'Playfair Display'; font-size: 1.2rem;">ΤΕΛΙΚΗ ΤΙΜΗ</div>
        <div class="result-total-value">{final_cost:.2f} €</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── WhatsApp ──────────────────────────────────────────────────────────────────
st.write("")
if st.button("📱 Δημιουργία Προσφοράς για WhatsApp"):
    msg = f"ΠΡΟΣΦΟΡΑ ΕΡΓΑΣΙΑΣ\n----------\n"
    msg += f"Συνολικά τρέχοντα μέτρα: {total_m:.2f}m\n"
    msg += f"Τιμή ανά μέτρο: {price_per_m}€\n"
    msg += f"----------\n"
    msg += f"ΤΕΛΙΚΟ ΠΟΣΟ: {final_cost:.2f}€"
    st.text_area("Αντιγράψτε το κείμενο:", value=msg, height=150)