# A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with "traditional","simplified", "pinyin", and "english" keys.

# Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on line 13.

# Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program will try to parse it and you will get an error message.

# Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.

# This code was written by Franki Allegra in February 2020.

# open CEDICT file
import re
from db import insert_list, insert, raw, select, update
from utils import cn_re
from tqdm import tqdm
import traceback

with open('./src/data/raw/2_dict/cedict_1_0_ts_utf-8_mdbg.txt') as file:
    text = file.read()
    lines = text.split('\n')
    dict_lines = list(lines)
    list_of_dicts = []

    def is_vowel(char):
        all_vowels = 'aeiou'
        return char in all_vowels

    def split_pinyin_tone(pinyin):
        if pinyin:
            syllable = pinyin.rstrip('0123456789')
            tone = pinyin[len(syllable):]

            syl_split = ["", ""]
            index = 0
            for i in range(len(syllable)):
                char = syllable[i]
                if is_vowel(char) and index == 0:
                    index = 1
                syl_split[index] += char
            return [syl_split[0], syl_split[1], tone]
        return [None] * 3

# define functions

    def parse_line(line):
        parsed = {}
        if line == '':
            dict_lines.remove(line)
            return 0
        line = line.rstrip('/')
        line = line.split('/')
        if len(line) <= 1:
            return 0
        # Rejoin english definitions
        english = "/".join([e for i, e in enumerate(line) if i > 0])
        char_and_pinyin = line[0].split('[')
        characters = char_and_pinyin[0]
        characters = characters.split()
        traditional = characters[0]
        simplified = characters[1]
        pinyin = char_and_pinyin[1]
        pinyin = pinyin.rstrip()
        pinyin = pinyin.rstrip("]")
        # pinyin_split = split_pinyin_tone(pinyin)
        parsed['traditional'] = traditional
        parsed['simplified'] = simplified
        parsed['pinyin'] = pinyin
        parsed['english'] = english
        list_of_dicts.append(parsed)

    removables = [
        "Suzhou numeral system",
        "zero",
        "iteration mark",
        "component in Chinese characters",
        "character used in Taiwan as a substitute for a real name",
        "euphemistic variant of 屄",
        "(slang) (Tw) to steal",
        "percent (Tw)",
        "swastika",
    ]

    def contains(definition, content_list):
        for x in range(0, len(content_list), 1):
            rem = content_list[x]
            if rem in definition:
                return True
        return False

    def contains_removable(entry):
        is_invalid_pinyin = False
        is_contain_unwanted = False
        for key in entry:
            value = entry[key]
            if key == "pinyin":
                if not value or ("xx5" in value) or len(value) <= 1:
                    is_invalid_pinyin = True
                    break
            else:
                if contains(value, removables):
                    is_contain_unwanted = True
                    break
        return is_contain_unwanted or is_invalid_pinyin

    radicals = [
        "radical in Chinese character",
        "Kangxi radical",
        "grass radical"
    ]

    def is_radical(definition):
        return contains(definition, radicals)

    def remove():
        for x in range(len(list_of_dicts)-1, -1, -1):
            # Remove surnames, Suzhou numeral system
            is_remove = False
            definition = list_of_dicts[x]['english']
            if ("surname " in definition and # Remove surnames
                list_of_dicts[x]['traditional'] == list_of_dicts[x+1]['traditional']) or contains_removable(list_of_dicts[x]):
                is_remove = True

            if is_remove:
                list_of_dicts.pop(x)

    def parse_d():
        # make each line into a dictionary
        print("Parsing dictionary . . .")
        for line in tqdm(dict_lines):
            parse_line(line)

        # remove entries for surnames from the data (optional):

        print("Removing unwanted values . . .")
        remove()
        return list_of_dicts


parsed_dict = parse_d()

# # Write to DB
def write_lines_db(parsed_dict):
    print("Writing to DB . . .")
    try:
        for l in tqdm(range(0, len(parsed_dict), 1)):
            line = parsed_dict[l]
            # Check if word already exists in dictionary
            word_ex = select("words", ["id", "simplified", "traditional", "pinyin", "english"], "simplified = %s AND traditional = %s AND pinyin = %s AND english = %s", (line["simplified"], line["traditional"], line["pinyin"], line["english"]))
            
            # If word not in dictionary, insert it
            if len(word_ex) == 0:
                # If it is a character
                if len(line["traditional"]) == 1:
                    # Word
                    word = insert("words", line)
                    variant = 'ts' if line["traditional"] == line["simplified"] else 't'
                    
                    # Characters - create if no pre-existing, check based on traditional characters
                    char_t_ex = select("characters", ["id"], "character = %s AND (variant = 't' OR variant = 'ts')", (line["traditional"]))
                    char_t = char_t_ex[0] if len(char_t_ex) > 0 else None
                    char_s = None
                    
                    # No existing character, insert character
                    if char_t is None:
                        new_vals = {
                            "character": line["traditional"],
                            "variant": variant
                        }
                        # If same character for trad/simp, insert trad character only
                        char_t = insert("characters", new_vals)
                        
                        if variant == 't':
                        # Otherwise, also insert simp with traditional_id reference
                            char_s = insert("characters", {
                                "character": line["simplified"],
                                "variant": 's',
                                "traditional_id": char_t[0]
                            })
                    
                    if char_t:
                        char_word_vals = (
                            (word[0], char_t[0], "0"),
                            (word[0], char_s[0], "0")
                        ) if char_s is not None else (
                            (word[0], char_t[0], "0"),
                        )
                        # Characters to words
                        insert_list("characters_words", ["word_id", "character_id", "positions"], values=char_word_vals)
                else:
                    word = insert("words", line)
    except (Exception) as error:
        traceback.print_exc()

def fill_char_words(chars_list):
    print("Referencing compound words")
    variant_key = "traditional"
    
    for char_ind in tqdm(range(0, len(chars_list), 1)):
        char = chars_list[char_ind]
        # Select words containing character
        words = select("words", ["id", variant_key, "pinyin"], (variant_key + " LIKE '%%%s%%' AND LENGTH(" + variant_key + ") > 1") % (char[1],))
        
        chregex = re.compile(char[1])
        upd_vals = []
        
        # Find matching words
        for word in words:
            positions = []
            matches = re.finditer(chregex, word[1])
            for m in matches:
                positions.append(str(m.start()))
            posstr = ",".join(positions)
            upd_vals.append((word[0], char[0], posstr))
        
        # Save word-character link
        insert_list("characters_words", ["word_id", "character_id", "positions"], values=tuple(upd_vals))

write_lines_db(parsed_dict)
t_chars = select("characters", ["id", "character", "variant", "traditional_id"], "(variant = 't' OR variant = 'ts')")
fill_char_words(t_chars)