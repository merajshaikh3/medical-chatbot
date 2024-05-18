import streamlit as st

class StateManager:
    def __init__(self, key1, key2):
        keys = (key1, key2)

        for key in keys:
            if key not in st.session_state:
                st.session_state[key] = []
                
        self.key1 = st.session_state[key1]
        self.key2 = st.session_state[key2]

    def update_current_chat_id(self, new_chat_attributes):
        if len(self.key1) == 0:
            self.key1.append(new_chat_attributes['id'])
        else:
            self.key1[0] = new_chat_attributes['id']

    def update_chats(self, new_chat_attributes):
        self.key2.append(new_chat_attributes)
    
    def get_current_chat_id(self):
        if len(self.key1) > 0:
            return self.key1[0]
        else:
            None
    
    def get_chats(self):
        if len(self.key2) > 0:
            return self.key2
        else:
            return []
    
    def update_chat_manager(self, new_chat_attributes):
        self.update_current_chat_id(new_chat_attributes)
        self.update_chats(new_chat_attributes)

    def update_chat_message(self, chat_id, message_attributes):
        for chat in self.key2:
            if chat['id'] == chat_id:
                chat['history'].append(message_attributes)
