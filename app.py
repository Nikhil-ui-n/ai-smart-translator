import os
import re
import streamlit as st
from openai import OpenAI

# ---------- Load API key safely ----------
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ OpenAI API key not found. Add it to .streamlit/secrets.toml or set OPENAI_API_KEY.")
    st.stop()

client = OpenAI(api_key=api_key)

# ---------- UI ----------
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

# ---------- Prompt builder ----------
def build_prompt(code, action, source, target):
    if action == "Translate Code":
        return f"""You are an expert code translator.
Translate this {source} code to {target}.
Rules:
- Only return the translated code (no markdown fences)
- Preserve logic and edge cases
- Use idiomatic {target}
Code:
{code}"""
    elif action == "Explain Code":
        return f"""Explain this {source} code in simple, beginner-friendly terms.
Include key steps and purpose of each part.
Code:
{code}"""
    elif action == "Optimize Code":
        return f"""Optimize this {source} code for performance and readability.
Return:
1) Optimized code (no markdown fences)
2) Bullet points of improvements
Code:
{code}"""
    else:
        return f"""Analyze this {source} code.
Return:
- Time Complexity (Big-O)
- Space Complexity (Big-O)
- Short explanation
Code:
{code}"""

# ---------- OpenAI call ----------
def ask_openai(prompt: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content or ""

# ---------- Evaluator ----------
def evaluate_output(input_code: str, output_text: str, action: str, target: str):
    """Lightweight heuristics + format checks -> confidence score (0-100)"""
    score = 50
    notes = []

    out = output_text.strip()

    # Basic sanity
    if len(out) > 20:
        score += 10
    else:
        notes.append("Very short output")

    # Check code-like structure for translate/optimize
    if action in ["Translate Code", "Optimize Code"]:
        # No markdown fences expected
        if "```" in out:
            score -= 10
            notes.append("Contains markdown fences")

        # Language hints
        if target == "Python":
            if re.search(r"\bdef\b|\bprint", out):
                score += 10
            else:
                notes.append("Missing common Python patterns")
        elif target == "Java":
            if re.search(r"\bclass\b|\bpublic\b|\bSystem\.out\.println", out):
                score += 10
            else:
                notes.append("Missing common Java patterns")
        elif target == "C++":
            if re.search(r"#include|std::|cout", out):
                score += 10
            else:
                notes.append("Missing common C++ patterns")
        elif target == "C":
            if re.search(r"#include|printf\(", out):
                score += 10
            else:
                notes.append("Missing common C patterns")

    # Explanation / analysis structure
    if action == "Analyze Complexity":
        if re.search(r"O\(.+", out):
            score += 15
        else:
            notes.append("No Big-O found")

    if action == "Explain Code":
        if len(out.split()) > 40:
            score += 10
        else:
            notes.append("Explanation may be too brief")

    # Clamp
    score = max(0, min(100, score))
    return score, notes

# ---------- Run ----------
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

                if action in ["Translate Code", "Optimize Code"]:
                    st.code(result, language=target_lang.lower())
                else:
                    st.write(result)

                # Evaluator
                score, notes = evaluate_output(code, result, action, target_lang)
                st.markdown("### 🧪 Evaluation")
                st.metric("Confidence Score", f"{score}/100")
                if notes:
                    st.write("Notes:")
                    for n in notes:
                        st.write(f"- {n}")
                else:
                    st.write("No obvious issues detected.")

                # Utilities
                st.download_button("⬇️ Download Output", result, file_name="output.txt")
                st.text_area("📋 Copy Output", result, height=150)

            except Exception as e:
                st.error(f"❌ Error: {e}")
