/** Namespace declaration **/
app.model.category = {};

app.model.category.use_lemmatized = true;
app.model.category.use_stop_words = false;

app.model.category.Phrases = function(data){
    this.ids = data.phrase_ids;
    this.index = {};
    for (var i = 0; i < this.ids.length; i++) {
        var phrase_id = this.ids[i];
        var phrase_info = data.phrase_index[phrase_id];
        var variants = data.variants[phrase_info.phrase];
        this.index[phrase_id] = new app.model.category.Phrase(phrase_id,
            phrase_info, variants);
    }

    this.visible_ids = [];
    this.selected_ids = [];
    this.removed_ids = [];
    this.pinned_id = null;

    this.calculateVisible();
}

app.model.category.Phrases.prototype.calculateVisible = function() {
    var t1 = new Date().getTime();
    this.visible_ids = [];
    this.selected_ids = [];
    this.removed_ids = [];
    for (var i = 0; i < this.ids.length; i++) {
        var id = this.ids[i];
        var phrase = this.getPhrase(id);
        phrase.calculateVisibility();
        if (phrase.is_visible) {
            this.visible_ids.push(id);
        }
        if (phrase.is_selected) {
            this.selected_ids.push(id)
        }
        if (phrase.is_removed) {
            this.removed_ids.push(id);
        }
    }
    app.model.search_results.sort_by_visible_categories =
        this.selected_ids.length > 0;
    var t2 = new Date().getTime();
    console.log("Time to calculate visible phrases: "+((t2-t1)/1000)+"s");
}

app.model.category.Phrases.prototype.getPhrase = function(id) {
    if (this.ids.indexOf(id) != -1) {
        return this.index[id];
    } else {
        throw "No such phrase id: "+id;
        return null;
    }
}

app.model.category.Phrases.prototype.sortVisible = function() {
    var me = this;
    this.visible_ids.sort(function(id_a, id_b) {
        var count_a = me.getPhrase(id_a).count;
        var count_b = me.getPhrase(id_b).count;
        return count_b - count_a
    })
}

app.model.category.Phrases.prototype.unpin = function() {
    this.pinned_id = null;
    var me = this;
    this.ids.forEach(function(id) {
        me.getPhrase(id).is_pinned = false;
    })
}

app.model.category.Phrase = function(id, data, variants) { 
    this.id = id;
    this.phrase = data.phrase;
    this.result_ids = data.ids;
    this.variants = variants;
 
    this.is_lemmatized = data.is_lemmatized;
    this.has_stop_words = data.has_stop_words;
    this.is_selected = false;
    this.is_removed = false;
    this.is_pinned = false;
    
    this.count = data.count;
    this.is_visible = true;
    this.visible_result_ids = [];
}

app.model.category.Phrase.prototype.calculateVisibility = function() {
    var visible = true;
    if (app.model.category.use_lemmatized) {
        visible = this.is_lemmatized;
    } else {
        visible = !this.is_lemmatized;
    }
    if (!app.model.category.use_stop_words) {
       visible = visible && !this.has_stop_words;
    } 
    visible = visible || this.is_removed;
    visible = visible || this.is_pinned;
    visible = visible || this.is_selected;
    this.is_visible = visible;
}