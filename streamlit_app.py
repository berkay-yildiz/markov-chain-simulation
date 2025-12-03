import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

st.title("Markov Zinciri Deneyi (Ünlü / Ünsüz)")

st.markdown("""
**Tanım:**  
- `0` → Ünlü harf  
- `1` → Ünsüz harf  

Teorik geçiş olasılıkları (P):  
- Ünlüden ünlüye: **0.13**  
- Ünlüden ünsüze: **0.87**  
- Ünsüzden ünsüze: **0.33**  
- Ünsüzden ünlüye: **0.67**
""")

n_steps = st.slider(
    "Simülasyon adım sayısı:",
    min_value=1_000,
    max_value=500_000,
    value=200_000,
    step=1_000
)

start_button = st.button("Simülasyonu Başlat 🚀")

if start_button:
    # Geçiş matrisi
    P = {
        0: {0: 0.13, 1: 0.87},  # Ünlü
        1: {0: 0.67, 1: 0.33}   # Ünsüz
    }

    # Başlangıç: 0 (ünlü)
    state = 0

    # Geçiş sayaçları
    c_00 = c_01 = c_11 = c_10 = 0

    for _ in range(n_steps - 1):
        prev_state = state
        rand = random.random()
        if rand < P[state][0]:
            state = 0
        else:
            state = 1

        if prev_state == 0 and state == 0:
            c_00 += 1
        elif prev_state == 0 and state == 1:
            c_01 += 1
        elif prev_state == 1 and state == 1:
            c_11 += 1
        elif prev_state == 1 and state == 0:
            c_10 += 1

    # Koşullu geçiş olasılıkları (doğru hesap)
    from_0 = c_00 + c_01
    from_1 = c_11 + c_10

    p_00 = c_00 / from_0 * 100  # P(0->0 | şu an 0)
    p_01 = c_01 / from_0 * 100  # P(0->1 | şu an 0)
    p_11 = c_11 / from_1 * 100  # P(1->1 | şu an 1)
    p_10 = c_10 / from_1 * 100  # P(1->0 | şu an 1)

    st.subheader("1) Simülasyondan Ölçülen Koşullu Geçiş Olasılıkları")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Başlangıç 0 (Ünlü) iken:**")
        st.write(f"- P(0 → 0) ≈ **%{p_00:.2f}**")
        st.write(f"- P(0 → 1) ≈ **%{p_01:.2f}**")
    with col2:
        st.write("**Başlangıç 1 (Ünsüz) iken:**")
        st.write(f"- P(1 → 1) ≈ **%{p_11:.2f}**")
        st.write(f"- P(1 → 0) ≈ **%{p_10:.2f}**")

    # Grafik için etiket ve değerler
    labels = [
        "0→0 (Ünlü→Ünlü)",
        "0→1 (Ünlü→Ünsüz)",
        "1→1 (Ünsüz→Ünsüz)",
        "1→0 (Ünsüz→Ünlü)",
    ]
    percentages = [p_00, p_01, p_11, p_10]

    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.barh(
        labels,
        percentages,
        color=["#4c72b0", "#dd8452", "#55a868", "#c44e52"],
        edgecolor="black",
        linewidth=1
    )

    ax.set_xlabel("Koşullu geçiş olasılığı (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Geçiş Olasılıkları (Simülasyon Sonucu)", fontsize=14, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    for bar, pct in zip(bars, percentages):
        width = bar.get_width()
        ax.text(
            width + 1,
            bar.get_y() + bar.get_height() / 2,
            f"%{pct:.2f}",
            va="center",
            fontsize=10,
            fontweight="bold"
        )

    st.pyplot(fig)


