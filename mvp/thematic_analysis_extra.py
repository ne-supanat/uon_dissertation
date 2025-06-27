import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import string
from gensim import corpora
from gensim.models import LsiModel, LdaModel
from sklearn.cluster import KMeans
from collections import defaultdict


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
    pos_tagged = nltk.pos_tag(tokens)
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

    # Filter Noun and Verb
    lemmatised_tokens = []
    for word, tag in wordnet_tagged:
        # Only Noun and Verb tag
        if tag in [wordnet.NOUN, wordnet.VERB]:
            # Use the tag to lemmatise the token
            lemmatised_token = WordNetLemmatizer().lemmatize(word, tag)
            if lemmatised_token not in stopwords.words("english"):
                lemmatised_tokens.append(lemmatised_token)

    normalised_document = " ".join(lemmatised_tokens).lower()
    return normalised_document


def common_words(corpus: list[str]):
    corpus = [normalised(c) for c in corpus]
    corpus_str = " ".join(corpus)

    # Word cloud Noun/Verb
    freq_dist = nltk.FreqDist(nltk.word_tokenize(corpus_str))
    most20 = freq_dist.most_common(20)
    for i in range(0, len(most20), 5):
        print(
            f"{most20[i]}\t{most20[i+1]}\t{most20[i+2]}\t{most20[i+3]}\t{most20[i+4]}"
        )


# https://www.datacamp.com/tutorial/what-is-topic-modeling
def topic_modeling(corpus: list[str]):
    clean_corpus = [normalised(doc).split() for doc in corpus]

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

    clustered = defaultdict(list)
    for sentence, label in zip(corpus, labels):
        clustered[label].append(sentence)

    for cluster_id, sents in clustered.items():
        print(f"Theme {cluster_id + 1}:")
        for s in sents[: min(3, len(sents))]:
            print(f" - {s}")
        print()


def analyse(document_paths):
    corpus = []

    for interview_path in document_paths:
        with open(interview_path, "r") as f:
            for line in f:
                # Cut only participant sentences
                if line.startswith("Participant: "):
                    line_sentence = line.strip().split(": ")[1]
                    corpus.append(line_sentence)

    corpus: list[str] = "".join(corpus).replace("\n", " ").split(". ")

    # Common words
    common_words(corpus)
    print()
    # LSA,LDA
    topic_modeling(corpus)
    print()
    # Clustering
    clustering(corpus)
    print()


if __name__ == "__main__":
    document_paths = ["data/mvp_1.txt", "data/mvp_2.txt", "data/mvp_3.txt"]
    ta_codes_csv_path = "mvp/results/thematic_analysis_codes.csv"
    analyse(document_paths)
