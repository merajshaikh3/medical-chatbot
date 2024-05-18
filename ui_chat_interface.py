import streamlit as st
from chat_components_5 import ChatManager
from model import MedicalChatBot

@st.cache_resource
def initialize_llm_model():
    # Initialize your chatbot
    VECTOR_STORE_PATH = "vector_store1"
    LLM_MODEL_NAME = 'llama-2-7b-chat.ggmlv3.q8_0.bin'
    LLM_MODEL_TYPE = 'llama'

    chatbot = MedicalChatBot(VECTOR_STORE_PATH, LLM_MODEL_NAME, LLM_MODEL_TYPE)
    chatbot.initialize_chatbot()

    return chatbot

class ChatApp:
    def __init__(self, llm_model):
        self.llm_model = llm_model
        self.chat_manager = ChatManager()
        self.chat_box = st.chat_input(
                                      placeholder='What is up?',
                                      key="Chat Box",
                                      on_submit=ChatApp.process_user_message,
                                      args=(self.chat_manager,)
                                     )
        self.new_chat_button = st.sidebar.button(
                                         label="New Chat",
                                         on_click=self.chat_manager.create_new_chat,
                                         type="primary",
                                         use_container_width=True
                                        )
    
    @staticmethod
    def process_user_message(chat_manager):
        user_message = st.session_state["Chat Box"]
        chat_manager.process_user_message(user_message)

    # @staticmethod
    # def create_new_chat_window(chat_manager):

    def render_page_outline(self):
        st.title("Medical Chatbot")
        st.sidebar.write("## Previous Chats")

    def load_chat_manager(self):
        self.chat_manager.load_chat_manager()
        if not self.chat_manager.has_valid_chats():
            st.sidebar.caption("No Chat History")

    def render_chat_messages(self):
        self.chat_manager.print_chat_history()

    def render_bot_message(self):
        self.chat_manager.stream_bot_message(self.llm_model)

    def run(self):
        self.render_page_outline()
        self.load_chat_manager()
        self.render_chat_messages()
        if self.chat_box:
            self.render_bot_message()



if __name__ == "__main__":
    # Initialize your chatbot
    llm_model = initialize_llm_model()
    # Run Streamlit application
    app = ChatApp(llm_model)
    app.run()
