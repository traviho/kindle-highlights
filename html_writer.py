def get_html_with_script(body):
    return """<!DOCTYPE html>
<html>
<head lang="en">
        <meta charset="utf-8">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
</head>
<body>
<div style="padding-left: 2%; padding-top: 12px;"><label for="search-input">Search: </label><input type="text" id="search-input" /></div>
""" + body + """<script>
$(document).ready(function(){
        $("#search-input").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("h2").filter(function(index) {
                        console.log(index)
                        var toggle_header = $(this).text().toLowerCase().indexOf(value) > -1;
                        if (toggle_header) {
                                // If it matches title show all quotes
                                $(this).toggle(toggle_header);
                                $("table").eq(index).filter(function() {
                                        $(this).toggle(true);
                                        // all children rows to true, as can be false from previous selection
                                        $(this).find("tr").filter(function() {
                                                $(this).toggle(true);
                                        });
                                });
                        } else {
                                // If it doesn't match title, but has any quotes inside, keep it
                                var total = $("table").eq(index).children("tr").length;
                                var count = 0;
                                $("table").eq(index).find("tr").filter(function() {
                                        toggle_row = $(this).text().toLowerCase().indexOf(value) > -1;
                                        $(this).toggle(toggle_row);
                                        if (toggle_row) {
                                                count += 1;
                                        }
                                });
                                if (count === 0) {
                                        $(this).toggle(false);
                                        $("table").eq(index).toggle(false);
                                } else {
                                        $(this).toggle(true);
                                        $("table").eq(index).toggle(true);
                                }
                        }
                });
        });
});
</script>
</body>
</html>"""

def get_html_editor_with_script(body):
        return """<!DOCTYPE html>
<html>
<head lang="en">
        <meta charset="utf-8">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
</head>
<body>
<div style="padding-left: 2%; padding-top: 12px;"><label for="search-input">Search: </label><input type="text" id="search-input" /></div>
<div id="clip-marker" style="position: fixed; top: 12px; right: 12px; width: 12px; height: 12px; background-color: red; border-radius: 6px; visibility: hidden;"></div>
""" + body + """<script>
var combine_quote = null;
var combine_quote_element = null;
$(document).ready(function(){
        $("#search-input").on("keyup", function() {
                var value = $(this).val().toLowerCase();
                $("h2").filter(function(index) {
                        console.log(index)
                        var toggle_header = $(this).text().toLowerCase().indexOf(value) > -1;
                        if (toggle_header) {
                                // If it matches title show all quotes
                                $(this).toggle(toggle_header);
                                $("table").eq(index).filter(function() {
                                        $(this).toggle(true);
                                        // all children rows to true, as can be false from previous selection
                                        $(this).find("tr").filter(function() {
                                                $(this).toggle(true);
                                        });
                                });
                        } else {
                                // If it doesn't match title, but has any quotes inside, keep it
                                var total = $("table").eq(index).children("tr").length;
                                var count = 0;
                                $("table").eq(index).find("tr").filter(function() {
                                        toggle_row = $(this).text().toLowerCase().indexOf(value) > -1;
                                        $(this).toggle(toggle_row);
                                        if (toggle_row) {
                                                count += 1;
                                        }
                                });
                                if (count === 0) {
                                        $(this).toggle(false);
                                        $("table").eq(index).toggle(false);
                                } else {
                                        $(this).toggle(true);
                                        $("table").eq(index).toggle(true);
                                }
                        }
                });
        });
        $(this).find(".highlight").click(function() {
                const quote = $(this).parent().text();
                const trow_element = $(this).parent().parent();
                $.ajax({
                        type: "POST",
                        url: "http://localhost:5000/highlight",
                        data: {quote: quote},
                        success: function(color) {
                                console.log(color)
                                trow_element.css("background-color", color)
                        },
                        dataType: "text"
                });
                console.log("highlight " + quote);
        });
        $(this).find(".quote-td").click(function() {
                const quote = $(this).text();
                const new_quote_element = $(this);
                if (combine_quote != null && quote !== combine_quote) {
                        $.ajax({
                                type: "POST",
                                url: "http://localhost:5000/combine",
                                data: {first_quote: quote, second_quote: combine_quote},
                                success: function(text) {
                                        const new_quote = quote + " " + combine_quote
                                        new_quote_element.text(new_quote);
                                        combine_quote_element.hide()
                                        combine_quote = null;
                                        combine_quote_element = null;
                                        $("#clip-marker").css('visibility', 'hidden');
                                },
                                dataType: "text"
                                
                        });
                }
        });
        $(this).find(".combine").click(function() {
                const quote = $(this).parent().text();
                if (combine_quote == null) {
                        $("#clip-marker").css('visibility', 'visible');
                        combine_quote = quote;
                        combine_quote_element = $(this).parent().parent();
                } else {
                        combine_quote = null;
                        $("#clip-marker").css('visibility', 'hidden');
                        combine_quote_element = null;
                }
                console.log("combine " + quote);
        })
        $(this).find(".delete").click(function() {
                const quote = $(this).parent().text();
                $.ajax({
                        type: "POST",
                        url: "http://localhost:5000/delete",
                        data: {quote: quote},
                });
                console.log("delete " + quote);
                $(this).parent().parent().hide();
        })
        jQuery.fn.visible = function() {
                return this.css('visibility', 'visible');
        };
        jQuery.fn.invisible = function() {
                return this.css('visibility', 'hidden');
        };
        $(document).on('mouseenter', 'tr', function () {
                $(this).find("img").visible();
        }).on('mouseleave', 'tr', function () {
                $(this).find("img").invisible();
        });
});
</script>
</body>
</html>"""