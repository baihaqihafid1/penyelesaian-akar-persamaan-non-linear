# app.py  - Metode Biseksi Interaktif (Web)  ----------------------------
import math
import streamlit as st
from typing import Callable, List, NamedTuple, Optional, Tuple

# ---------- FUNGSI BISEKSI (sama seperti versi CLI) -------------------
class Step(NamedTuple):
    k: int; a: float; b: float; c: float; f_c: float
    err_abs: Optional[float]; err_rel: Optional[float]

def bisection(
    f: Callable[[float], float],
    a: float,
    b: float,
    e: float = 1e-6,
    imax: int = 100
) -> Tuple[float, List[Step]]:
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError("f(a) dan f(b) harus berlawanan tanda!")

    steps: List[Step] = []
    prev_c = None

    for k in range(1, imax + 1):
        c = (a + b) / 2.0
        fc = f(c)

        err_abs = err_rel = None
        if prev_c is not None:
            err_abs = abs(c - prev_c)
            err_rel = abs(err_abs / c) if c != 0 else None

        steps.append(Step(k, a, b, c, fc, err_abs, err_rel))
        prev_c = c

        # Stop jika error atau residu cukup kecil
        if (err_abs is not None and err_abs < e) or abs(fc) < e:
            return c, steps

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

    return c, steps
# ----------------------------------------------------------------------

st.title("🧮 Metode Biseksi – Iterasi Interaktif")

# -------------- FORM INPUT -------------------------------------------
expr_default = "math.exp(x) + x"      # contoh f(x) = e^x + x
expr = st.text_input("Masukkan fungsi f(x)",
                     value=expr_default,
                     help='Gunakan "x" sebagai variabel, mis. x**3-2*x-5')

cols = st.columns(3)
a = cols[0].number_input("Batas bawah a", value=-1.0)
b = cols[1].number_input("Batas atas b",  value=0.0)
e = cols[2].number_input("Toleransi error (e)", value=1e-6, format="%.1e")

imax = st.slider("Iterasi maksimum", min_value=1, max_value=200, value=50)

# --------- INISIALISASI SESSION STATE --------------------------------
if "steps" not in st.session_state:
    st.session_state.steps = []
    st.session_state.idx = 0
    st.session_state.root = None

# --------- TOMBOL MULAI / RESET --------------------------------------
if st.button("Mulai / Reset"):
    try:
        f = lambda x: eval(expr, {"x": x, "math": math})
        root, steps = bisection(f, a, b, e, imax)
        st.session_state.steps = steps
        st.session_state.idx = 0
        st.session_state.root = root
    except Exception as err:
        st.error(f"Error: {err}")

# --------- TAMPILKAN ITERASI -----------------------------------------
if st.session_state.steps:
    i = st.session_state.idx
    step = st.session_state.steps[i]

    st.subheader(f"Iterasi ke‑{step.k}")

    # ---------- BARIS YANG DIUBAH ---------- #
    st.write(f"a = **{step.a:g}**,  b = **{step.b:g}**")
    # --------------------------------------- #

    st.write(f"c = **{step.c:.10f}**,  f(c) = **{step.f_c:.3e}**")
    if step.err_abs is not None:
        st.write(f"Error abs = **{step.err_abs:.3e}**,  "
                 f"Error rel = **{step.err_rel:.3e}**")

    # --------- NAVIGASI ITERASI --------------------------------------
    cols2 = st.columns(3)
    if cols2[0].button("⬅️ Sebelumnya", disabled=i == 0):
        st.session_state.idx -= 1
    if cols2[2].button("Iterasi Berikutnya ➡️",
                       disabled=i == len(st.session_state.steps) - 1):
        st.session_state.idx += 1

    if i == len(st.session_state.steps) - 1:
        st.success(f"Selesai! Akar ter­aproksimasi ≈ {step.c:.10f}")
