# Frequencies list
from tqdm import tqdm
from db import insert_list, insert, raw, select, update
import pandas as pd
import traceback

def write_freq_db():
    print("Writing to DB . . .")
    try:
        files = [
            {
                "filename": 'blogs_wordfreq.release_UTF-8.txt',
                "column": 'blog'
            },
            {
                "filename": 'global_wordfreq.release_UTF-8.txt',
                "column": 'global'
            },
            {
                "filename": 'literature_wordfreq.release_UTF-8.txt',
                "column": 'literature'
            },
            {
                "filename": 'news_wordfreq.release_UTF-8.txt',
                "column": 'news'
            },
            {
                "filename": 'technology_wordfreq.release_UTF-8.txt',
                "column": 'tech'
            },
            {
                "filename": 'weibo_wordfreq.release_UTF-8.txt',
                "column": 'weibo'
            }
            # {
            #     "encoding": 'utf-8-sig',
            #     "filename": 'SUBTLEX-CH-WF_PoS',
            #     "column": 'tv'
            # }
        ]
        
        dfs = []
        for f in range(0, len(files), 1):
            # Create dataframe based on file
            fileparams = files[f]
            df = pd.read_csv("./src/data/raw/4_freq/" + fileparams["filename"], names=['word',  'freq'], sep='\t', encoding=(fileparams["encoding"] if "encoding" in fileparams else None))
            df.where(pd.notnull(df), None)
            dfs.append(df)
        
        words = select("words", ["id", "simplified", "traditional", "pinyin"])

        print("Processing words")
        
        for w_index in tqdm(range(0, len(words), 1)):
            word = words[w_index]
            insert_vals = { "word_id": word[0] }
            has_freq = False
            
            # Find frequencies in each file
            for f in range(0, len(dfs), 1):
                df = dfs[f]
                fileparams = files[f]
                words_df = df.loc[(df['word'] == word[1]) | (df['word'] == word[2])]
                if not words_df.empty and words_df.shape[0] > 0:
                    df_word, df_freq = words_df.iloc[0].values
                    has_freq = True
                    insert_vals[fileparams["column"]] = df_freq.item()             
            
            if has_freq:
                insert("frequencies", insert_vals)
    except (Exception):
        traceback.print_exc()


write_freq_db()