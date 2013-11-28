/** Namespace declaration **/
app.model.search_results = {};
var module = app.model.search_results;  // Short-hand to save typing.

module.sort_by_visible_categories = false; // If false, sorts by ranking.

module.SearchResults = function(data) {
    this.ids = data.ranked_sentence_ids;
    this.visible_ids = [];
    this.index = {};
    for (var i = 0; i < this.ids.length; i++) {
        var result_id = this.ids[i];
        var result_data = data.sentence_index[result_id];
        this.index[result_id] = new app.model.search_results.SearchResult(
            result_id, result_data);
    }
}


module.SearchResults.prototype.calculateVisible = function(data) {
    app.model.resetResultVisibility();
    this.visible_ids = [];
    this.removed_ids = [];
    var me = this;
    
    app.model.phrases.removed_ids.forEach(function(phrase_id) {
        var removed_phrase = app.model.getPhrase(phrase_id);
        removed_phrase.result_ids.forEach(function(id) {
            if (me.removed_ids.indexOf(id) == -1) {
                me.removed_ids.push(id);
            }
        });
    });
    
    if (app.model.phrases.pinned_id != null) {
        // Only show the sentences for the pinned phrase
        me.ids.forEach(function(id) {
            me.getResult(id).is_visible = false;
        })
        var pinned = app.model.getPhrase(app.model.phrases.pinned_id);
        pinned.result_ids.forEach(function(id) {
                me.visible_ids.push(id);
                me.getResult(id).setVisible();                
        })
    } else if (app.model.phrases.selected_ids.length > 0) {
        // Intersect the sets of sentences of the selected phrases.
        me.ids.forEach(function(id) {
            me.getResult(id).is_visible = false;
        })
        var first_phrase_id = app.model.phrases.selected_ids[0];
        var first_phrase = app.model.getPhrase(first_phrase_id);
        me.visible_ids = [];
        first_phrase.result_ids.forEach(function(id) {
            if (me.removed_ids.indexOf(id) == -1) {
                me.visible_ids.push(id);                
            }
        });
        app.model.phrases.selected_ids.forEach(function(phrase_id) {
            var phrase = app.model.getPhrase(phrase_id);
            first_phrase.result_ids.forEach(function (id) {
                if (phrase.result_ids.indexOf(id) == -1) {
                    var i = me.visible_ids.indexOf(id);
                    if (i != -1) {
                        me.visible_ids.splice(i, 1);
                    }
                }
            })
        })
        me.visible_ids.forEach(function(id) {
            me.getResult(id).setVisible();
        })
    } else {
        // Hide sentences with removed phrases.
        for (var i = 0; i < this.ids.length; i++) {
            var id = this.ids[i];
            var result = this.getResult(id);
            result.calculateVisibility();
            if (result.is_visible) {
                this.visible_ids.push(id);
            }
        }   
    }
}

module.SearchResults.prototype.getResult = function(id) {
    if (this.ids.indexOf(id) != -1) {
        return this.index[id];
    }
    throw "No such result ID: "+id;
    return null;
}

module.SearchResults.prototype.sortVisible = function() {
    var t1 = new Date().getTime();
    var me = this;
    this.visible_ids.sort(function(id_a, id_b) {
        var a = me.getResult(id_a);
        var b = me.getResult(id_b);
        return a.rank - a.rank;
    })
    
    if (app.model.search_results.sort_by_visible_categories) {
        this.visible_ids.sort(function(id_a, id_b) {
            var a = me.getResult(id_a);
            var b = me.getResult(id_b);
            return (b.visible_phrase_ids.length - a.visible_phrase_ids.length);
        })
    }
    var t2 = new Date().getTime();
    console.log("Time to sort search results: "+((t2-t1)/1000)+"s");
}

module.SearchResult = function(id, data) {
    this.id = id;
    this.data = data;
    this.rank = data.rank;
    this.sentence = data.sentence;
    this.phrase_ids = data.phrase_ids;
    this.visible_phrase_ids = [];
    this.is_visible = true;
}

module.SearchResult.prototype.calculateVisibility = function() {
    var is_visible = true;
    this.visible_phrase_ids = [];
    for (var i = 0; i < this.phrase_ids.length; i++) {
        var phrase_id = this.phrase_ids[i];
        if (app.model.getPhrase(phrase_id).is_removed) {
            is_visible = false;
        }
        var phrase_is_visible = app.model.getPhrase(phrase_id).is_visible;
        if (phrase_is_visible) {
            this.visible_phrase_ids.push(phrase_id);
        }
    }
    if (is_visible) {
        this.setVisible();
    }
}

module.SearchResult.prototype.setVisible = function () {
    this.is_visible = true;
    var me = this;
    this.phrase_ids.forEach(function(phrase_id) {
        var visible = app.model.getPhrase(phrase_id).visible_result_ids;
        if (visible.indexOf(me.id) == -1) {
            visible.push(me.id);
        }
        app.model.getPhrase(phrase_id).count = visible.length;
    })
}

