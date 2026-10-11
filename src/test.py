import gensim.downloader as api

model = api.load("glove-wiki-gigaword-50")

print(model.most_similar(positive=['woman', 'king'])[0][0])