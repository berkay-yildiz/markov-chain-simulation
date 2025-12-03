import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Markov Zinciri Deneyi (2 Durumlu)")

# Kullanıcıdan step sayısı al
n_steps = st.slider(
    "Simülasyon adım sayısı:",
    min_value=100,
    max_value=200_000,
    value=20_000,
    step=100
)

start_button = st.button("Simülasyonu Başlat 🚀")

if start_button:

    # --- Loading Animasyonu ---
    with st.spinner("Simülasyon çalışıyor..."):
        time.sleep(0.5)

    # --- Markov Transition Matrix ---
    P = {
        0: {0: 0.13, 1: 0.87},
        1: {0: 0.67, 1: 0.33}
    }

    # Başlangıç durumu
    state = 0
    states = [state]

    # Simülasyon
    for _ in range(n_steps - 1):
        rand = random.random()
        if rand < P[state][0]:
            state = 0
        else:
            state = 1
        states.append(state)

    # Durum sayıları
    count_0 = states.count(0)
    count_1 = states.count(1)

    p0 = count_0 / n_steps * 100
    p1 = count_1 / n_steps * 100

    # --- Grafik Çizimi ---
    fig, ax = plt.subplots(figsize=(7, 4))

    bars = ax.barh(
        ['Durum 0', 'Durum 1'],
        [p0, p1],
        color=['#4c72b0', '#dd8452'],
        edgecolor='black',
        linewidth=1
    )

    ax.set_xlabel("Yüzde (%)")
    ax.set_title("Markov Zinciri Simülasyonu Sonucu", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", linestyle="--", alpha=0.55)

    # Barların üzerine yüzde yaz
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1,
            bar.get_y() + bar.get_height() / 2,
            f"%{width:.2f}",
            va="center",
            fontsize=10,
            fontweight="bold"
        )

    st.pyplot(fig)

    # Yazılı sonuç
    st.success(f"**Durum 0 oranı:** %{p0:.2f} \n\n **Durum 1 oranı:** %{p1:.2f}")
