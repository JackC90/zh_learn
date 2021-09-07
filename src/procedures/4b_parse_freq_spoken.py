# Frequencies list (Spoken)
from tqdm import tqdm
import numpy as np
from db import insert_list, insert, raw, select, update
import pandas as pd
import traceback

def write_freq_db():
    print("Writing to DB . . .")
    try:
        fileparams =  {
            "encoding": 'GBK',
            "filename": 'SUBTLEX-CH-WF_PoS',
            "column": 'tv'
        }
        df = pd.read_csv("./src/data/raw/4_freq/" + fileparams["filename"], names=['Lemma', 'WF_Lemma',	'WordForm', 'PoS',	'WF_PoS'], sep='\t', encoding=fileparams["encoding"], skiprows=[0, 1, 2], skip_blank_lines=True)
        df.where(pd.notnull(df), None)
        
        print("Processing words")
        word_db = None
        
        for index, row in tqdm(df.iterrows(), total=df.shape[0]):
            lemma, wf_lemma, wf, pos, wf_pos = row
            if isinstance(lemma, str):
                if '@' in lemma and type(word_db) is tuple:
                    # Belongs to same Lemma set, variant word forms / PoS
                    line = { "word_id": word_db[0], "pos": pos, "frequency": wf_pos }
                    insert("spoken_frequencies", line)
                else:
                    # New Lemma set
                    lemma_tr = lemma.strip()
                    word_ex = select("words", ["id", "simplified", "traditional", "pinyin", "english"], "simplified = %s OR traditional = %s", (lemma_tr, lemma_tr))
                    
                    if len(word_ex) != 0:
                        word_0 = word_ex[0]
                        word_db = word_0
                        frequencies = select("frequencies", ["id", "word_id"], "word_id = %s", (word_0[0],))
                        frequency = frequencies[0] if frequencies and len(frequencies) > 0 else None
                        # Update frequency
                        if frequency:
                            update("frequencies", ["spoken"], (wf_lemma,), "id = %s" % (frequency[0],))
                        else:
                            new_freq = { "word_id": word_0[0], "spoken": wf_lemma }
                            insert("frequencies", new_freq)
                        # Insert into spoken table
                        line = { "word_id": word_0[0], "pos": "all", "frequency": wf_lemma }
                        insert("spoken_frequencies", line)
                    else:
                        # Clear word
                        word_db = None
    except (Exception):
        traceback.print_exc()


write_freq_db()