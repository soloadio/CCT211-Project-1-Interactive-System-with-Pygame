import json
import gensim.downloader as api
from wonderwords import RandomWord


class WordModel():
    """
    
    """
    def __init__(self):
        pass

    def setup(self):
        """
        General method to initialize all parts of the word model for the Game.
        """
        # Setup word prediction model
        self.model = api.load("glove-wiki-gigaword-50")

        self.emoji_map = self.setup_emoji()

        # Setup goal
        rw = RandomWord()
        self.targetword = rw.word()

        return self.targetword

    def predict_word(self, text1, text2):
        """
        Simple word prediction defaulting to an addition in strings, when the word is out of scope.
        """
        try:
            predictedword = self.model.most_similar(positive=[text1, text2])[0][0]
        except:
            predictedword = text1 + text2
        print(predictedword)

        hexcode = self.get_emoji(predictedword)

        return predictedword, hexcode

    def get_emoji(self, text):
        """
        Returns the most similar emoji to the given text.
        """
        try:
            similar_emoji = self.model.most_similar_to_given(text, list(self.emoji_map.keys()))
            print(similar_emoji)
            hexcode = self.emoji_map[similar_emoji]
        except:
            hexcode = "1F4A9" # Defaults to poop emoji if word does not exist in the assets
        return hexcode


    def setup_emoji(self):
        """
        Parses openmoji.json into a dictionary storing all unique annotation for each emoji into a hexcode map.
        """
        with open("src/assets/openmoji.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        emoji_map = {}
        for emoji in data:
            if "-" in emoji["hexcode"]: # skip the different skin tone
                continue
            words = emoji["annotation"].lower().split()
            model_known = []
            for word in words:
                if word.isalpha() and word in self.model:
                    model_known.append(word)

            if len(model_known) == 0:
                continue
            elif len(model_known) == 1 and model_known[0] not in emoji_map:
                emoji_map[model_known[0]] = emoji["hexcode"]
            else:
                for knownwords in model_known:
                    if knownwords not in emoji_map:
                        emoji_map[knownwords] = emoji["hexcode"]

        return emoji_map