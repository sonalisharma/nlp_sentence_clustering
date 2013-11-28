/*******************************************************************************
The main clustering code. Sets up interactions and defines major functionality.
*******************************************************************************/

/** Namespace declarations **/
app = {};
app.model = {};
app.view = {};

/**
This function is called when the page loads.
*/
app.init = function() {
    app.view.form.init(); // Draws a form.
    app.model.init(); // Creates a new model to hold form data.

    // 'Categories' are phrases that occur in the sentences.
    //-- initializes the left-hand-side display.
    app.view.category.init();

    // Draws an empty table of search results.
    app.view.search_results.init();
};

/**
A convenience method for defining custom 'events' on ordinary JavaScript objects
and binding callbacks to those 'events'
*/
app.bind = function(event_name, callback) {
    $("#events").bind(event_name, callback);
};

/**
A convenience method for triggering previously-defined callbacks for events on
objects.
*/
app.trigger = function(event_name, data) {
    $("#events").trigger(event_name, data);
};
