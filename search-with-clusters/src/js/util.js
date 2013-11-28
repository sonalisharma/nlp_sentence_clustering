/** Namespace declaration. **/
app.util = {};

app.util.newlineToBr = function(text) {
    return text.replace(/\n/g, '<br/>');
}