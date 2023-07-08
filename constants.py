import os

doc_chunk_size = 1500
doc_chunk_overlap = 200
knowledge_base_folder_name = "kb"
cwd = os.path.dirname(os.path.abspath(__file__))
kb_folder_path = os.path.abspath(cwd+"/"+knowledge_base_folder_name)
embedding_model = "sentence-transformers/all-mpnet-base-v2"
invalid_channel_d = "invalid_channel_id"

# Questions to ask
# 1. What do i need to do in order to progress in my carrer ?
# 2. Why is networking important ?
