import json

def get_highlight_colors():
    return {0: "#ccb574", 1: "#86cad1", 2: "#bd88a8", 3: "#ffffff"}

def get_highlight_color_for_quote(quote):
    colors_dict = get_highlight_colors()
    with open("edits.json", "r") as f:
        file_data = json.load(f)
        if quote in file_data["highlights"]:
            color_index = file_data["highlights"][quote]
            return colors_dict[color_index]
        else:
            return None
