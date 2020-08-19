import os
import re
import sys
import json

def strip_bad_chars(line):
    construct = ""
    for c in line:
        if ord(c) <= 256:
            construct += c
    return construct.strip()

# The dictionary contains {title: [(quote, page, date)]}
def get_quotes_dict(filename="My Clippings.txt"):
    quotes_dict = {}
    with open(filename, "r", encoding="utf8") as f:
        line = None
        index = 0
        title = ""
        quote = ""
        metadata = ""
        do_save = True

        while line != "":
            line = f.readline()
            if index == 0:
                title = strip_bad_chars(line)
            elif index == 1:
                metadata = strip_bad_chars(line)
                if "Bookmark" in metadata:
                    do_save = False
            elif line == "==========\n":
                # End of quote segment
                if do_save:
                    quotes_arr = quotes_dict.get(title, [])
                    m = re.search('Your Highlight on page ([\d-]+) \|.*Added on (.*)$', metadata)
                    page = m.group(1) if len(m.groups()) > 0 else None
                    datetime = m.group(2) if len(m.groups()) > 1 else None
                    quotes_arr.append((quote, page, datetime))
                    quotes_dict[title] = quotes_arr
                index = -1
                quote = ""
                metadata = ""
                do_save = True
            elif not line == '\n':
                quote = quote + line
            index += 1
    return quotes_dict

def make_edits(quotes_dict):
    quotes_dict_new = {}
    with open("edits.json", "r") as f:
        file_data = json.load(f)
    deleted_arr = file_data["deleted"]
    combined_dict = file_data["combined"]
    deleted_set = set(deleted_arr)
    combined_values_set = set(combined_dict.values())

    for title in quotes_dict:
        for tup in quotes_dict[title]:
            quote = tup[0]
            quote_strip = quote.strip()
            page = tup[1]
            datetime = tup[2]
            if quote_strip in combined_dict:
                quote_strip += " " + combined_dict[quote_strip]
            
            if quote_strip not in deleted_set and quote_strip not in combined_values_set:
                quotes_arr = quotes_dict_new.get(title, [])
                quotes_arr.append((quote_strip, page, datetime))
                quotes_dict_new[title] = quotes_arr
    return quotes_dict_new

def get_quotes_dict_edited(filename="My Clippings.txt"):
    return make_edits(get_quotes_dict(filename))

quotes_dict = get_quotes_dict_edited(sys.argv[1]) if len(sys.argv) > 1 else get_quotes_dict_edited()
