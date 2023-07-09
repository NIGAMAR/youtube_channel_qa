from ingestion_pipeline import IngetionPipeline
from transformers import pipeline
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv
import constants as const
import prompts as prmpt

# query the openai llm for the response


def run_llm(llm, question: str, context: str) -> str:
    chain = LLMChain(
        llm=llm,
        prompt=prmpt.prompt
    )
    return chain.run(context=context, question=question)


def main():

    llm = OpenAI(
        temperature=0.2,
        max_tokens=1000
    )

    while True:
        channel_name = input(const.msg_channel_name)
        # create a new ingestion pipeline
        ingestion_pipeline = IngetionPipeline()
        # run the ingestion pipeline
        try:
            knowlege_base = ingestion_pipeline.run(channel_name=channel_name)
            while True:
                question = input(const.msg_ask_question)
                # get the results from the knowlege base
                results = knowlege_base.similarity_search(query=question, k=4)
                context = "".join([result.page_content for result in results])
                response = run_llm(llm=llm, question=question, context=context)
                print(response)
                cont = input(const.msg_question_query)
                if cont == "n":
                    break
        except ValueError:
            print(
                f"Invalid channel name {channel_name}, Try with a different channel")
        cont = input(const.msg_channel_query)
        if cont == "n":
            break


if __name__ == "__main__":
    load_dotenv()
    main()
