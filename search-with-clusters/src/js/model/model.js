/** Namespace declaration **/
app.model = {}

app.model.DATA_URL = "../python/top_phrases.py"
app.model.form = {};
app.model.phrases = {};
app.model.results = {};

app.model.init = function () {
    app.bind("model.fetch", app.model.fetch)
}

/** Gets search results from the server and triggers the "model.fetched" event  **/
app.model.fetch = function() {
    console.log("searched");
    params = {
        format: "json",
        lemmatize: "no",
        query: app.model.form.query,
        instance: app.model.form.instance,
    };
    $.getJSON(app.model.DATA_URL, params, function(data){
        app.model.instantiate(data);
        app.trigger("model.fetched");
    })
}

app.model.instantiate = function(data) {
    app.model.form.loading = false;
    app.model.phrases = new app.model.category.Phrases(data);
    app.model.results = new app.model.search_results.SearchResults(data);
}

app.model.calculateVisible = function() {
    app.model.phrases.calculateVisible();
    app.model.results.calculateVisible();
    app.model.phrases.sortVisible();
    app.model.results.sortVisible();
}

app.model.getSelectedPhrases = function() {
    var selected = [];
    app.model.phrases.selected_ids.forEach(function(id){
        selected.push(app.model.getPhrase(id));
    })
    return selected;
}

app.model.getRemovedPhrases = function() {
    app.model.calculateVisible();
    var removed = [];
    app.model.phrases.removed_ids.forEach(function(id){
        removed.push(app.model.getPhrase(id));
    })
    return removed;
}

app.model.getAllPhrases = function() {
    app.model.calculateVisible();
    var all = [];
    app.model.phrases.ids.forEach(function(id){
        all.push(app.model.getPhrase(id));
    })
    return all;
}

app.model.getVisiblePhrases = function() {
    app.model.calculateVisible();
    var all = [];
    app.model.phrases.visible_ids.forEach(function(id){
        all.push(app.model.getPhrase(id));
    })
    return all;
}

app.model.getUnmarkedPhrases = function() {
    app.model.calculateVisible();
    var visible = [];
    var removed = app.model.phrases.removed_ids;
    var selected = app.model.selected_ids;
    app.model.phrases.visible_ids.forEach(function(id) {
        if(selected.indexOf(id) == -1 && removed.indexOf(id) == -1) {
            visible.push(app.model.getPhrase(id));
        }
    })
    return visible;
}

app.model.getPhrase = function(id) {
    return app.model.phrases.getPhrase(id);
}

app.model.getSearchResult = function(id) {
    return app.model.results.getResult(id);
}

app.model.getVisibleResults = function() {
    app.model.calculateVisible();
    var results = [];
    var ids = app.model.results.visible_ids;
    ids.forEach(function(id) {
        results.push(app.model.getSearchResult(id))
    })
    return results;
}

app.model.resetResultVisibility = function() {
   app.model.phrases.ids.forEach(function(id) {
      app.model.getPhrase(id).visible_result_ids = [];
      app.model.getPhrase(id).count = 0;
   })
   app.model.results.visible_ids = [];
   app.model.results.ids.forEach(function(id){
      app.model.getSearchResult(id).is_visible = false;
   })
}
