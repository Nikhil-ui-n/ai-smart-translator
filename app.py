import streamlit as st

# ====== CONFIG ======
st.set_page_config(page_title="Smart Code Translator", layout="wide")

st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
textarea {
    background-color: #1e1e1e !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

st.title("💻 Smart Code Translator (AI Powered)")

# ====== SIDEBAR ======
st.sidebar.title("⚙️ Settings")

provider = st.sidebar.selectbox("AI Provider", ["OpenAI", "Gemini (Free)"])

action = st.sidebar.selectbox("Choose Action", [
    "Translate Code",
    "Explain Code",
    "Optimize Code",
    "Analyze Complexity"
])

source_lang = st.sidebar.selectbox("Source Language", ["Python", "Java", "C++", "C"])
target_lang = st.sidebar.selectbox("Target Language", ["Python", "Java", "C++", "C"])

# ====== INPUT ======
code = st.text_area("📝 Paste your code here:", height=300)

# ====== AI FUNCTIONS ======

def ask_openai(prompt):
    from openai import OpenAI
    client = OpenAI(api_key="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")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def ask_gemini(prompt):
    import google.generativeai as genai

    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content(prompt)
    return response.text


def generate_prompt():
    if action == "Translate Code":
        return f"""
You are an expert code translator.

Translate this {source_lang} code to {target_lang}.

Rules:
- Only return code
- No explanations
- Maintain logic

Code:
{code}
"""

    elif action == "Explain Code":
        return f"""
Explain this {source_lang} code in simple beginner-friendly language.

Code:
{code}
"""

    elif action == "Optimize Code":
        return f"""
Optimize this {source_lang} code.

Return:
1. Optimized code
2. Improvements made

Code:
{code}
"""

    elif action == "Analyze Complexity":
        return f"""
Analyze time and space complexity of this {source_lang} code.

Return:
- Time Complexity
- Space Complexity
- Explanation

Code:
{code}
"""


# ====== RUN BUTTON ======
if st.button("🚀 Run AI"):
    if not code.strip():
        st.warning("⚠️ Please enter some code first!")
    else:
        with st.spinner("Processing..."):
            prompt = generate_prompt()

            try:
                if provider == "OpenAI":
                    result = ask_openai(prompt)
                else:
                    result = ask_gemini(prompt)

                st.success("✅ Done!")

                # Output
                st.subheader("📌 Output")
                st.code(result, language=target_lang.lower())

                # Download
                st.download_button(
                    label="⬇️ Download Output",
                    data=result,
                    file_name="output.txt"
                )

                # Copy
                st.text_area("📋 Copy Output", result, height=150)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
