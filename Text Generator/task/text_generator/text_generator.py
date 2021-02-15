from nltk import WhitespaceTokenizer
from nltk import bigrams, trigrams
from collections import Counter
from collections import defaultdict
import random


class TextGenerator:

    def __init__(self):
        self.ending_signs = list('.!?')
        
    @staticmethod
    def w_tokenize(text):
        f = open(f'C:/Users/Jaroslav Marhivka/PycharmProjects/Text Generator/Text Generator/task/{text}',
                 'r', encoding='utf-8')
        pre_corpus = f.read()
        ws_tokenizer = WhitespaceTokenizer()
        corpus = ws_tokenizer.tokenize(pre_corpus)
        f.close()
        return corpus

    @staticmethod
    def generate_bigrams(corpus):
        bg = list(bigrams(corpus))
        return bg

    @staticmethod
    def generate_trigrams(corpus):
        tg = list(trigrams(corpus))
        return tg

    @staticmethod
    def process_bigrams(bg):
        pre_markov = defaultdict(list)
        for i in bg:
            pre_markov[i[0]].append(i[1])
        markov = {}
        for k, v in pre_markov.items():
            markov[k] = Counter(v)
        return markov

    @staticmethod
    def process_trigrams(tg):
        pre_markov = defaultdict(list)
        for i in tg:
            pre_markov[i[0] + " " + i[1]].append(i[2])
        markov = {}
        for k, v in pre_markov.items():
            markov[k] = Counter(v)
        return markov

    @staticmethod
    def generate_words(word, markov):
        s = random.choices([j[0] for j in markov[word].most_common()],
                           [j[1] for j in markov[word].most_common()])[0]
        return s

    @staticmethod
    def generate_pairs(pair, markov):
        # print(pair)
        if type(pair) == list:
            pair = " ".join(pair)
        s1 = pair.split(" ")[1]
        s2 = random.choices([j[0] for j in markov[pair].most_common()],
                            [j[1] for j in markov[pair].most_common()])[0]
        new_pair = s1 + " " + s2
        s3 = random.choices([j[0] for j in markov[new_pair].most_common()],
                            [j[1] for j in markov[new_pair].most_common()])[0]
        return s2 + " " + s3

    def generate_seed(self, corpus):
        seed = random.choice(corpus)
        if seed[0].isalpha() and seed[0].isupper() and not any(end in seed for end in self.ending_signs):
            return seed
        else:
            return self.generate_seed(corpus)

    def generate_pairs_by_rules(self, sent: list, i: int, p: str, markov: dict):
        if i == 0:
            s = self.generate_pairs(p, markov)
            try:
                if s.startswith(s[0].upper()) and any(end not in s for end in self.ending_signs):
                    return s
                else:
                    return self.generate_pairs_by_rules(sent, i, p, markov)
            except RecursionError:
                return s
        elif 4 >= i > 0:
            s = self.generate_pairs(p, markov)
            try:
                if any(end not in s for end in self.ending_signs):
                    return s
                else:
                    return self.generate_pairs_by_rules(sent, i, p, markov)
            except RecursionError:
                return s
        elif 10 > i >= 5:
            s = self.generate_pairs(p, markov)
            try:
                if any(end in s[-1] for end in self.ending_signs):
                    return s
                else:
                    return self.generate_pairs_by_rules(sent, i, p, markov)
            except RecursionError:
                return s

    def generate_sentence(self, sent, markov):
        while len(sent) < 10:
            i = len(sent)
            s = self.generate_pairs_by_rules(sent, i, sent[-1:], markov)
            sent.append(s)
            if len(sent) > 2 and any(end in s for end in self.ending_signs):
                return sent
        return sent

    def generate_text(self, sent, txt, markov):
        while len(txt) < 10:
            sentence = self.generate_sentence(sent, markov)
            last_1 = sentence[-1].split(" ")[0]
            if any(end in last_1 for end in self.ending_signs):
                sentence[-1] = last_1
            txt.append(" ".join(sentence))
            s = self.generate_seed((list(markov.keys())))
            sent = list()
            sent.append(s)
            sent.append(self.generate_pairs_by_rules(sent, len(sent), s, markov))
        print("\n".join(txt))

    def process_input(self):
        text = input()
        corpus = self.w_tokenize(text)
        bg = self.generate_trigrams(corpus)
        markov = self.process_trigrams(bg)
        seed = self.generate_seed(list(markov.keys()))
        sent = list()
        txt = list()
        sent.append(seed)
        pair = self.generate_pairs_by_rules(sent=sent, i=1, p=seed, markov=markov)
        sent.append(pair)
        self.generate_text(sent, txt, markov)


if __name__ == '__main__':
    text_gen = TextGenerator()
    # a = text_gen.w_tokenize('test/corpus.txt')
    # b = text_gen.generate_trigrams(a)
    # c = text_gen.process_trigrams(b)
    text_gen.process_input()


