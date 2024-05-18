from state_3 import StateManager
import string, random
import streamlit as st
from message_components import UserMessage, BotMessage
import time
from typing import Dict, Any



def generate_random_alphanumeric(length=10):
        """Generates a random alphanumeric string of specified length."""

        characters = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(characters) for _ in range(length))
        return random_string

class Chat:
    def __init__(
                 self,
                 id, 
                 callback=None, 
                 history=None, 
                 title=None, 
                 button=None
                 ):
        self.id = id
        self.callback = callback
        self.history = self.get_history(history)
        # st.write(self.history)
        self.title = self.get_chat_title(title, self.history)
        self.button = button
        # self.button = self.get_chat_button(button, self.title, self.callback)
    
    def create_chat_button(self):
        if self.title is not None:
            self.button = st.sidebar.button(
                                     label=self.title,
                                     on_click=self.callback,
                                     args=(self,),
                                     use_container_width=True
                                     )
        else:
            self.button = None


    def _get_last_user_message(self):
        if len(self.history) > 0:
            if self.history[-1].role == "user":
                return self.history[-1]
            
            if self.history[-2].role == "user":
                return self.history[-2]
        else:
            return None
        
    def _get_last_bot_message(self):
        if len(self.history) > 0:
            if self.history[-1].role == "assistant":
                return self.history[-1]
            
            if self.history[-2].role == "assistant":
                return self.history[-2]
        else:
            return None
            
    @staticmethod
    def get_chat_title(title, history):
        if title is None and history is not None and len(history) > 0:
            return f"{history[0].message_text[:30]}..."
        else:
            return title
    
    def get_chat_button(self, button, title, callback):
        if button is not None:
            return button
        elif title is not None:
            return st.sidebar.button(
                                     label=title,
                                     on_click=callback,
                                     args=(self,),
                                     use_container_width=True
                                     )
        else:
            return None
        
    @staticmethod
    def get_history(history):
        messages_list = []
        if history is None:
            return []
        else:
            for message_data in history:
                messages_list.append(Chat.instantiate_existing_message(message_data))
            return messages_list

    @staticmethod
    def instantiate_existing_message(message_data):
        if message_data['role'] == 'user':
            return UserMessage(**message_data)
        
        if message_data['role'] == 'assistant':
            return BotMessage(**message_data)
        
    @staticmethod
    def create_new_message(user, message, time=None):
        if user == "user":
            return UserMessage(message)
        
        if user == "assistant":
            return BotMessage(message, time)
        
    def print_chat_history(self):
        if len(self.history) > 0:
            for message in self.history:
                message.print_message() # This step is instantiating + printing the contents of UserMessage and BotMessage

    def generate_bot_response(self, llm_model):
        with st.spinner('Loading...'):
            t1 = time.time()
            response_dict = llm_model.generate_response(self._get_last_user_message().message_text)
            t2 = time.time()
            response_time = t2 - t1

        return response_dict, response_time
    
    @staticmethod
    def stream_bot_message(bot_message):
        bot_message.stream_message()
    
        

class ChatManager:
    def __init__(self) -> None:
        self.state = StateManager("current_chat_id","chats")
        self.current_chat_id = None
        self.chats = []

    # METHODS TO MANAGE CHAT OBJECTS

    def load_chat_manager(self) -> None:
        self.load_current_chat_id()
        self.load_chats()
        
    def load_current_chat_id(self) -> None:
        self.current_chat_id = self.state.get_current_chat_id()

    def load_chats(self) -> None:
        chats_data = self.state.get_chats()

        if len(chats_data) > 0:
            for chat_data in chats_data:
                self.chats.append(self.instantiate_existing_chats(chat_data))
        else:
            self.create_new_chat()

    def instantiate_existing_chats(self, chat_data: Dict[str, Any]) -> Chat:
        existing_chat_object = Chat(**chat_data)
        existing_chat_object.callback = self.update_current_chat_id # add the callback after serialization
        existing_chat_object.create_chat_button()
        return existing_chat_object 

    def save_chat(self, new_chat_attributes: dict) -> None:
        self.state.update_chat_manager(new_chat_attributes)

    def save_message(self, chat_id, message_attributes):
        self.state.update_chat_message(chat_id, message_attributes)

    def save_new_current_chat_id(self, chat_attributes):
        self.state.update_current_chat_id(chat_attributes)
        
    def create_new_chat(self):
        # Instantiating new chat
        new_chat_id = generate_random_alphanumeric()
        new_chat = Chat(
                        id=new_chat_id, 
                        callback=self.update_current_chat_id
                        )

        # Adding new chat to chat list
        self.chats.append(new_chat)
        self.current_chat_id = new_chat_id

        # Saving the new chat to the state manager
        new_chat.__dict__.pop('callback') # remove the callback before serialization
        self.save_chat(new_chat.__dict__) 

    def update_current_chat_id(self, new_chat):
        self.current_chat_id = new_chat.id
        self.save_new_current_chat_id(new_chat.__dict__)

    def get_current_chat(self):
        for chat in self.chats:
            if self.current_chat_id == chat.id:
                return chat

    # METHODS TO INTERFACE CHAT OBJECTS

    def process_user_message(self, message, time=None):
        current_chat = self.get_current_chat()
        formatted_user_message = current_chat.create_new_message("user", message, time)
        self.save_message(current_chat.id, formatted_user_message.__dict__)

    @staticmethod
    def process_user_message_wrapper(message):
        st.write(message)

    def print_chat_history(self):
        current_chat = self.get_current_chat()
        current_chat.print_chat_history()

    def stream_bot_message(self, llm_model):
        current_chat = self.get_current_chat()
        response_dict, response_time = current_chat.generate_bot_response(llm_model)
        formatted_bot_message = current_chat.create_new_message("assistant", response_dict['result'], response_time)
        Chat.stream_bot_message(formatted_bot_message)
        self.save_message(current_chat.id, formatted_bot_message.__dict__)

    def has_valid_chats(self):
        "It checks if the chat manager has at least 1 non-empty chat"
        for chat in self.chats:
            if chat.title is not None:
                return True
        return False

        
        








