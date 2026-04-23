import streamlit as st
from openai import OpenAI

# 🔑 PUT YOUR API KEY HERE
client = OpenAI(api_key="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")

def guess_game():
    print("🎮 Welcome to the Number Guessing Game!")
    number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("Enter your guess (1-100): "))
        attempts += 1

        if guess < number:
            print("📉 Too low! Try again.")
        elif guess > number:
            print("📈 Too high! Try again.")
        else:
            print(f"🎉 Correct! You guessed it in {attempts} attempts.")
            break

guess_

def guess_game():
    print("🎮 Welcome to the Number Guessing Game!")
    number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = int(input("Enter your guess (1-100): "))
        attempts += 1

        if guess < number:
            print("📉 Too low! Try again.")
        elif guess > number:
            print("📈 Too high! Try again.")
        else:
            print(f"🎉 Correct! You guessed it in {attempts} attempts.")
            break

guess_game()
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
