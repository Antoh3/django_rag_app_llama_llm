from langchain_ollama import OllamaEmbeddings


def embeding_fuction():
    embedings = OllamaEmbeddings(model='nomic-embed-text')
    return embedings


# input = ["I am emmanuel"]
# vector = embeding_fuction(input)
# print(len(vector))
# print(vector[0][:3])