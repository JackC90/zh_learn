from db import create_table, raw

def drop_create_tables():
  create_table("words", [
    '"id" SERIAL PRIMARY KEY',
    '"simplified" varchar',
    '"traditional" varchar',
    '"pinyin" varchar',
    '"english" text'
  ])

  create_table("characters", [
    '"id" SERIAL PRIMARY KEY',
    '"character" varchar',
    
    # 't' - traditional
    # 's' - simplified
    # 'ts' - both
    '"variant" varchar',
    '"traditional_id" int',
    '"utf" varchar',
    '"strokes" int',
    '"formation" varchar',
    '"composition" text',
    '"sound_component" varchar',
    '"meaning_component" varchar',
    '"radical" varchar',
    '"radical_id" int'
  ])

  create_table("characters_words", [
    '"id" SERIAL PRIMARY KEY',
    '"word_id" int',
    '"character_id" int',
    '"positions" varchar'
  ])

  create_table("radicals", [
    '"id" SERIAL PRIMARY KEY',
    '"simplified" varchar',
    '"traditional" varchar',
    '"pinyin" varchar',
    '"english" varchar',
    '"strokes" int'
    '"variants" varchar',
    '"kangxi" int'
  ])

  create_table("frequencies", [
    '"id" SERIAL PRIMARY KEY',
    '"word_id" int',
    '"global" int',
    '"literature" int',
    '"news" int',
    '"tech" int',
    '"blog" int',
    '"weibo" int'
    '"spoken" int'
  ])
  
  create_table("spoken_frequencies", [
    '"id" SERIAL PRIMARY KEY',
    '"word_id" int',
    '"pos" varchar',
    '"frequency" int',
  ])

  raw("""
    ALTER TABLE "characters_words" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");
  """)

  raw("""
    ALTER TABLE "characters_words" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");
  """)

  raw("""
    ALTER TABLE "characters" ADD FOREIGN KEY ("radical_id") REFERENCES "radicals" ("id");
  """)

  raw("""
    ALTER TABLE "characters" ADD FOREIGN KEY ("traditional_id") REFERENCES "characters" ("id");
  """)
  
  raw("""
    ALTER TABLE "frequencies" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");
  """)
  
  raw("""
    ALTER TABLE "spoken_frequencies" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");
  """)
  
  raw("""
    ALTER TABLE "frequencies" ADD CONSTRAINT frequencies_word_id_un UNIQUE ("word_id");
  """)


drop_create_tables()

