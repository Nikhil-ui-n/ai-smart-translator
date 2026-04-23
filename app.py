import streamlit as st
from openai import OpenAI

# 🔑 PUT YOUR API KEY HERE
client = OpenAI(api_key="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")

# Page config
st.set_page_config(page_title="Smart Code Translator", layout="wide")

# Simple styling
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("💻 Smart Code Translator (OpenAI Powered)")

# Sidebar
st.sidebar.title("⚙️ Options")

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

# Prompt builder
def build_prompt():
    if action == "Translate Code":
        return f"Translate this {source_lang} code to {target_lang}. Only return code:\n{code}"

    elif action == "Explain Code":
        return f"Explain this {source_lang} code in simple beginner-friendly way:\n{code}"

    elif action == "Optimize Code":
        return f"Optimize this {source_lang} code and explain improvements:\n{code}"

    elif action == "Analyze Complexity":
        return f"Give time and space complexity of this {source_lang} code with explanation:\n{code}"

# Run button
if st.button("🚀 Run AI"):
    if not code.strip():
        st.warning("⚠️ Please enter code first!")
    else:
        with st.spinner("Processing..."):
            try:
                prompt = build_prompt()

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )

                result = response.choices[0].message.content

                st.success("✅ Done!")

                # Output
                st.subheader("📌 Output")
                st.code(result, language=target_lang.lower())

                # Copy box
                st.text_area("📋 Copy Output", result, height=150)

                # Download button
                st.download_button(
                    label="⬇️ Download Output",
                    data=result,
                    file_name="output.txt"
                )

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
