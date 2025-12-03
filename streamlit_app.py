import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt

st.title("Markov Zinciri Deneyi (Ünlü / Ünsüz)")

st.markdown("""
**Tanım:**  
- `0` → Ünlü harf  
- `1` → Ünsüz harf  

Geçiş olasılıkları (P):  
- Ünlüden ünlüye: **0.13**  
- Ünlüden ünsüze: **0.87**  
- Ünsüzden ünsüze: **0.33**  
- Ünsüzden ünlüye: **0.67**
""")

# Adım sayısı (yazıdaki gibi 200.000 default)
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
    states = [state]

    # Geçiş sayacı (tüm çiftler)
    transition_counts = {
        "0→0 (Ünlü→Ünlü)": 0,
        "0→1 (Ünlü→Ünsüz)": 0,
        "1→1 (Ünsüz→Ünsüz)": 0,
        "1→0 (Ünsüz→Ünlü)": 0,
    }

    # Simülasyon
    for _ in range(n_steps - 1):
        prev_state = state
        rand = random.random()
        if rand < P[state][0]:
            state = 0
        else:
            state = 1
        states.append(state)

        # Geçişi say
        if prev_state == 0 and state == 0:
            transition_counts["0→0 (Ünlü→Ünlü)"] += 1
        elif prev_state == 0 and state == 1:
            transition_counts["0→1 (Ünlü→Ünsüz)"] += 1
        elif prev_state == 1 and state == 1:
            transition_counts["1→1 (Ünsüz→Ünsüz)"] += 1
        elif prev_state == 1 and state == 0:
            transition_counts["1→0 (Ünsüz→Ünlü)"] += 1

    # Durum oranları (tek tek 0 ve 1 sayısı)
    count_0 = states.count(0)
    count_1 = states.count(1)

    p0 = count_0 / n_steps * 100
    p1 = count_1 / n_steps * 100

    st.subheader("1) Durumların (0 / 1) Simülasyondan Çıkan Oranları")
    st.write(f"**0 (Ünlü) oranı:** %{p0:.2f}")
    st.write(f"**1 (Ünsüz) oranı:** %{p1:.2f}")

    # Geçiş olasılıkları (çiftler üzerinden)
    total_transitions = sum(transition_counts.values())
    labels = list(transition_counts.keys())
    percentages = [
        count / total_transitions * 100 for count in transition_counts.values()
    ]

    st.subheader("2) Geçiş Olasılıkları (Simülasyondan Ölçülen)")

    # Bar chart: geçiş olasılıkları
    fig, ax = plt.subplots(figsize=(8, 4))

    bars = ax.barh(labels, percentages, color=["#4c72b0", "#dd8452", "#55a868", "#c44e52"],
                   edgecolor="black", linewidth=1)

    ax.set_xlabel("Yüzde (%)")
    ax.set_xlim(0, 100)
    ax.set_title("Geçiş Olasılıkları (Simülasyon Sonucu)", fontsize=14, fontweight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    # Etiket yaz
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

   
