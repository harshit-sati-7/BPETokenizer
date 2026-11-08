import streamlit as st

from main_tokenizer import BPETokinizer

st.title("BPE Tokenizer")

st.text("Trained on over 5000+ characters in a text")

if "toke" not in st.session_state:
    tok=BPETokinizer()
    tok.load()
    st.session_state["toke"]=tok

tok=st.session_state["toke"]

text=st.text_area(
    "Enter the text",
    placeholder="Type here..."
)

if st.button("Tokenize"):
    if text.strip():
        val=tok.encode(text)
        st.write("TOKEN USED: ",len(val))
        

    else:
        st.warning("Type something first")
