import streamlit as st
import openai

# 🔑 Add your OpenAI API Key here
openai.api_key = "YOUR_API_KEY_HERE"

st.set_page_config(page_title="Smart Code Translator", layout="wide")

st.title("💻 Smart Code Translator + Analyzer")

# Sidebar options
st.sidebar.title("⚙️ Options")
action = st.sidebar.selectbox("Choose Action", [
    "Translate Code",
    "Explain Code",
    "Optimize Code",
    "Analyze Complexity"
])

source_lang = st.sidebar.selectbox("Source Language", ["Python", "Java", "C++", "C"])
target_lang = st.sidebar.selectbox("Target Language", ["Python", "Java", "C++", "C"])

# Code input
code = st.text_area("📝 Enter your code here:", height=300)

def ask_ai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message["content"]

if st.button("🚀 Run"):
    if not code.strip():
        st.warning("Please enter code!")
    else:
        with st.spinner("Processing..."):

            if action == "Translate Code":
                prompt = f"Translate this {source_lang} code to {target_lang}. Only return code:\n{code}"

            elif action == "Explain Code":
                prompt = f"Explain this {source_lang} code in simple terms:\n{code}"

            elif action == "Optimize Code":
                prompt = f"Optimize this {source_lang} code and explain improvements:\n{code}"

            elif action == "Analyze Complexity":
                prompt = f"Give time and space complexity for this {source_lang} code:\n{code}"

            result = ask_ai(prompt)

        st.success("✅ Done!")
        st.subheader("📌 Output:")
        st.code(result, language=target_lang.lower())
