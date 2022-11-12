from preprocessor import get_lines, extract_language_name, parse_raw_text, extract_paranthesis
from preprocessor.parser import get_lines, extract_language_name, parse_raw_text, extract_paranthesis

def generate_df(file, langs):
    # produced result shape (num_main_header * num_sub_header)
    # data = {
    #         1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    #         2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #     }
    #

    dictionary = {}
    idx = 0
    for line in get_lines(file):
        if not line == "\n":
            splitted_line = line.split(" ")
            if not splitted_line[0] in langs:
                print("not in langs: ", splitted_line[0], line)

            lang = extract_language_name(line)
            word = parse_raw_text(line)
            definition = extract_paranthesis(line)
            # mux = pd.MultiIndex.from_product([['Start', 'Intermediary', 'End'], ["word", "gloss", "transition"]])
            # sub_columns = []
            temp_data = [
                word,
                definition,
                ""
            ]
            # temp_df = pd.DataFrame.from_dict(data=temp_data, orient='index', columns=mux)
            if idx in dictionary.keys():
                for item in temp_data:
                    dictionary[idx].append(" ".join(item))
            else:
                dictionary.update({idx: []})
                for item in temp_data:
                    dictionary[idx].append(" ".join(item))
        else:
            # New word in the tokenizer
            idx += 1

    return dictionary


def export_to(file, langs, to_format="json"):
    dictionary = {}
    idx = 0
    for line in get_lines(file):
        if not line == "\n":
            splitted_line = line.split(" ")

            if to_format == "json":
                to_json(idx, line, dictionary)
            elif to_format == "dataframe":
                # produced result shape (num_main_header * num_sub_header)
                # data = {
                #         1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                #         2: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                #     }
                #

                to_dataframe(idx, line, dictionary)

            if not splitted_line[0] in langs:
                print("not in langs: ", splitted_line[0], line)
        else:
            # New word in the tokenizer
            idx += 1

    return dictionary


def to_dataframe(idx, line, dictionary):
    lang = extract_language_name(line)
    word = parse_raw_text(line)
    definition = extract_paranthesis(line)
    # mux = pd.MultiIndex.from_product([['Start', 'Intermediary', 'End'], ["word", "gloss", "transition"]])
    # sub_columns = []
    temp_data = [
        word,
        definition,
        ""
    ]
    # temp_df = pd.DataFrame.from_dict(data=temp_data, orient='index', columns=mux)
    if idx in dictionary.keys():
        for item in temp_data:
            dictionary[idx].append(" ".join(item))
    else:
        dictionary.update({idx: []})
        for item in temp_data:
            dictionary[idx].append(" ".join(item))


def to_json(idx, line, dictionary):
    lang = extract_language_name(line)
    word = parse_raw_text(line)
    definition = extract_paranthesis(line)
    if idx in dictionary.keys():
        dictionary[idx].append({
            "lang": lang,
            "word": word,
            "definition": definition
        })
    else:
        dictionary.update({idx: [
            {
                "lang": lang,
                "word": word,
                "definition": definition
            }
        ]})