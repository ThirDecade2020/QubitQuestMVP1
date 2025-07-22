import streamlit as st
import inspect
from braket.circuits import Circuit
from braket.devices import LocalSimulator
from braket.aws import AwsDevice

# ————— Lesson Builders —————

def build_measure():
    """def build():
    circuit = Circuit()
    circuit.measure(0)
    return circuit
    """
    circuit = Circuit()
    circuit.measure(0)
    return circuit


def build_hadamard():
    """def build():
    circuit = Circuit()
    circuit.h(0)
    circuit.measure(0)
    return circuit
    """
    circuit = Circuit()
    circuit.h(0)
    circuit.measure(0)
    return circuit


def build_pauli_x():
    """def build():
    circuit = Circuit()
    circuit.x(0)
    circuit.measure(0)
    return circuit
    """
    circuit = Circuit()
    circuit.x(0)
    circuit.measure(0)
    return circuit


def build_cnot():
    """def build():
    circuit = Circuit()
    circuit.cnot(0, 1)
    circuit.measure(0)
    circuit.measure(1)
    return circuit
    """
    circuit = Circuit()
    circuit.cnot(0, 1)
    circuit.measure(0)
    circuit.measure(1)
    return circuit

# ————— Lessons Dictionary —————
LESSONS = {
    "Measurement Gate (M)": {
        "builder": build_measure,
        "latex": r"M = |0\rangle\langle0| + |1\rangle\langle1|",
        "description": "Measure qubit 0: collapse its state to 0 or 1 and record the result."
    },
    "Hadamard Gate (H)": {
        "builder": build_hadamard,
        "latex": r"H = \frac1{\sqrt2}\begin{pmatrix}1 & 1\\1 & -1\end{pmatrix}",
        "description": "Creates an equal superposition: H|0⟩ = (|0⟩ + |1⟩)/√2"
    },
    "Pauli‑X Gate (X)": {
        "builder": build_pauli_x,
        "latex": r"X = \begin{pmatrix}0 & 1\\1 & 0\end{pmatrix}",
        "description": "Bit‑flip: X|0⟩ → |1⟩, X|1⟩ → |0⟩"
    },
    "CNOT Gate": {
        "builder": build_cnot,
        "latex": r"\mathrm{CNOT} = |0\rangle\langle0|\otimes I + |1\rangle\langle1|\otimes X",
        "description": "Controlled‑NOT: flip target qubit 1 if control qubit 0 is |1⟩"
    }
}

# ————— Main App —————
if "started" not in st.session_state:
    st.session_state.started = False

# Landing Page
if not st.session_state.started:
    st.title("Welcome to QubitQuest ✨")

    st.markdown(
        """
        🔭 **Enter the quantum realm where real particles, real math, and real code power your quest for fundamental understanding.**

        ---

        🌟 **What is QubitQuest?**
        QubitQuest is an interactive learning platform that guides you through a hands‑on quantum computing journey. Each lesson integrates theory, code, and hardware.

        - 📝 **Theory:** Dive into the mathematics behind quantum gates, state vectors, and measurement postulates.
        - 💻 **Code:** Write Braket Python snippets to build, manipulate, and visualize real quantum circuits.
        - ⚛️ **Hardware:** Run your circuits on IonQ’s trapped‑ion systems or a local simulator for instant feedback.

        ---

        📈 **Your Learning Path**
        1️⃣ Start with single‑qubit basics (superposition, Hadamard, Pauli gates).
        2️⃣ Progress to entanglement and multi‑qubit states (Bell, GHZ, W).
        3️⃣ Dive into core algorithms: Grover’s search, Quantum Fourier Transform, Phase Estimation, and more.
        💻 Practice by writing and running code directly on real IonQ hardware, reinforcing quantum mechanics from the ground up.

        ---

        🚀 **Why “Fundamental” Matters**
        - 🧲 **Atomic‑scale qubits:** Each qubit is a ¹⁷¹Yb⁺ ion — no superconducting abstractions; you work with real particles.
        - 💡 **Laser‑driven transitions:** Directly manipulate electronic states via focused laser pulses — textbook quantum mechanics in action.
        - 🔗 **Natural interactions:** Generate entanglement through Coulomb coupling and photon exchange, bypassing synthetic circuit complexity.

        ---
        """
    )
    def begin_qquest():
        st.session_state.started = True
    st.button("▶ Begin QubitQuest", on_click=begin_qquest)

# Tutorial Page
else:
    st.title("QubitQuest: Gate‑by‑Gate Tutorial")

    # ───── Gate Selector ─────
    lesson = st.selectbox("Select a gate to explore:", list(LESSONS.keys()))
    meta = LESSONS[lesson]

    # ───── Theory Panel ─────
    st.markdown(f"### {lesson}")
    st.write(meta["description"])
    st.latex(meta["latex"])

    # ───── Example Code (Read‑Only) ─────
    default_code = inspect.getdoc(meta["builder"])
    st.markdown("#### Example Code (click to populate below)")
    st.code(default_code, language="python")

    # ───── Populate Button ─────
    if "editor_code" not in st.session_state:
        st.session_state.editor_code = ""
    if st.button("Populate editor with example code"):
        lines = default_code.splitlines()
        if lines:
            func_def = lines[0]
            body     = ["    " + ln for ln in lines[1:]]
            st.session_state.editor_code = "\n".join([func_def] + body)

    # ───── Code Editor ─────
    user_code = st.text_area(
        "Your `build()` function:",
        value=st.session_state.editor_code,
        height=200
    )

    # ───── Backend Toggle & Shots ─────
    backend = st.radio("Run on:", ["🚀 Simulator", "⚛️ IonQ QPU"])
    shots   = st.slider("Shots:", 100, 5000, 1000)

    # ───── Run & Display ─────
    if st.button("▶ Run Circuit"):
        try:
            exec_env = {"Circuit": Circuit}
            exec(user_code, exec_env)
            circuit = exec_env["build"]()

            st.text(str(circuit))
            device = LocalSimulator() if backend.startswith("🚀") else AwsDevice("arn:aws:braket:us-west-2::device/qpu/ionq/H1")
            task   = device.run(circuit, shots=shots)
            counts = task.result().measurement_counts
            st.success(f"Results ({backend.split()[1]}):")
            st.bar_chart(counts)
        except Exception as e:
            st.error(f"Error in your build() function: {e}")

