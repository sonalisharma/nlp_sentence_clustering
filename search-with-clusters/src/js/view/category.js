goog.require('goog.string.StringBuffer');
goog.require('goog.dom');

/**Namespace declaration **/
app.view.category = {}

/** Number of phrases to display **/
app.view.category.number_of_top_phrases = 300;

app.view.category.init = function () {
    app.bind("model.fetched", app.view.category.draw);
    app.bind("model.changed", app.view.category.draw);
}


/** Draws the categories on the left hand side and sets up interactivity
with the search results. **/
app.view.category.draw = function(){
    var t1 = new Date().getTime();
    var html = new goog.string.StringBuffer("");
    html.append("<div class='category options'></div>");
    html.append("<div class='category pane selected'></div>");
    html.append("<div class='category pane removed'></div>");
    html.append("<div class='category pane unmarked'></div>");
    $("#categories").html(html.toString())
    app.view.category.drawOptions();
    app.view.category.drawCategories();
    var t2 = new Date().getTime();
    console.log("Time to draw categories: "+((t2-t1)/1000)+"s");
}

app.view.category.drawOptions = function() {
    var html = new goog.string.StringBuffer("");
    html.append("<input class='category options' type='checkbox' name='use_lemmatized'> Stems only</input><br>")
    html.append("<input class='category options' type='checkbox' name='use_stop_words'>  Function words </input>")
    $("div.category.options").append(html.toString());
    $("input.category.options[name='use_lemmatized']").prop(
        "checked", app.model.category.use_lemmatized);
    $("input.category.options[name='use_stop_words']").prop(
        "checked", app.model.category.use_stop_words);
    $("input.category.options").change(function() {
        app.model.category[$(this).attr("name")] = $(this).prop("checked");
        app.trigger("model.changed");
    })
};

app.view.category.drawCategories = function() {
    var data = app.model.getVisiblePhrases();
    data.forEach(app.view.category.drawCategory);
}

app.view.category.drawCategory = function(category){
    html = new goog.string.StringBuffer("");
    html.append("<li is_pinned='false' class='category' phrase_id='" + category.id + "'>");
        html.append("<span class='category selectors'>");
            html.append("<span class='remove category button'></span>")
            html.append("<input name='is_selected' type='checkbox'>")
        html.append("</span>");
        html.append("<span class='category label'>");
            html.append(category.phrase)
        html.append('</span>');
        html.append("<span class='category count'>(");
            html.append(category.count)
        html.append(")</span>");
    html.append("</li>");
    var div = $("div.category.pane.unmarked");
    if (category.is_selected) {
        div = $("div.category.pane.selected");
    } else if (category.is_removed) {
        div = $("div.category.pane.removed");
    }
    div.append(html.toString());
    
    // Alter the base appearance based on the category's state.
    var view = div.children().last();
    view.attr("is_pinned", category.is_pinned);
    view.attr("active", category.count > 0);
    view.attr("is_removed", category.is_removed);
    view.find("input[name='is_selected']").prop("checked", category.is_selected);
    if (category.is_selected) {
        var index = app.model.phrases.selected_ids.indexOf(category.id);
        view.css("color", app.view.category.getHighlightColor(index));
    }
    app.view.category.bindCategoryControls(view);
}

app.view.category.bindCategoryControls = function(view) {
    // Filtering by a category.
    view.click(function() {
        var category = app.view.category.getPhrase($(this));
        var is_pinned = !category.is_pinned;
        app.model.phrases.unpin();
        category.is_pinned = is_pinned;
        if (is_pinned) {
            app.model.phrases.pinned_id = category.id;
        } else {            
            app.model.phrases.pinned_id = null;
        }
        app.trigger("model.changed");
    })
    
    // Selecting a category.
    view.find("input[name='is_selected']").change(function() {
        var category = app.view.category.getPhrase($(this));
        category.is_selected = $(this).prop("checked");
        app.model.phrases.unpin();
        app.trigger("model.changed");
    })
    
    // Removing a category.
    view.find(".button.remove.category").click(function() {
        var category = app.view.category.getPhrase($(this));
        category.is_removed = !category.is_removed;
        app.model.phrases.unpin();
        app.trigger("model.changed");
    })
}

app.view.category.getPhrase = function(view) {
    var id = view.closest('li.category').attr("phrase_id");
    return app.model.getPhrase(id);
}

app.view.category.getHighlightColor = function(index) {
    if (index >= 0) {
        var colors = ['darkgoldenrod', 'firebrick', 'skyblue', 'olivedrab'];
        var normalized = index % colors.length;
        return colors[normalized];   
    } else {
        return 'lightskyblue';
    }
}