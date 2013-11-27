goog.require('goog.string.StringBuffer');
goog.require('goog.dom');

/** Namespace declaration. **/
app.view.search_results = {};

app.view.search_results.init = function() {
    app.bind("model.fetched", app.view.search_results.draw);
    app.bind("model.changed", app.view.search_results.draw)     
}

/** Draws search results in the center pane and sets up interactivity. **/
app.view.search_results.draw = function(){
    var t1 = new Date().getTime();
    var html = new goog.string.StringBuffer("");
    html.append('<table id="search-results-table">')
    app.view.search_results.appendTableHeader(html);
    app.model.getVisibleResults().forEach(function(result) {
        app.view.search_results.appendResult(result, html);
    })
    html.append('</table>')
    $("#search-results").html(html.toString());
    var t2 = new Date().getTime();
    console.log("Time to draw search results: "+ ((t2 - t1)/1000) +"s");
}

app.view.search_results.appendTableHeader = function(html) {
    html.append("<thead>");
    html.append("</thead>");
}

app.view.search_results.appendResult = function(result, html) {
    html.append("<tr sentence-id='" + result.id + "'>");
    html.append("<td class='sentence'>");
    var text = result.sentence +"";
    // Highlight the selected phrases
    var selected = app.model.getSelectedPhrases().reverse();
    if (app.model.phrases.pinned_id) {
        selected.push(app.model.getPhrase(app.model.phrases.pinned_id));
    }
    selected.forEach(function(phrase) {
        var phrase_id = phrase.id;
        var index = app.model.phrases.selected_ids.indexOf(phrase_id);
        var color = app.view.category.getHighlightColor(index);
        var variants = phrase.variants;
        variants.forEach(function(variant) {
            var variant_regex = new RegExp("\\W"+variant+"\\W", 'g');
            text = text.replace(variant_regex, function(match) {
                left = match[0];
                right = match[match.length - 1];
                if (right == " ") {
                    variant += " ";
                }
                return left + ("<span style='color:"+color+";'>" + 
                        variant + "</span>") + right;
            });
        })
    })
    html.append(app.util.newlineToBr(text));
    html.append("</td>");
    html.append("</tr>");
}