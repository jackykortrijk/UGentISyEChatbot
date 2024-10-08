import streamlit as st
from openai import OpenAI
from langchain_community.graphs import Neo4jGraph

# Page Config
st.set_page_config("UGent ISyE Chatbot", page_icon="random")

# Show title and description.
st.title("🤖 UGent ISyE Chatbot")
st.write(
    "This is a chatbot that uses OpenAI's GPT-4.0 model to generate responses. "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🔑")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello👋, I'm the UGent ISyE Chatbot🤖! What can I do for you?"},]
        
    def write_message(role, content, save = True):
        """
        This is a helper function that saves a message to the
        session state and then writes a message to the UI
        """
        # Append to session state
        if save:
            st.session_state.messages.append({"role": role, "content": content})

        # Write to UI
        with st.chat_message(role):
            st.markdown(content) #显示内容
            
    def handle_submit(message):
        """
        Submit handler:

        You will modify this method to talk with an LLM and provide
        context using data from Neo4j.
        """

        # Handle the response
        with st.spinner('Thinking...'):
            # # TODO: Replace this with a call to your LLM
            from time import sleep
            sleep(1)
            write_message('assistant', message)

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
