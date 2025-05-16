from langchain_ollama import OllamaEmbeddings


def embeding_fuction():
    embedings = OllamaEmbeddings(
        model='tinyllama'
    )
    return embedings


# input = ["data/monopoly.pdf","data/ticket_to_ride.pdf"]
# vector = embed.embed_documents(input)
# print(len(vector))
# print(vector[0][:3])