import streamlit as st
from openai import OpenAI

# --- Load API key safely ---
api_key = st.secrets.get("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", None)
if not api_key:
    import os
    api_key = os.getenv("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")

if not api_key:
    st.error("❌ OpenAI API key not found. Add it to .streamlit/secrets.toml or set OPENAI_API_KEY env var.")
    st.stop()

client = OpenAI(api_key=api_key)

# --- UI ---
st.set_page_config(page_title="Smart Code Translator", layout="wide")
st.title("💻 Smart Code Translator (OpenAI)")

st.sidebar.header("⚙️ Options")
action = st.sidebar.selectbox("Choose Action", [
    "Translate Code",
    "Explain Code",
    "Optimize Code",
    "Analyze Complexity"
])

source_lang = st.sidebar.selectbox("Source Language", ["Python", "Java", "C++", "C"])
target_lang = st.sidebar.selectbox("Target Language", ["Python", "Java", "C++", "C"])

code = st.text_area("📝 Paste your code here:", height=300)

def build_prompt(code, action, source, target):
    if action == "Translate Code":
        return f"""You are an expert code translator.
Translate this {source} code to {target}.
Rules:
- Only return the translated code
- Preserve logic
Code:
{code}"""
    elif action == "Explain Code":
        return f"""Explain this {source} code in simple terms for a beginner:
{code}"""
    elif action == "Optimize Code":
        return f"""Optimize this {source} code.
Return:
1) Optimized code
2) Bullet points of improvements
Code:
{code}"""
    else:
        return f"""Analyze this {source} code.
Return:
- Time Complexity
- Space Complexity
- Short explanation
Code:
{code}"""

def ask_openai(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content

if st.button("🚀 Run AI"):
    if not code.strip():
        st.warning("⚠️ Please paste some code first.")
    else:
        with st.spinner("Thinking..."):
            try:
                prompt = build_prompt(code, action, source_lang, target_lang)
                result = ask_openai(prompt)

                st.success("✅ Done")
                st.subheader("📌 Output")

                # For translation/optimize, show as code; else plain text
                if action in ["Translate Code", "Optimize Code"]:
                    st.code(result, language=target_lang.lower())
                else:
                    st.write(result)

                st.download_button("⬇️ Download Output", result, file_name="output.txt")
                st.text_area("📋 Copy Output", result, height=150)

            except Exception as e:
                st.error(f"❌ Error: {e}")
