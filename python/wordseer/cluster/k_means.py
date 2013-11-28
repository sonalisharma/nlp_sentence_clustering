import wordseer.setup
import wordseer.search
import wordseer.util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
    
def kMeansClusters(query, n_clusters=5):
    """ Returns the ranked list of search results, cluster centroids, and 
    labels 
    """
    sentences =  wordseer.search.getMatchingSentenceText(query)
    sents = [sent for sent in sentences];
    
    # Transform sentences into features of word counts.
    stop_words = wordseer.util.STOP_WORDS
    #stop_words = []
    vectorizer = TfidfVectorizer(max_df=0.5,
        stop_words='english')
    feature_vectors = vectorizer.fit_transform(sents)
    
    km = KMeans(n_clusters=n_clusters,
        init='k-means++', 
        max_iter=100,
        n_init=10,
        verbose=0)
    km.fit(feature_vectors)

    # Print out results.
    centers = km.cluster_centers_
    clustered = {};
    for i, label in enumerate(km.labels_):
        if not clustered.has_key(label):
            clustered[label] = [];
        clustered[label].append(sents[i])
    index = vectorizer.get_feature_names()
    return sentences, clustered, centers, index
    for i, center in enumerate(centers):
        print "<h1>\n--------------- CLUSTER " + str(i+1) + "-------------\n</h1>"
        paired = []
        for j, feature  in enumerate(center):
            if feature > 0:
                paired.append((feature, index[j]))
        paired.sort()
        paired.reverse()
        top_words = ", ".join([pair[1] for pair in paired[:10]])
        print "<h2>Top 10 Words</h2>\n<br>\t"+top_words+"<br><br>"
        print "<h2>Example sentences (showing upto 30)</h2>\n<br>"
        print '<ol>'
        for sentence in clustered[i][:30]:
            try:
                print "<li>\t\t"+ sentence.replace("\n", " ")+"</li>"
            except Exception, e:
                continue
        print '</ol>'
    