import re
import string


class Minifier:
    _TABLE = str.maketrans("", "", string.ascii_lowercase)

    @classmethod
    def _remove_lowercase(cls, input_dict):
        for key in input_dict.keys():
            input_dict[key] = "".join(key[0].upper() + key[1:]).translate(cls._TABLE)

            add_number = 1
            number_added = False
            while input_dict[key] in [v for k, v in input_dict.items() if k != key]:
                input_dict[key] = (
                    input_dict[key][:-1] + str(add_number) if number_added else input_dict[key] + str(add_number)
                )
                number_added = True
                add_number += 1

        return input_dict

    @classmethod
    def minify(cls, input_text):
        # Remove comment blocks
        text = re.sub(r"--\[\[[^\]\]]*]]", "", input_text, flags=re.MULTILINE)

        # Remove single-line comments
        text = re.sub(r"[ \t]*--(?!\[\[).*$", "", text, flags=re.MULTILINE)

        # Find all global/local variable names
        found_variables = {k: "" for k in re.findall(r"(?<=\B[#$])[_A-za-z0-9]+(?=[= &|<>\-+%*\/^])", text)}

        # Find all custom function names
        found_functions = {k: "" for k in re.findall(r"(?<=on )[_A-za-z0-9]+(?= then)", text)}

        # Shorten variable/function names by removing lowercase letters
        found_variables = cls._remove_lowercase(found_variables)
        found_functions = cls._remove_lowercase(found_functions)

        for k, v in found_variables.items():
            text = re.sub(rf"(?<=\B[#$]){k}(?=[= &|<>\-+%*\/^);,])", v, text)

        for k, v in found_functions.items():
            text = re.sub(rf"{k}(?= then|\()", v, text)

        # Remove empty lines
        text = re.sub(r"^(?:[\t ]*(?:\r?\n|\r))+", "", text, flags=re.MULTILINE)

        # Remove spaces and tabs at beginning and end of lines
        text = re.sub(r"^[\t| ]+|[\t| ]+$", "", text, flags=re.MULTILINE)

        # Remove newline after line ending with 'then' or 'else'
        text = re.sub(r"(?<=then|else)\r{0,1}\n{1}", " ", text, flags=re.MULTILINE)

        # Remove newline after line ending with all possible operators
        text = re.sub(r"(?<=[;=&|<>\-+%*\/^()])\r{0,1}\n{1}", "", text, flags=re.MULTILINE)

        # Remove newline after line ending with 'end', except for last end of function
        text = re.sub(r"(?<=end)\s*(?!\s*on |\Z)", " ", text, flags=re.MULTILINE)

        # Correct spaces around equal signs
        text = re.sub(r"(?<![<>]) *= *(?=-*\d;|[#$@%?].+;)", " = ", text, flags=re.MULTILINE)

        # Correct spaces around double equal signs
        text = re.sub(r" *== *", " == ", text, flags=re.MULTILINE)

        # Remove all spaces around comma signs
        text = re.sub(r"(?<=[)_A-Za-z0-9]) *, *\s*(?=[$#@?_A-Za-z0-9])", ",", text, flags=re.MULTILINE)

        return text
