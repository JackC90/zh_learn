# ~ SAFE ~
# Text analysis using IDS (Ideographic Description Sequence)
from tqdm import tqdm
from db import insert_list, insert, raw, select, update
import pandas as pd
import traceback
    
def write_comp_db():
    print("Writing to DB . . .")
    try:
        fields = ["utf", "composition", "formation"]
        # Create IDS dataframe
        idsdf = pd.read_csv("./src/data/raw/3_compose/ids-analysis.txt", names=['utf',  'character',  'composition', 'formation', 'reference', 'notes'], sep='\t')
        idsdf.where(pd.notnull(idsdf), None)
        
        # Get characters list from DB
        chars = select("characters", ["id", "character", "variant", "traditional_id"])
        
        for l in tqdm(range(0, len(chars), 1)):
            char = chars[l]
            
            # Find character in IDS file
            ids_match = idsdf[idsdf["character"] == char[1]]
            if ids_match.shape[0] > 0:
                ids = ids_match.iloc[0]
                cols = []
                vals = []
                for field in fields:
                    if isinstance(ids[field], str):
                        cols.append(field)
                        vals.append(ids[field])
                update("characters", cols, tuple(vals), "id = %s" % (char[0],))

    except (Exception) as error:
        print(error)
        traceback.print_exc()
        
def write_stroke_db():
    print("Writing to DB . . .")
    try:
        # Create IDS dataframe
        idsdf = pd.read_csv("./src/data/raw/3_compose/ucs-strokes.txt", names=['utf',  'character',  'strokes'], sep='\t')
        idsdf.where(pd.notnull(idsdf), None)
        
        # Get characters list from DB
        chars = select("characters", ["id", "character", "variant", "utf","traditional_id"])
        
        for l in tqdm(range(0, len(chars), 1)):
            char = chars[l]
            
            # Find character in IDS file
            ids_match = idsdf[idsdf["character"] == char[1]]
            if ids_match.shape[0] > 0:
                ids = ids_match.iloc[0]
                cols = ["strokes"]
                strokes = int(ids["strokes"].split(",")[0]) if isinstance(ids["strokes"], str) and len(ids["strokes"]) > 0 else 0
                vals = [strokes]
                update("characters", cols, tuple(vals), "id = %s" % (char[0],))

    except (Exception) as error:
        print(error)
        traceback.print_exc()

write_comp_db()
write_stroke_db()