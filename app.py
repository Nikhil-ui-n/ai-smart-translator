import streamlit as st
import requests

# 🔑 Add your Grok (xAI) API key here
XAI_API_KEY = "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"

st.set_page_config(page_title="Smart Code Translator (Grok)", layout="wide")

st.title("💻 Smart Code Translator (Grok Powered)")

# Sidebar
action = st.sidebar.selectbox("Choose Action", [
    "Translate Code",
    "Explain Code",
    "Optimize Code",
    "Analyze Complexity"
])

source_lang = st.sidebar.selectbox("Source Language", ["Python", "Java", "C++", "C"])
target_lang = st.sidebar.selectbox("Target Language", ["Python", "Java", "C++", "C"])

code = st.text_area("📝 Paste your code here:", height=300)


def ask_grok(prompt):
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grok-beta",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json()["choices"][0]["message"]["content"]


def build_prompt():
    if action == "Translate Code":
        return f"Translate this {source_lang} code to {target_lang}. Only return code:\n{code}"

    elif action == "Explain Code":
        return f"Explain this {source_lang} code simply:\n{code}"

    elif action == "Optimize Code":
        return f"Optimize this {source_lang} code and explain improvements:\n{code}"

    elif action == "Analyze Complexity":
        return f"Give time and space complexity of this {source_lang} code:\n{code}"


if st.button("🚀 Run AI"):
    if not code.strip():
        st.warning("Enter code first!")
    else:
        with st.spinner("Processing..."):
            prompt = build_prompt()
            result = ask_grok(prompt)

        st.success("Done!")

        st.subheader("📌 Output")
        st.code(result, language=target_lang.lower())

        st.download_button("⬇️ Download Output", result)
