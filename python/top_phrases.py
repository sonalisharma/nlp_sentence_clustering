#!/Users/shubham/.virtualenvs/nlp/bin/python

import wordseer.setup
import wordseer.search
import wordseer.util
import wordseer.cluster.top_phrases as top_phrases

import cgi,cgitb
import sys
import json

cgitb.enable()


start_html = """<!DOCTYPE HTML5>
<html>
<head>
<title>Top phrases from search results</title>
</head>
<body>
<form action="">
<label>Query</label> <input name="query">
<label>Collection</label>
<select name="instance">
    <option value="shakespeare">Shakespeare</option>
    <option value="acm">ACM Digital Library Abstracts</option>
</select>
<br>
<label>Stemming?</label>
<input checked="checked" type="radio" name="lemmatize" value="yes">Yes</input>
<input type="radio" name="lemmatize" value="no">No</input>
<input type="submit" value="Go">
</form>
"""
end_html = "</body></html>"
if __name__ == "__main__":
    form = cgi.FieldStorage()

    # Extract command-line arguments.
    query = None  # query term like "trilingual resource"
    if (len(sys.argv) > 2):
        query = sys.argv[2]
    elif "query" in form:
        query = form.getfirst("query")

    instance = None  # acm or shakespeare
    if (len(sys.argv) > 1):
        instance = sys.argv[1]
    elif "instance" in form:
        instance = form.getfirst("instance")

    lemmatize = False
    if "lemmatize" in form:
        lemmatize = (form.getfirst("lemmatize") == "yes")

    output_as_json = False
    if "format" in form:
        output_as_json = (form.getfirst("format") == "json")

    ## If this is being used as an AJAX request URL and not as a direct interface
    if not instance == None and not query == None:
        wordseer.setup.setup(instance)
        composite = top_phrases.calculateTopPhrases(query)
        phrase_ids = composite[0]
        phrase_index = composite[1]
        ranked_sentence_ids = composite[2]
        sentence_index = composite[3]
        variants = composite[4]
        #if output_as_json:  # Output an HTML page
        if not output_as_json:  # Output an HTML page
            print "Content-Type: text/html"
            print
            print start_html
            for i in range(min(200, len(ranked_phrase_ids))):
                phrase_id = phrase_ids[i]
                print '<p>'+phrase_index[phrase_id]["phrase"] + ": " +str(phrase_index[phrase_id]["count"])+"<p>"
            print end_html
        else: # Output a json-formatted response
            print "Content-Type: text/plain"
            print
            output = {"phrase_ids":phrase_ids,
                "phrase_index": phrase_index,
                "ranked_sentence_ids":ranked_sentence_ids,
                "sentence_index":sentence_index,
                "variants":variants}
            print json.dumps(output, indent=2, ensure_ascii=False)
    else:
        print "Content-Type: text/plain"
        print
        print "No data received."


