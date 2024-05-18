import streamlit as st
from datetime import datetime
import time

class UserMessage:
    def __init__(
                 self, 
                 message_text,
                 role = "user",
                 current_time = datetime.now(),
                 user_icon = ""
                 ):
        self.message_text = message_text
        self.role = role
        self.current_time = current_time
        self.user_icon = user_icon

    def _get_message_date(self):
        return self.current_time.strftime('%d %b')
    
    def _get_message_time(self):
        return self.current_time.strftime('%H:%M')
    
    def print_message(self):
        with st.chat_message('user'):
            st.markdown(self.message_text)
            st.caption(f"{self._get_message_date()}, {self._get_message_time()}")

class BotMessage:
    def __init__(
                 self, 
                 message_text,
                 time_to_respond,
                 role = "assistant",
                 current_time = datetime.now(),
                 bot_icon = "" 
                 ):
        self.message_text = message_text
        self.time_to_respond = time_to_respond
        self.role = role
        # self.debug_response = debug_response
        self.current_time = current_time
        self.bot_icon = bot_icon

    def _get_message_date(self):
        return self.current_time.strftime('%d %b')
    
    def _get_message_time(self):
        return self.current_time.strftime('%H:%M')
    
    def _get_message_len(self):
        return len(self.message_text.split())

    @staticmethod
    def yield_response(response):
        # Simulate typing effect 
        for word in response.split():
            yield word + " "
            time.sleep(0.10)

    def stream_message(self):
        with st.chat_message('assistant'):
            st.write_stream(self.yield_response(self.message_text))
            #st.caption only accepts strings
            st.caption(f"{self._get_message_date()}, {self._get_message_time()}  |  Load Time: {self.time_to_respond:.2f} seconds | Output Size: {self._get_message_len()} words")

    def print_message(self):
        with st.chat_message('assistant'):
            st.markdown(self.message_text)
            #st.caption only accepts strings
            st.caption(f"{self._get_message_date()}, {self._get_message_time()}  |  Load Time: {self.time_to_respond:.2f} seconds | Output Size: {self._get_message_len()} words")