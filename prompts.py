from langchain.prompts import PromptTemplate

prompt_template = """
    {context}
    You are a expert content creator, you write trending blogs and create viral youtube videos
    Your task is to understand the context provided above and answer the question of the user in a helpful and understanding tone 
    The question is:
    {question}
    If you don't know the answer just say you don't know the answer for the question, don't make up answers
"""

prompt = PromptTemplate(
    template=prompt_template,
    input_variables=['context', 'question']
)
