import streamlit as st
import math

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Painting Estimator",
    page_icon="🎨",
    layout="centered",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
}

.stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    min-height: 100vh;
}

/* Header */
.main-header {
    text-align: center;
    padding: 2rem 0 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 2rem;
}
.main-header h1 {
    font-size: 2.6rem;
    color: #f5c842;
    letter-spacing: -1px;
    margin-bottom: 0.3rem;
}
.main-header p {
    color: #a0aec0;
    font-size: 1rem;
    font-weight: 300;
}

/* Section cards */
.section-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.4rem;
    backdrop-filter: blur(10px);
}
.section-title {
    color: #f5c842;
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Result box */
.result-box {
    background: linear-gradient(135deg, rgba(245,200,66,0.15), rgba(245,200,66,0.05));
    border: 1px solid #f5c842;
    border-radius: 16px;
    padding: 1.8rem;
    margin: 1.5rem 0;
}
.result-title {
    color: #f5c842;
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    margin-bottom: 1.2rem;
    text-align: center;
}
.result-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    color: #e2e8f0;
    font-size: 0.95rem;
}
.result-row:last-child { border-bottom: none; }
.result-value {
    font-weight: 600;
    color: #ffffff;
}
.result-total {
    display: flex;
    justify-content: space-between;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 2px solid #f5c842;
}
.result-total-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    color: #f5c842;
}
.result-total-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #f5c842;
    font-weight: 700;
}
.profit-box {
    background: rgba(72,187,120,0.1);
    border: 1px solid rgba(72,187,120,0.4);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-top: 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.profit-label { color: #68d391; font-size: 0.95rem; }
.profit-value { color: #68d391; font-weight: 700; font-size: 1.1rem; }

/* Offer box */
.offer-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 1.5rem;
    white-space: pre-wrap;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.9rem;
    color: #e2e8f0;
    line-height: 1.7;
    margin-top: 1rem;
}

/* Streamlit overrides */
.stSlider > div > div > div { background: #f5c842 !important; }
label { color: #cbd5e0 !important; font-size: 0.9rem !important; }
.stSelectbox label { color: #cbd5e0 !important; }
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.2) !important;
    color: white !important;
}
.stButton > button {
    background: linear-gradient(135deg, #f5c842, #f0a500) !important;
    color: #1a1a2e !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2rem !important;
    font-size: 1rem !important;
    width: 100% !important;
    font-family: 'Source Sans 3', sans-serif !important;
    letter-spacing: 0.5px;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(245,200,66,0.35) !important;
}
.stCheckbox label { color: #cbd5e0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🎨 Smart Painting Estimator</h1>
    <p>Επαγγελματικός Υπολογισμός Κόστους Βαψίματος</p>
</div>
""", unsafe_allow_html=True)

# ─── Editable Pricing Settings ────────────────────────────────────────────────
with st.expander("⚙️ Ρυθμίσεις Τιμών & Κατηγοριών", expanded=False):
    st.markdown("##### 💶 Τιμές Εργασίας & Υλικών")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        LABOR_BASE_PER_M2 = st.number_input(
            "Εργασία (€/m²)", min_value=0.5, max_value=50.0, value=6.0, step=0.5,
            help="Βασική τιμή εργασίας ανά τετραγωνικό μέτρο"
        )
        MATERIAL_PER_M2 = st.number_input(
            "Υλικά (€/m²)", min_value=0.0, max_value=30.0, value=3.5, step=0.5,
            help="Κόστος υλικών (χρώμα, στόκος, αστάρι) ανά m²"
        )
    with col_p2:
        PROFIT_MARGIN_PCT = st.number_input(
            "Κέρδος (%)", min_value=0, max_value=100, value=25, step=1,
            help="Ποσοστό κέρδους επί του συνολικού κόστους"
        )

    st.markdown("##### 🧱 Πολλαπλασιαστές Κατάστασης Τοίχου")
    st.caption("Ορίζουν πόσο αυξάνεται η τιμή εργασίας ανάλογα με την κατάσταση")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        mult_good = st.number_input("Καλή 😊 (×)", min_value=0.5, max_value=3.0, value=1.0, step=0.05)
    with col_c2:
        mult_medium = st.number_input("Μέτρια 😐 (×)", min_value=0.5, max_value=3.0, value=1.25, step=0.05)
    with col_c3:
        mult_bad = st.number_input("Κακή 😟 (×)", min_value=0.5, max_value=3.0, value=1.60, step=0.05)

    st.markdown("##### 👤 Στοιχεία Επαγγελματία (για προσφορά)")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        your_name = st.text_input("Το όνομά σου", placeholder="π.χ. Νίκος Μαραγκός")
    with col_b2:
        your_phone = st.text_input("Τηλέφωνο", placeholder="π.χ. 6912345678")

CONDITION_MULTIPLIER = {
    "Καλή 😊": mult_good,
    "Μέτρια 😐": mult_medium,
    "Κακή 😟": mult_bad,
}

# ─── Inputs ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📐 Διαστάσεις Δωματίου</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    length = st.slider("Μήκος (m)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
with col2:
    width = st.slider("Πλάτος (m)", min_value=1.0, max_value=20.0, value=4.0, step=0.5)
with col3:
    height = st.slider("Ύψος (m)", min_value=2.0, max_value=5.0, value=2.7, step=0.1)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card"><div class="section-title">🧱 Κατάσταση & Επιλογές</div>', unsafe_allow_html=True)

col4, col5 = st.columns(2)
with col4:
    wall_condition = st.selectbox(
        "Κατάσταση Τοίχου",
        options=list(CONDITION_MULTIPLIER.keys()),
        index=0
    )
with col5:
    include_materials = st.checkbox("✅ Συμπερίληψη Υλικών στην προσφορά", value=True)

client_name = st.text_input("Όνομα Πελάτη (για την προσφορά)", placeholder="π.χ. Γιώργης Παπαδόπουλος")
st.markdown('</div>', unsafe_allow_html=True)

# ─── Calculations ──────────────────────────────────────────────────────────────
# Εμβαδόν τοίχων (4 τοίχοι) + οροφή
wall_area = 2 * (length + width) * height
ceiling_area = length * width
total_area = wall_area + ceiling_area

multiplier = CONDITION_MULTIPLIER[wall_condition]

labor_cost = total_area * LABOR_BASE_PER_M2 * multiplier
material_cost = total_area * MATERIAL_PER_M2 if include_materials else 0.0
base_cost = labor_cost + material_cost

profit_amount = base_cost * (PROFIT_MARGIN_PCT / 100)
final_price = base_cost + profit_amount

# ─── Results display ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="result-box">
    <div class="result-title">📊 Ανάλυση Κόστους</div>
    <div class="result-row">
        <span>Εμβαδόν Τοίχων</span>
        <span class="result-value">{wall_area:.1f} m²</span>
    </div>
    <div class="result-row">
        <span>Εμβαδόν Οροφής</span>
        <span class="result-value">{ceiling_area:.1f} m²</span>
    </div>
    <div class="result-row">
        <span>Συνολικό Εμβαδόν</span>
        <span class="result-value">{total_area:.1f} m²</span>
    </div>
    <div class="result-row">
        <span>Κόστος Εργασίας <small style="color:#a0aec0">(×{multiplier} κατάσταση)</small></span>
        <span class="result-value">{labor_cost:.2f} €</span>
    </div>
    <div class="result-row">
        <span>Κόστος Υλικών</span>
        <span class="result-value">{"" if include_materials else "—  "}{material_cost:.2f} € {"✅" if include_materials else "❌"}</span>
    </div>
    <div class="result-row">
        <span>Βασικό Κόστος</span>
        <span class="result-value">{base_cost:.2f} €</span>
    </div>
    <div class="result-total">
        <span class="result-total-label">💰 Τελική Τιμή Πελάτη</span>
        <span class="result-total-value">{final_price:.2f} €</span>
    </div>
    <div class="profit-box">
        <span class="profit-label">📈 Κέρδος σου ({PROFIT_MARGIN_PCT}%)</span>
        <span class="profit-value">+{profit_amount:.2f} €</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── WhatsApp Offer Button ──────────────────────────────────────────────────────
st.markdown("### 📱 Επαγγελματική Προσφορά για WhatsApp")

if st.button("✉️ Δημιούργησε Προσφορά"):
    name_line = f"Αγαπητέ/ή {client_name}," if client_name.strip() else "Αγαπητέ/ή πελάτη,"
    materials_line = (
        f"✅ Συμπεριλαμβάνονται υλικά (χρώματα, στόκος, αστάρι)"
        if include_materials
        else "❌ Χωρίς υλικά (εργασία μόνο)"
    )
    condition_clean = wall_condition.split(" ")[0]  # αφαιρεί emoji

    offer_text = f"""
{name_line}

Σας αποστέλλω την προσφορά μας για τη βαφή του χώρου σας:

━━━━━━━━━━━━━━━━━━━━
🏠 ΛΕΠΤΟΜΕΡΕΙΕΣ ΧΩΡΟΥ
━━━━━━━━━━━━━━━━━━━━
📏 Διαστάσεις: {length}m × {width}m × {height}m ύψος
📐 Συνολικό εμβαδόν: {total_area:.1f} m²
🧱 Κατάσταση τοίχων: {condition_clean}

━━━━━━━━━━━━━━━━━━━━
💼 ΑΝΑΛΥΣΗ ΠΡΟΣΦΟΡΑΣ
━━━━━━━━━━━━━━━━━━━━
🔧 Εργασία: {labor_cost:.2f} €
{materials_line}
💰 Συνολικό κόστος: {base_cost:.2f} €

━━━━━━━━━━━━━━━━━━━━
✨ ΤΕΛΙΚΗ ΤΙΜΗ: {final_price:.2f} €
━━━━━━━━━━━━━━━━━━━━

📋 Η τιμή περιλαμβάνει:
• Πλήρη προετοιμασία επιφανειών
• Επαγγελματική εφαρμογή χρώματος (2 στρώσεις)
• Καθαρισμός χώρου μετά το τέλος
• Εγγύηση εργασίας

📞 Για οποιαδήποτε απορία είμαι στη διάθεσή σας!

Με εκτίμηση,
{your_name if your_name.strip() else "[Το Όνομά σου]"}
{your_phone if your_phone.strip() else "[Τηλέφωνο]"}
""".strip()

    st.markdown(f'<div class="offer-box">{offer_text}</div>', unsafe_allow_html=True)
    st.success("✅ Αντέγραψε το κείμενο και επικόλλησέ το στο WhatsApp!")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#4a5568; font-size:0.8rem; margin-top:3rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.05);">
    Smart Painting Estimator • Κατασκευάστηκε με Streamlit 🎨
</div>
""", unsafe_allow_html=True)
