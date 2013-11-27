goog.require('goog.string.StringBuffer');
goog.require('goog.dom');

/** Namespace declaration **/
app.view.form = {};

app.view.form.init = function () {
		app.view.form.drawForm();

		// Every time data is fetched (i.e. when the user clicks the search button),
		// re-draw the form. see line 53.
		app.bind("model.fetch", app.view.form.drawForm);

		// After data is fetched, re-draw the form.
		app.bind("model.fetched", app.view.form.drawForm);
};

// Add a form to the empty 'input' div on the main page.
app.view.form.drawForm = function() {
		var html = new goog.string.StringBuffer("");
		var query = "";
		if(app.model.form.query !== undefined) {
				query = app.model.form.query;
		}
		instance = 'interviews';
		if(app.model.form.instance !== undefined) {
				instance = app.model.form.instance;
		}
		html.append('<label>Query </label> <input name="query" value="'+query+'">');
		html.append(' <label>Collection </label>');
		html.append('<select name="instance">');
		html.append('<option value="shakespeare">Shakespeare</option>');
		html.append('<option value="acm">ACM Conference Abstracts</option>');
		html.append('</select>');
	html.append('<button id="search-button">Go</button>');
	if (app.model.form.loading) {
			html.append("<label>Loading...</label>");
	}
		$("#input").html(html.toString());
		$("option[value='"+instance+"']").prop("selected", true);
		app.view.form.bindControls();
};


// When the search button is clicked, populate the form model with the
// entered data and ask the model to get results from the server.
app.view.form.bindControls = function() {
		$("#search-button").click(function(){
			app.model.form.query = $("input[name='query']").val();
			app.model.form.instance = $("select[name='instance']").val();
			app.model.form.loading = true;
			app.trigger("model.fetch");  // in model.js
		});
};
