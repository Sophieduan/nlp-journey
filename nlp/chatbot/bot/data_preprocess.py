import jieba
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer

__PAD__ = 0
__UNK__ = 1
__GO__ = 2
__EOS__ = 3
__VOCAB__ = ['__PAD__', '__UNK__', '__GO__', '__EOS__']


def split(lines):
    out_lines = []
    for line in lines:
        split_line = ' '.join(jieba.cut(line.strip()))
        out_lines.append(split_line)
    return out_lines


def preprocess(lines, max_length, num_words, post=False):
    samples = split(lines)
    tokenizer = Tokenizer(num_words=num_words)
    tokenizer.fit_on_texts(samples)
    sequences = tokenizer.texts_to_sequences(samples)
    word_index = tokenizer.word_index

    # 加入辅助符号
    word_index_with = dict()
    index_word_with = dict()
    if post:
        sequences = [[__GO__] + [s + 3 for s in sequence] + [__EOS__] for sequence in sequences]
        for i, v in enumerate(__VOCAB__):
            word_index_with[v] = i
            index_word_with[i] = v
        for word, index in word_index.items():
            word_index_with[word] = index + 3
            index_word_with[index + 3] = word
        sequences = pad_sequences(sequences, maxlen=max_length, padding='post', value=__PAD__)
    else:
        sequences = [[s + 1 for s in sequence] for sequence in sequences]
        sequences = pad_sequences(sequences, maxlen=max_length, value=__PAD__)
        for i, v in enumerate(__VOCAB__[0:2]):
            word_index_with[v] = i
            index_word_with[i] = v

        for word, index in word_index.items():
            word_index_with[word] = index + 1
            index_word_with[index + 1] = word
    return sequences, word_index_with, index_word_with
