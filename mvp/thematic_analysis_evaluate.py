import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

import string
from gensim import corpora
from gensim.models import LsiModel, LdaModel
from sklearn.cluster import KMeans


# Run once
# nltk.download("stopwords")
# nltk.download("wordnet")


# https://www.geeksforgeeks.org/machine-learning/python-lemmatization-approaches-with-examples/
def pos_tagger(nltk_tag):
    if nltk_tag.startswith("J"):
        return wordnet.ADJ
    elif nltk_tag.startswith("V"):
        return wordnet.VERB
    elif nltk_tag.startswith("N"):
        return wordnet.NOUN
    elif nltk_tag.startswith("R"):
        return wordnet.ADV
    else:
        return None


# def NLPThemeticAnalysis(interviewPaths: list[str]):
#     participantCorpus = []
#     for interviewPath in interviewPaths[0:]:
#         with open(interviewPath, "r") as f:
#             for line in f:
#                 # Cut only participant sentences
#                 if line.startswith("Participant: "):
#                     participantCorpus.append(line.split(": ")[1])

#     fullCorpus = re.sub(r"[^a-zA-Z\s]", "", ". ".join(participantCorpus))

#     lemmatisedTokensNV = [normalised(doc) for doc in participantCorpus]
#     lemmatisedTokensNV = ". ".join(lemmatisedTokensNV)

#     # # Word cloud Noun/Verb
#     # freqDist = nltk.FreqDist(nltk.word_tokenize(lemmatisedTokensNV))
#     # most20 = freqDist.most_common(20)
#     # for i in range(0, len(most20), 5):
#     #     print(
#     #         f"{most20[i]}\t{most20[i+1]}\t{most20[i+2]}\t{most20[i+3]}\t{most20[i+4]}"
#     #     )

#     # # Topic modeling LDA
#     # vectorizer = TfidfVectorizer()
#     # X = vectorizer.fit_transform(nltk.word_tokenize(lemmatisedTokensNV))

#     # topicSize = 5
#     # nmf = NMF(n_components=topicSize)
#     # nmf.fit(X)

#     # # Display top keywords per theme
#     # for i, topic in enumerate(nmf.components_):
#     #     print(
#     #         f"Theme {i+1}: ",
#     #         [vectorizer.get_feature_names_out()[j] for j in topic.argsort()[-10:]],
#     #     )

#     # # ///
#     # clean_corpus = [clean(doc).split() for doc in participantCorpus]

#     # # Creating document-term matrix
#     # # clean_corpus = [lemmatisedTokensNV.split(" ")]
#     # dictionary = corpora.Dictionary(clean_corpus)
#     # doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_corpus]

#     # # LSA model
#     # lsa = LsiModel(doc_term_matrix, num_topics=3, id2word=dictionary)
#     # print(lsa.print_topics(num_topics=3, num_words=3))

#     # # LDA model
#     # lda = LdaModel(doc_term_matrix, num_topics=3, id2word=dictionary)
#     # print(lda.print_topics(num_topics=3, num_words=3))

#     # ///
#     from sklearn.cluster import KMeans

#     sentences = lemmatisedTokensNV.split(". ")
#     vectorizer = TfidfVectorizer()
#     X = vectorizer.fit_transform(sentences)

#     n_clusters = 5
#     kmeans = KMeans(n_clusters=n_clusters)
#     labels = kmeans.fit_predict(X)

#     from collections import defaultdict

#     clustered = defaultdict(list)
#     for sentence, label in zip(sentences, labels):
#         clustered[label].append(sentence)

#     for cluster_id, sents in clustered.items():
#         print(f"\nTheme {cluster_id + 1}:")
#         for s in sents[: min(3, len(sents))]:
#             print(f" - {s}")


def normalised(document: str) -> str:
    # Only alphabet and whitespace
    document = re.sub(r"[^a-zA-Z\s.]", "", document)

    # Tokenise document
    tokens = nltk.word_tokenize(document)

    # Remove stopwords and punctuation
    tokens = [
        token
        for token in tokens
        if token not in stopwords.words("english")
        or token not in set(string.punctuation)
    ]

    # Tag part of speech
    posTagged = nltk.pos_tag(tokens)
    wordnetTagged = list(map(lambda x: (x[0], pos_tagger(x[1])), posTagged))

    # Filter Noun and Verb
    lemmatisedTokens = []
    for word, tag in wordnetTagged:
        # Only Noun and Verb tag
        if tag in [wordnet.NOUN, wordnet.VERB]:
            # Use the tag to lemmatise the token
            lemmatisedToken = WordNetLemmatizer().lemmatize(word, tag)
            if lemmatisedToken not in stopwords.words("english"):
                lemmatisedTokens.append(lemmatisedToken)

    normalisedDocument = " ".join(lemmatisedTokens).lower()
    return normalisedDocument


def common_words(corpus: list[str]):
    corpus = [normalised(c) for c in corpus]
    # for interviewPath in interviewPaths[0:]:
    #     with open(interviewPath, "r") as f:
    #         for line in f:
    #             # Cut only participant sentences
    #             if line.startswith("Participant: "):
    #                 sentences = line.strip().split(": ")[1]
    #                 for sentence in sentences.split(". "):
    #                     corpus.append(normalised(sentence))

    corpus_str = " ".join(corpus)

    # Word cloud Noun/Verb
    freq_dist = nltk.FreqDist(nltk.word_tokenize(corpus_str))
    most20 = freq_dist.most_common(20)
    for i in range(0, len(most20), 5):
        print(
            f"{most20[i]}\t{most20[i+1]}\t{most20[i+2]}\t{most20[i+3]}\t{most20[i+4]}"
        )


def topic_modeling(corpus: list[str]):
    corpus = [normalised(c) for c in corpus]
    # for interviewPath in interviewPaths[0:]:
    #     with open(interviewPath, "r") as f:
    #         for line in f:
    #             # Cut only participant sentences
    #             if line.startswith("Participant: "):
    #                 sentences = line.strip().split(": ")[1]
    #                 for sentence in sentences.split(". "):
    #                     corpus.append(normalised(sentence))

    clean_corpus = [doc.split() for doc in corpus]

    # Creating document-term matrix
    dictionary = corpora.Dictionary(clean_corpus)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in clean_corpus]

    # LSA model
    lsa = LsiModel(doc_term_matrix, num_topics=5, id2word=dictionary)
    print(lsa.print_topics(num_topics=5, num_words=5))

    # LDA model
    lda = LdaModel(doc_term_matrix, num_topics=5, id2word=dictionary)
    print(lda.print_topics(num_topics=5, num_words=5))


def clustering(corpus: list[str]):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)

    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters)
    labels = kmeans.fit_predict(X)

    from collections import defaultdict

    clustered = defaultdict(list)
    for sentence, label in zip(corpus, labels):
        clustered[label].append(sentence)

    for cluster_id, sents in clustered.items():
        print(f"\nTheme {cluster_id + 1}:")
        for s in sents[: min(3, len(sents))]:
            print(f" - {s}")


if __name__ == "__main__":
    interviewPaths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    corpus = []

    for interviewPath in interviewPaths:
        with open(interviewPath, "r") as f:
            for line in f:
                # Cut only participant sentences
                if line.startswith("Participant: "):
                    line_sentence = line.strip().split(": ")[1]
                    corpus.append(line_sentence)

    corpus: list[str] = "".join(corpus).replace("\n", " ").split(". ")

    # # Common words
    common_words(corpus)
    # LSA,LDA
    topic_modeling(corpus)
    # Clustering
    clustering(corpus)
