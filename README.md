# Medical Chatbot

This project implements a medical chatbot that can answer common medical questions using information from the Gale Encyclopedia of Medicine. The chatbot utilizes Streamlit for the chat user interface, Langchain for the LLM chain, and FAISS for storing vector embeddings.

![Screenshot 2024-05-18 193117](https://github.com/merajshaikh3/medical-chatbot/assets/47921927/63f58534-e8c2-4b5e-a4aa-bda51da90b0b)

## Usage
### Running the Chat Interface
To run the chat interface, use the following command:

```bash
streamlit run ui_chat_interface.py
```

### Data Ingestion
To process PDF files and convert them into vector embeddings, use the following command:

```python ml_data_ingestion.py```

Note: Only PDF files are supported for now. The processed embeddings will be stored in a folder named "vectorstores".

## Files
### UI Files
* ui_chat_interface.py: Main file for running the chat interface.
* ui_chat_components.py: Contains classes for different chat components like messages, buttons, etc.
* ui_message_components.py: Contains classes for user and bot messages.
* ui_state_manager.py: Manages the chat data every time Streamlit is reloaded.
### ML Files
* ml_data_ingestion.py: Processes PDF files in the "data" folder and converts them into vector embeddings.
* ml_model_initialization.py: Contains classes required to initialize and access the LLM model. You'll need to download the lama-2-7b-chat.ggmlv3.q8_0.bin model from Hugging Face.

## Requirements
* Streamlit
* Langchain
* FAISS
* Hugging Face Transformers (for model initialization)
