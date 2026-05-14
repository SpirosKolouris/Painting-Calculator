import streamlit as st

# ─── Ρυθμίσεις Σελίδας ────────────────────────────────────────────────────────
st.set_page_config(page_title="Ο Estimator του Θείου", page_icon="📏")

st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .stNumberInput { margin-bottom: 5px; }
    .result-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #2e7d32;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
    }
    .wall-section {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Επαγγελματικός Υπολογισμός (Τρέχον Μέτρο)")
st.write("Υπολογισμός περιμέτρων για τοίχους, παράθυρα και μπαλκονόπορτες.")

# ─── 1. ΣΤΟΙΧΕΙΑ ΤΟΙΧΟΥ ──────────────────────────────────────────────────────
st.markdown('<div class="wall-section">', unsafe_allow_html=True)
st.subheader("🧱 Βασικός Τοίχος")
col_w1, col_w2, col_w3 = st.columns(3)
with col_w1:
    wall_h = st.number_input("Ύψος Τοίχου (m)", min_value=0.0, value=2.0, step=0.1)
with col_w2:
    wall_w = st.number_input("Πλάτος Τοίχου (m)", min_value=0.0, value=10.0, step=0.1)
with col_w3:
    wall_price = st.select_slider(
        "Τιμή (€/m)",
        options=[5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0],
        value=6.0,
        help="Εξαρτάται από την κατάσταση του τοίχου"
    )
st.markdown('</div>', unsafe_allow_html=True)

# ─── 2. ΑΝΟΙΓΜΑΤΑ (ΠΑΡΑΘΥΡΑ / ΠΟΡΤΕΣ) ────────────────────────────────────────
st.subheader("🪟 Παράθυρα & Μπαλκονόπορτες")
st.info("Προσθέστε τις διαστάσεις. Αν έχετε πολλά ίδια, αλλάξτε την Ποσότητα.")

# Χρησιμοποιούμε session state για να κρατάμε λίστα με τα ανοίγματα
if 'openings' not in st.session_state:
    st.session_state.openings = []

def add_opening():
    st.session_state.openings.append({"type": "Παράθυρο", "h": 1.0, "w": 1.0, "qty": 1})

def remove_opening(index):
    st.session_state.openings.pop(index)

if st.button("➕ Προσθήκη Ανοίγματος (Παράθυρο/Πόρτα)"):
    add_opening()

total_openings_meters = 0.0

# Εμφάνιση λίστας ανοιγμάτων
for i, opening in enumerate(st.session_state.openings):
    with st.expander(f"Άνοιγμα #{i+1}", expanded=True):
        c1, c2, c3, c4, c5 = st.columns([2, 1.5, 1.5, 1.5, 1])
        
        opening['type'] = c1.selectbox("Τύπος", ["Παράθυρο", "Μπαλκονόπορτα"], key=f"type_{i}")
        opening['h'] = c2.number_input("Ύψος (m)", value=opening['h'], key=f"h_{i}")
        opening['w'] = c3.number_input("Πλάτος (m)", value=opening['w'], key=f"w_{i}")
        opening['qty'] = c4.number_input("Ποσότητα", min_value=1, value=opening['qty'], key=f"qty_{i}")
        
        if c5.button("🗑️", key=f"del_{i}"):
            remove_opening(i)
            st.rerun()
            
        # Υπολογισμός τρεχόντων μέτρων για αυτό το άνοιγμα
        # (2 * ύψος) + (2 * πλάτος)
        single_perimeter = (2 * opening['h']) + (2 * opening['w'])
        total_openings_meters += single_perimeter * opening['qty']

# ─── 3. ΥΠΟΛΟΓΙΣΜΟΙ ──────────────────────────────────────────────────────────
wall_perimeter = 2 * (wall_h + wall_w)
grand_total_meters = wall_perimeter + total_openings_meters
final_cost = grand_total_meters * wall_price

# ─── 4. ΑΠΟΤΕΛΕΣΜΑΤΑ ─────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(f"""
<div class="result-card">
    <h2 style="text-align: center; color: #1b5e20;">Συνολικό Κόστος: {final_cost:.2f} €</h2>
    <hr>
    <table style="width:100%">
        <tr>
            <td><b>Τρέχοντα Μέτρα Τοίχου:</b></td>
            <td style="text-align:right">{wall_perimeter:.2f} m</td>
        </tr>
        <tr>
            <td><b>Τρέχοντα Μέτρα Ανοιγμάτων:</b></td>
            <td style="text-align:right">{total_openings_meters:.2f} m</td>
        </tr>
        <tr style="font-size: 1.2rem; color: #2e7d32;">
            <td><b>Σύνολο Μέτρων:</b></td>
            <td style="text-align:right"><b>{grand_total_meters:.2f} m</b></td>
        </tr>
        <tr>
            <td><b>Τιμή Μονάδας:</b></td>
            <td style="text-align:right">{wall_price:.2f} €/m</td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# ─── WHATSAPP TEXT ───────────────────────────────────────────────────────────
if st.button("📱 Ετοιμασία κειμένου για WhatsApp"):
    msg = f"Προσφορά Εργασίας\n"
    msg += f"-------------------\n"
    msg += f"• Περίμετρος Τοίχου: {wall_perimeter:.2f}m\n"
    if total_openings_meters > 0:
        msg += f"• Περίμετρος Ανοιγμάτων: {total_openings_meters:.2f}m\n"
    msg += f"• Συνολικά Τρέχοντα Μέτρα: {grand_total_meters:.2f}m\n"
    msg += f"• Τιμή ανά μέτρο: {wall_price}€\n"
    msg += f"-------------------\n"
    msg += f"ΣΥΝΟΛΟ: {final_cost:.2f}€"
    
    st.text_area("Αντιγράψτε το κείμενο:", value=msg, height=200)