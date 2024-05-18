from langchain_community.llms import CTransformers
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain.chains.retrieval_qa.prompt import prompt_template
# from langchain.chains.question_answering.stuff_prompt import PROMPT_SELECTOR
import streamlit as st
import time

class MedicalChatBot:
    def __init__(self, vector_store_path, llm_model_name, llm_model_type):
        self.vector_store_path = vector_store_path
        self.llm_model_name = llm_model_name
        self.llm_model_type = llm_model_type
        self.custom_prompt_template = """
            Use the following pieces of information to answer the user's question.
            If you don't know the answer, please just say that you don't know the answer, don't try to make up an answer.

            Context: {context}
            Question: {question}

            Only returns the helpful answer below and nothing else.
            Helpful answer:"""

        self.llm_chain = None  # Initialize later

    def _load_llm_model(self):
        print("\n==========Loading LLM Model==========\n")
        return CTransformers(
            model=self.llm_model_name,
            model_type=self.llm_model_type,
            max_new_tokens=512,
            temperature=0.5
        )

    def _load_vector_store(self):
        print("\n==========Loading Vector Store==========\n")
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        return FAISS.load_local(self.vector_store_path, embeddings)

    def _create_llm_chain(self):
        print("\n==========Creating LLM Chain==========\n")
        prompt = PromptTemplate(
            template=self.custom_prompt_template,
            input_variables=["context", "question"]
        )

        llm = self._load_llm_model()
        vector_store = self._load_vector_store()

        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=vector_store.as_retriever(search_kwargs={"k": 2}),
            return_source_documents=True,
            chain_type_kwargs={'prompt': prompt}
        )

    def initialize_chatbot(self):
        """Loads the LLM and vector store, creates the LLM chain."""
        print("\n==========Initializing Chatbot==========\n")
        t1 = time.time()

        self.llm_chain = self._create_llm_chain()  

        t2 = time.time()
        print(f"\n\n==========Time to load model is {t2 - t1} seconds==========\n\n")

    def generate_response(self, prompt):
        print(f"\n\n====={self.llm_chain}=====\n\n")
        response_dict = self.llm_chain({'query': prompt})
        # response = full_answer['result']

        # return response
        return response_dict
        # # Simulate typing effect 
        # for word in response.split():
        #     yield word + " "
        #     time.sleep(0.10)
    
if __name__ == "__main__":
    # Initialize your chatbot
    VECTOR_STORE_PATH = "vector_store"
    LLM_MODEL_NAME = 'llama-2-7b-chat.ggmlv3.q8_0.bin'
    LLM_MODEL_TYPE = 'llama'

    chatbot = MedicalChatBot(VECTOR_STORE_PATH, LLM_MODEL_NAME, LLM_MODEL_TYPE)
    chatbot.initialize_chatbot()

    chatbot.generate_response('Explain type 2 diabetes')
