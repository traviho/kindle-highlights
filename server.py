from flask import Flask, send_file, request
from flask_cors import CORS
from parse_clippings import get_quotes_dict_edited
from html_writer import get_html_with_script, get_html_editor_with_script
from colors import get_highlight_color_for_quote
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def send_html():
    return send_file('./kindle_highlights.html')

# Save html to local file
@app.route('/save')
def save_html():
    quotes_dict = get_quotes_dict_edited()
    html = "<div style=\"padding-left: 2%; padding-right: 2%;\">"
    for title in quotes_dict.keys():
        html += "<h2>%s</h2>" % title
        quotes_arr = quotes_dict[title]
        html += """<div style="display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; width: 96%;">
        <table border=1><th>Page</th><th>Quote</th>"""
        
        for tup in quotes_arr:
            quote = tup[0]
            highlight_color = get_highlight_color_for_quote(quote)
            if highlight_color is None:
                html += "<tr><td>%s</td><td>%s</td></tr>" % (tup[1], quote)
            else:
                html += "<tr style=\"background-color: %s\"><td>%s</td><td>%s</td></tr>" % (highlight_color, tup[1], quote)
        html += "</table></div></div><br/>"
    html += "</div>"
    html = get_html_with_script(html)
    with open("kindle_highlights.html", "w+", encoding="utf8") as f:
        f.write(html)
    return html

# Return editable html file. Save html to local file.
@app.route('/edit')
def send_edit_html():
    quotes_dict = get_quotes_dict_edited()
    html = "<div style=\"padding-left: 2%; padding-right: 2%;\">"
    for title in quotes_dict.keys():
        html += "<h2>%s</h2>" % title
        quotes_arr = quotes_dict[title]
        html += """<div style="display: flex; justify-content: center;">
        <div style="display: flex; flex-direction: column; width: 96%;">
        <table border=1><th>Page</th><th>Quote</th>"""
        
        for tup in quotes_arr:
            quote = tup[0]
            highlight_color = get_highlight_color_for_quote(quote)
            if highlight_color is None:
                html += """<tr><td>%s</td><td style="position: relative;" class="quote-td">%s <img class="highlight" style="position: absolute; right: 64px; width: 18px; height: 18px; cursor: pointer; visibility: hidden;" src="./static/edit-button.svg"/>
                <img class="combine" style="position: absolute; right: 36px; width: 18px; height: 18px; cursor: pointer; visibility: hidden;" src="./static/layers.svg"/>
                <img class="delete" style="position: absolute; right: 8px; width: 18px; height: 18px; cursor: pointer; visibility: hidden;" src="./static/trash.svg"/></td></tr>""" % (tup[1], tup[0])
            else:
                html += """<tr style=\"background-color: %s\"><td>%s</td><td style="position: relative;" class="quote-td">%s <img class="highlight" style="position: absolute; right: 64px; width: 18px; height: 18px; cursor: pointer; visibility: hidden;" src="./static/edit-button.svg"/>
                <img class="combine" style="position: absolute; right: 36px; width: 18px; height: 18px; cursor: pointer; visibility: hidden;" src="./static/layers.svg"/>
                <img class="delete" style="position: absolute; right: 8px; width: 18px; height: 18px; cursor: pointer; visibility: hidden;" src="./static/trash.svg"/></td></tr>""" % (highlight_color, tup[1], tup[0])
            
        html += "</table></div></div><br/>"
    html += "</div>"
    html = get_html_editor_with_script(html)
    save_html()
    return html

@app.route('/delete', methods=['POST'])
def delete_quote():
    quote = request.form['quote']
    quote_strip = quote.strip()
    with open("edits.json", "r") as f:
        file_data = json.load(f)
        file_data['deleted'].append(quote_strip)
    with open("edits.json", "w") as f:
        json.dump(file_data, f)
    return ""

@app.route('/combine', methods=['POST'])
def combine_quote():
    first_quote = request.form['first_quote'].strip()
    second_quote = request.form['second_quote'].strip()
    with open("edits.json", "r") as f:
        file_data = json.load(f)
        file_data['combined'][first_quote] = second_quote
    with open("edits.json", "w") as f:
        json.dump(file_data, f)
    return ""

@app.route('/highlight', methods=['POST'])
def highlight_quote():
    quote = request.form['quote']
    quote_strip = quote.strip()
    
    with open("edits.json", "r") as f:
        file_data = json.load(f)
        highlight_color = file_data['highlights'].get(quote_strip, 0)
        highlight_color = (highlight_color + 1) % 4
        file_data['highlights'][quote_strip] = highlight_color

    with open("edits.json", "w") as f:
        json.dump(file_data, f)
    highlight_color = get_highlight_color_for_quote(quote_strip)
    return "" if highlight_color is None else highlight_color

@app.route('/getJSON')
def send_json():
    return get_quotes_dict_edited()

if __name__ == '__main__':
    # APP.debug=True
    app.run()
