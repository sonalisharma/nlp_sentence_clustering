#!/Users/shubham/.virtualenvs/nlp/bin/python

"""
Code for calculating and printing out a k-means clustering of search results that
match a certain word.
"""
import os
#os.environ['PYTHON_EGG_CACHE'] = '/tmp'
import sys
import MySQLdb
import cgi, cgitb
import wordseer.setup
import wordseer.search
import wordseer.cluster.k_means as k_means

cgitb.enable()
start_html = """<!DOCTYPE HTML5>
<html>
<head>
<title>K-means of search results</title>
</head>
<body>
<form action="">
<label>Query</label> <input name="query">
<label>Collection</label>
<select name="instance">
    <option value="shakespeare">Shakespeare</option>
    <option value="acm">ACM Conference Abstracts</option>
</select>
<label>Number of clusters</label>
<input name="n_clusters">
<input type="submit" value="Go">
</form>
"""
end_html = "</body></html>"

if __name__ == "__main__":
    print "Content-Type: text/html;charset=utf-8"
    print
    form = cgi.FieldStorage()

    print start_html

    # Extract command-line arguments.
    query = None
    if (len(sys.argv) > 1):
        query = sys.argv[1]
    elif "query" in form:
        query = form["query"].value

    n_clusters = None
    if (len(sys.argv) > 2):
        n_clusters = int(sys.argv[2])
    elif "n_clusters" in form:
        n_clusters = int(form["n_clusters"].value)

    instance = None
    if (len(sys.argv) > 3):
        instance = sys.argv[3]
    elif "instance" in form:
        instance = form["instance"].value

    if query is not None and instance is not None and n_clusters is not None:
        wordseer.setup.setup(instance)
        sentences, clustered, centers, index = k_means.kMeansClusters(query,
            n_clusters)
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
    print end_html
