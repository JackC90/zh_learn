pyenv virtualenv 3.9.1

252
351
---
603
4375
---
4978
 965
----
5943

Run migration with 
```
psql -U postgres -d cn_learn  -f ./results/words_202207052236.sql
psql -U postgres -d cn_learn  -f ./results/radicals_202207052236.sql
psql -U postgres -d cn_learn  -f ./results/_characters__202207052236.sql
psql -U postgres -d cn_learn  -f ./results/characters_words_202207052236.sql

psql -U postgres -d cn_learn  -f ./results/frequencies_202207052236.sql
psql -U postgres -d cn_learn  -f ./results/spoken_frequencies_202207052236.sql


psql -U postgres -d cn_learn  -f ./results/books_202207052236.sql
psql -U postgres -d cn_learn  -f ./results/sentences_202207052236.sql
```