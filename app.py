import streamlit as st
import subprocess
import time

st.title("🎓 Course Assistant")

question = st.text_input("Your question:")
submit = st.button("Search")

if submit and question:

    # save question
    with open("question.txt", "w", encoding="utf-8") as f:
        f.write(question)

    st.subheader("Answer")

    # run your existing script (NO CHANGE)
    subprocess.run(["py", "processing_incoming.py"])

    # wait a bit (important)
    time.sleep(1)

    # read response
    try:
        with open("response.txt", "r", encoding="utf-8") as f:
            answer = f.read()
            st.write(answer)
    except:
        st.error("No response found")