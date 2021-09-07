CREATE TABLE "words" (
  "id" SERIAL PRIMARY KEY,
  "simplified" string,
  "traditional" string,
  "pinyin" string,
  "english" string
);

CREATE TABLE "traditional_characters" (
  "id" SERIAL PRIMARY KEY,
  "utf" string,
  "strokes" int,
  "type" string,
  "construction" string,
  "sound_component" string,
  "radical" string
);

CREATE TABLE "simplified_characters" (
  "id" SERIAL PRIMARY KEY,
  "utf" string,
  "strokes" int,
  "type" string,
  "construction" string,
  "sound_component" string,
  "radical" string
);

CREATE TABLE "simp_to_trad" (
  "id" SERIAL PRIMARY KEY,
  "traditional_character_id" int,
  "simplified_character_id" int,
  "word_id" int
);

CREATE TABLE "simp_characters_words" (
  "id" SERIAL PRIMARY KEY,
  "word_id" int,
  "simplified_character_id" int,
  "positions" string
);

CREATE TABLE "trad_characters_words" (
  "id" SERIAL PRIMARY KEY,
  "word_id" int,
  "traditional_character_id" int,
  "positions" string
);

CREATE TABLE "radicals" (
  "id" SERIAL PRIMARY KEY,
  "simplified" string,
  "traditional" string,
  "pinyin" string,
  "english" string,
  "strokes" int
);

CREATE TABLE "frequencies" (
  "id" SERIAL PRIMARY KEY,
  "word_id" int,
  "global" int,
  "literature" int,
  "news" int,
  "tech" int,
  "blog" int,
  "weibo" int
  "tv" int
);

ALTER TABLE "simp_to_trad" ADD FOREIGN KEY ("traditional_character_id") REFERENCES "traditional_characters" ("id");

ALTER TABLE "simp_to_trad" ADD FOREIGN KEY ("simplified_character_id") REFERENCES "simplified_characters" ("id");

ALTER TABLE "simp_to_trad" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");

ALTER TABLE "simp_characters_words" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");

ALTER TABLE "simp_characters_words" ADD FOREIGN KEY ("simplified_character_id") REFERENCES "simplified_characters" ("id");

ALTER TABLE "trad_characters_words" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");

ALTER TABLE "trad_characters_words" ADD FOREIGN KEY ("traditional_character_id") REFERENCES "traditional_characters" ("id");
