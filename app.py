import streamlit as st

st.set_page_config(page_title="Smart Code Translator", layout="wide")

st.title("💻 Smart Code Translator (Demo Mode)")

# Sidebar
action = st.sidebar.selectbox("Choose Action", [
    "Translate Code",
    "Explain Code",
    "Optimize Code",
    "Analyze Complexity"
])

source_lang = st.sidebar.selectbox("Source Language", ["Python", "Java", "C++", "C"])
target_lang = st.sidebar.selectbox("Target Language", ["Python", "Java", "C++", "C"])

# Input
code = st.text_area("📝 Paste your code here:", height=300)


# -------- Fake AI (Demo Logic) --------
def fake_ai():
    if action == "Translate Code":
        return f"// Translated from {source_lang} to {target_lang}\n{code}"

    elif action == "Explain Code":
        return "This code takes user input, processes conditions, and prints output based on logic."

    elif action == "Optimize Code":
        return f"// Optimized version\n{code}\n\n// Improvements:\n- Reduced redundancy\n- Better readability"

    elif action == "Analyze Complexity":
        return "Time Complexity: O(n)\nSpace Complexity: O(1)\n\nExplanation: The code runs in a single loop."


# Run button
if st.button("🚀 Run AI"):
    if not code.strip():
        st.warning("⚠️ Please enter code!")
    else:
        result = fake_ai()

        st.success("✅ Done!")

        st.subheader("📌 Output")
        st.code(result)

        st.download_button("⬇️ Download Output", result)
