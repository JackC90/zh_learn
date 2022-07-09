CREATE TABLE "words" (
  "id" SERIAL PRIMARY KEY,
  "simplified" varchar,
  "traditional" varchar,
  "pinyin" varchar,
  "english" varchar
);

CREATE TABLE "characters" (
  "id" SERIAL PRIMARY KEY,
  "character" varchar,
  "variant" varchar,
  "traditional_id" int
  "utf" varchar,
  "strokes" int,
  "formation" varchar,
  "composition" varchar,
  "sound_component" varchar,
  "meaning_component" varchar,
  "radical" varchar,
  "radical_id" int
);

CREATE TABLE "characters_words" (
  "id" SERIAL PRIMARY KEY,
  "word_id" int,
  "character_id" int,
  "positions" varchar
);

CREATE TABLE "radicals" (
  "id" SERIAL PRIMARY KEY,
  "simplified" varchar,
  "traditional" varchar,
  "pinyin" varchar,
  "english" varchar,
  "strokes_traditional" int
  "strokes_simplified" int
  "variants" int
  "kangxi" int
);

CREATE TABLE "frequencies" (
  "id" SERIAL PRIMARY KEY,
  "word_id" int,
  "global" int,
  "literature" int,
  "news" int,
  "tech" int,
  "blog" int,
  "weibo" int,
  "spoken" int
);

CREATE TABLE "spoken_frequencies" (
  "id" SERIAL PRIMARY KEY,
  "word_id" int,
  "pos" varchar,
  "frequency" int
);

ALTER TABLE "characters" ADD FOREIGN KEY ("traditional_id") REFERENCES "characters" ("id");

ALTER TABLE "characters_words" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");

ALTER TABLE "characters_words" ADD FOREIGN KEY ("character_id") REFERENCES "characters" ("id");

ALTER TABLE "frequencies" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");

ALTER TABLE "sentences" ADD FOREIGN KEY ("book_id") REFERENCES "books" ("id");

ALTER TABLE "spoken_frequencies" ADD FOREIGN KEY ("word_id") REFERENCES "words" ("id");
