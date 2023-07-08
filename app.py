from ingestion_pipeline import IngetionPipeline


def main():
    channel_name = input("Enter channel name: ")
    # create a new ingestion pipeline
    ingestion = IngetionPipeline()
    # run the ingestion pipeline
    try:
        ingestion.run(channel_name=channel_name)
        while True:
            question = input("Ask your question: ")
            knowlege_base = ingestion.get_knowlege_base()
            # get the results from the knowlege base
            results = knowlege_base.similarity_search(query=question, k=2)
            print(results)
            cont = input("Do you want to ask more questions (y/n): ")
            if cont == "n":
                break
    except ValueError:
        print(
            f"Invalid channel name {channel_name}, Try with a different channel")


if __name__ == "__main__":
    main()
