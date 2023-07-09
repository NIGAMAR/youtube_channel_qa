import os

doc_chunk_size = 1500
doc_chunk_overlap = 200
knowledge_base_folder_name = "kb"
cwd = os.path.dirname(os.path.abspath(__file__))
kb_folder_path = os.path.abspath(cwd+"/"+knowledge_base_folder_name)
embedding_model = "sentence-transformers/all-mpnet-base-v2"
invalid_channel_d = "invalid_channel_id"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
msg_channel_query = "Do you want to query another channel (y/n): "
msg_channel_name = "Enter channel name: "
msg_ask_question = "Ask your question: "
msg_question_query = "Do you want to ask more questions (y/n): "
