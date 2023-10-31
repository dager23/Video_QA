import working as w
import streamlit as st
#[theme]
st.set_page_config(layout="wide")

text=""
summary="Summary will come here"
url=False

st.title("VideoQA Bot")

url=st.text_input('Enter your url')

#col1, col2 , col3= st.tabs(['container1','container2','container3'])

with st.sidebar:
    st.title("Translation")
    text=None
    # Create a text input field for the user to enter the text they want to translate
    text = st.text_input("Enter text to translate:")
    target_language = st.selectbox("Target language:", ["tamil", "hindi", "telugu", "kannada", "malayalam"])
    #print(text)
    #print(target_language)
    if text and target_language:

        # Create a dropdown menu for the user to select the language they want to translate the text to
        if target_language=='tamil':
            target_language='ta'
        if target_language=='hindi':
            target_language='hi'
        if target_language=='telugu':
            target_language='te'
        if target_language=='kannada':
            target_language='kn'
        if target_language=='malayalam':
            target_language='ml'

        # Translate the text using the Google Translate API
        translated_text = w.translate(text, target_language)

        # Display the translated text
        st.markdown("Translated text:")
        st.markdown(translated_text)
if url:
    text=w.get_text_from_url(url)
    if text:
        summary=w.text_summary(text)
        with st.sidebar:
            st.video(url)
            st.markdown(" ")
            st.markdown("Here is a short Summary of the video for quick reference")
            st.markdown(" ")
            if summary:
                st.markdown(summary)
            else :
                st.markdown(text)
        st.spinner(text='In progress')
        #bard=w.connect_to_bard()
        bard=True
        #print(bard)
        st.markdown("Connecting to Bot")
        if bard:
            st.markdown("Bot Is Ready Now to Answer")
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # React to user input
            if prompt := st.chat_input("What is up?"):
                # Display user message in chat message container
                st.chat_message("user").markdown(prompt)
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})

                response = f"Echo: {w.connect_to_palm(text,prompt)}"
                #response="Its working?"
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})



