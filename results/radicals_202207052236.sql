SET CLIENT_ENCODING TO 'utf8';

ALTER SEQUENCE radicals_id_seq RESTART;

INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('一','一','yī','one',1,NULL,1,1),
	 ('丨','丨','shù','line',1,NULL,2,1),
	 ('丶','丶','diǎn','dot',1,NULL,3,1),
	 ('丿','丿','piě','slash',1,'乀,乁',4,1),
	 ('乙','乙','yǐ','second',1,'乚,乛',5,1),
	 ('亅','亅','gōu','hook',1,NULL,6,1),
	 ('二','二','èr','two',2,NULL,7,2),
	 ('亠','亠','tóu','lid',2,NULL,8,2),
	 ('人','人','rén','person',2,'亻',9,2),
	 ('儿','儿','ér','legs',2,NULL,10,2);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('入','入','rù','enter',2,NULL,11,2),
	 ('八','八','bā','eight',2,'丷',12,2),
	 ('冂','冂','jiǒng','down box',2,NULL,13,2),
	 ('冖','冖','mì','cover',2,NULL,14,2),
	 ('冫','冫','bīng','ice',2,NULL,15,2),
	 ('几','几','jī, jǐ','table',2,NULL,16,2),
	 ('凵','凵','qǔ','open box',2,NULL,17,2),
	 ('刀','刀','dāo','knife',2,'刂',18,2),
	 ('力','力','lì','power',2,NULL,19,2),
	 ('勹','勹','bāo','wrap',2,NULL,20,2);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('匕','匕','bǐ','ladle',2,NULL,21,2),
	 ('匚','匚','fāng','right open box',2,NULL,22,2),
	 ('匸','匸','xǐ','hiding enclosure',2,NULL,23,2),
	 ('十','十','shí','ten',2,NULL,24,2),
	 ('卜','卜','bǔ','divination',2,NULL,25,2),
	 ('卩','卩','jié','seal',2,NULL,26,2),
	 ('厂','厂','hàn','cliff',2,NULL,27,2),
	 ('厶','厶','sī','private',2,NULL,28,2),
	 ('又','又','yòu','again',2,NULL,29,2),
	 ('口','口','kǒu','mouth',3,NULL,30,3);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('囗','囗','wéi','enclosure',3,NULL,31,3),
	 ('土','土','tǔ','earth',3,NULL,32,3),
	 ('士','士','shì','scholar',3,NULL,33,3),
	 ('夂','夂','zhī','go',3,NULL,34,3),
	 ('夊','夊','suī','go slowly',3,NULL,35,3),
	 ('夕','夕','xī','night',3,NULL,36,3),
	 ('大','大','dà','big',3,NULL,37,3),
	 ('女','女','nǚ','woman',3,NULL,38,3),
	 ('子','子','zǐ','child',3,NULL,39,3),
	 ('宀','宀','gài','roof',3,NULL,40,3);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('寸','寸','cùn','inch',3,NULL,41,3),
	 ('小','小','xiǎo','small',3,NULL,42,3),
	 ('尢','尢','yóu','lame',3,'尣',43,3),
	 ('尸','尸','shī','corpse',3,NULL,44,3),
	 ('屮','屮','chè','sprout',3,NULL,45,3),
	 ('山','山','shān','mountain',3,NULL,46,3),
	 ('川','川','chuān','river',3,'巛,巜',47,3),
	 ('工','工','gōng','work',3,NULL,48,3),
	 ('己','己','jǐ','oneself',3,NULL,49,3),
	 ('巾','巾','jīn','towel',3,NULL,50,3);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('干','干','gān','dry',3,NULL,51,3),
	 ('幺','幺','yāo','thread',3,NULL,52,3),
	 ('广','广','guǎng','shelter',3,NULL,53,3),
	 ('廴','廴','yǐn','stride',3,NULL,54,3),
	 ('廾','廾','gǒng','hands joined',3,NULL,55,3),
	 ('弋','弋','yì','shoot with a bow',3,NULL,56,3),
	 ('弓','弓','gōng','bow',3,NULL,57,3),
	 ('彐','彐','jì','snout',3,'彑',58,3),
	 ('彡','彡','shān','hair',3,NULL,59,3),
	 ('彳','彳','chì#xec;','step',3,NULL,60,3);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('心','心','xīn','heart',4,'忄',61,4),
	 ('戈','戈','gē','spear',4,NULL,62,4),
	 ('户','户','hù','door',4,NULL,63,4),
	 ('手','手','shǒu','hand',4,'扌',64,4),
	 ('支','支','zhī','branch',4,NULL,65,4),
	 ('攴','攴','pū','rap',4,'攵',66,4),
	 ('文','文','wén','script',4,NULL,67,4),
	 ('斗','斗','dǒu','dipper',4,NULL,68,4),
	 ('斤','斤','jīn','axe',4,NULL,69,4),
	 ('方','方','fāng','square',4,NULL,70,4);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('无','无','wú','not',4,NULL,71,4),
	 ('日','日','rì','sun',4,NULL,72,4),
	 ('曰','曰','yuē','say',4,NULL,73,4),
	 ('月','月','yuè','moon',4,NULL,74,4),
	 ('木','木','mù','tree',4,NULL,75,4),
	 ('欠','欠','qiàn','lack',4,NULL,76,4),
	 ('止','止','zhǐ','stop',4,NULL,77,4),
	 ('歹','歹','dǎi','death',4,NULL,78,4),
	 ('殳','殳','shū','weapon',4,NULL,79,4),
	 ('母','毋','mǔ','mother',4,'母',80,4);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('比','比','bǐ','compare',4,NULL,81,4),
	 ('毛','毛','máo','fur',4,NULL,82,4),
	 ('氏','氏','shì','clan',4,NULL,83,4),
	 ('气','气','qì','steam',4,NULL,84,4),
	 ('水','水','shuǐ','water',4,'氵',85,4),
	 ('火','火','huǒ','fire',4,'灬',86,4),
	 ('爪','爪','zhǎo','claw',4,'爫',87,4),
	 ('父','父','fù','father',4,NULL,88,4),
	 ('爻','爻','yáo','lines on a trigram',4,NULL,89,4),
	 ('爿','爿','qiáng','half of a tree trunk',4,NULL,90,4);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('片','片','piàn','slice',4,NULL,91,4),
	 ('牙','牙','yá','tooth',4,NULL,92,4),
	 ('牛','牛','niú','cow',4,'牜',93,4),
	 ('犭','犬','quǎn','dog',4,'犭',94,3),
	 ('玄','玄','xuán','profound',5,NULL,95,5),
	 ('玉','玉','yù','jade',5,'王',96,5),
	 ('瓜','瓜','guā','melon',5,NULL,97,5),
	 ('瓦','瓦','wǎ','tile',5,NULL,98,5),
	 ('甘','甘','gān','sweet',5,NULL,99,5),
	 ('生','生','shēng','life',5,NULL,100,5);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('用','用','yòng','use',5,NULL,101,5),
	 ('田','田','tián','field',5,NULL,102,5),
	 ('疋','疋','pǐ','cloth',5,NULL,103,5),
	 ('疒','疒','bìng','ill',5,NULL,104,5),
	 ('癶','癶','bō','foot steps',5,NULL,105,5),
	 ('白','白','bái','white',5,NULL,106,5),
	 ('皮','皮','pí','skin',5,NULL,107,5),
	 ('皿','皿','mǐn','dish',5,NULL,108,5),
	 ('目','目','mù','eye',5,NULL,109,5),
	 ('矛','矛','máo','spear',5,NULL,110,5);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('矢','矢','shǐ','arrow',5,NULL,111,5),
	 ('石','石','shí','stone',5,NULL,112,5),
	 ('示','示','shì','spirit',5,'礻',113,5),
	 ('禸','禸','róu','track',4,NULL,114,4),
	 ('禾','禾','hé','grain',5,NULL,115,5),
	 ('穴','穴','xuè','cave',5,NULL,116,5),
	 ('立','立','lì','stand',5,NULL,117,5),
	 ('竹','竹','zhú','bamboo',6,NULL,118,6),
	 ('米','米','mǐ','rice',6,NULL,119,6),
	 ('纟','糸','sī','silk',6,NULL,120,3);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('缶','缶','fǒu','jar',6,NULL,121,6),
	 ('网','网','wǎng','net',6,'罒',122,6),
	 ('羊','羊','yáng','sheep',6,NULL,123,6),
	 ('羽','羽','yǔ','feather',6,NULL,124,6),
	 ('老','老','lǎo','old',6,NULL,125,6),
	 ('而','而','ér','and',6,NULL,126,6),
	 ('耒','耒','lěi','plow',6,NULL,127,6),
	 ('耳','耳','ěr','ear',6,NULL,128,6),
	 ('聿','聿','yù','brush',6,NULL,129,6),
	 ('肉','肉','ròu','meat',6,NULL,130,6);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('臣','臣','chén','minister',6,NULL,131,6),
	 ('自','自','zì','oneself',6,NULL,132,6),
	 ('至','至','zhì','arrive',6,NULL,133,6),
	 ('臼','臼','jiù','mortar',6,NULL,134,6),
	 ('舌','舌','shé','tongue',6,NULL,135,6),
	 ('舛','舛','chuǎn','contrary',6,NULL,136,6),
	 ('舟','舟','zhōu','boat',6,NULL,137,6),
	 ('艮','艮','gèn','mountain',6,NULL,138,6),
	 ('色','色','sè','color',6,NULL,139,6),
	 ('艹','艸','cǎo','grass',6,NULL,140,3);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('虍','虍','hǔ','tiger',6,NULL,141,6),
	 ('虫','虫','chóng','insect',6,NULL,142,6),
	 ('血','血','xuě','blood',6,NULL,143,6),
	 ('行','行','xíng','walk',6,NULL,144,6),
	 ('衣','衣','yī','clothes',6,'衤',145,6),
	 ('西','西','xī','west',6,'覀',146,6),
	 ('见','見','jiàn','see',7,NULL,147,4),
	 ('角','角','jiǎo','horn',7,NULL,148,7),
	 ('讠','言','yán','speech',7,NULL,149,2),
	 ('谷','谷','gǔ','valley',7,NULL,150,7);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('豆','豆','dòu','bean',7,NULL,151,7),
	 ('豕','豕','shǐ','pig',7,NULL,152,7),
	 ('豸','豸','zhì','badger',7,NULL,153,7),
	 ('贝','貝','bèi','shell',4,NULL,154,4),
	 ('赤','赤','chì','red',7,NULL,155,7),
	 ('走','走','zǒu','walk',7,NULL,156,7),
	 ('足','足','zú','foot',7,NULL,157,7),
	 ('身','身','shēn','body',7,NULL,158,7),
	 ('车','車','chē','cart',7,NULL,159,4),
	 ('辛','辛','xīn','bitter',7,NULL,160,7);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('辰','辰','chén','morning',7,NULL,161,7),
	 ('辶','辶','chuò','walk',3,NULL,162,3),
	 ('邑','邑','yì','city',7,'阝',163,7),
	 ('酉','酉','yǒu','wine',7,NULL,164,7),
	 ('釆','釆','biàn','distinguish',7,NULL,165,7),
	 ('里','里','lǐ','village',7,NULL,166,7),
	 ('钅','金','jīn','metal',8,NULL,167,5),
	 ('长','長','cháng','long',8,NULL,168,4),
	 ('门','門','mén','gate',8,NULL,169,3),
	 ('阜','阜','fù','mound',8,'阝',170,8);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('隶','隶','lì','slave',8,NULL,171,8),
	 ('隹','隹','zhuī','short-tailed bird',8,NULL,172,8),
	 ('雨','雨','yǔ','rain',8,NULL,173,8),
	 ('青','青','qīng','blue',8,NULL,174,8),
	 ('非','非','fēi','wrong',8,NULL,175,8),
	 ('面','面','miàn','face',9,NULL,176,9),
	 ('革','革','gé','leather',9,NULL,177,9),
	 ('韦','韋','wěi','soft leather',9,NULL,178,4),
	 ('韭','韭','jiǔ','leek',9,NULL,179,9),
	 ('音','音','yīn','sound',9,NULL,180,9);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('页','頁','yè','page',9,NULL,181,6),
	 ('风','風','fēng','wind',9,NULL,182,4),
	 ('飞','飛','fēi','fly',9,NULL,183,4),
	 ('饣','食','shí','eat',9,'飠',184,3),
	 ('首','首','shǒu','head',9,NULL,185,9),
	 ('香','香','xiāng','fragrant',9,NULL,186,9),
	 ('马','馬','mǎ','horse',10,NULL,187,3),
	 ('骨','骨','gǔ','bone',9,NULL,188,9),
	 ('高','高','gāo','high',10,NULL,189,10),
	 ('髟','髟','biāo','long hair',10,NULL,190,10);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('鬥','鬥','dòu','fight',10,NULL,191,10),
	 ('鬯','鬯','chàng','sacrificial wine',10,NULL,192,10),
	 ('鬲','鬲','lì','cauldron',10,NULL,193,10),
	 ('鬼','鬼','guǐ','ghost',9,NULL,194,9),
	 ('鱼','魚','yú','fish',11,NULL,195,8),
	 ('鸟','鳥','niǎo','bird',11,NULL,196,5),
	 ('卤','鹵','lǔ','salty',11,NULL,197,7),
	 ('鹿','鹿','lù','deer',11,NULL,198,11),
	 ('麦','麥','mài','wheat',11,NULL,199,7),
	 ('麻','麻','má','hemp',11,NULL,200,11);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('黄','黄','huáng','yellow',11,NULL,201,11),
	 ('黍','黍','shǔ','millet',12,NULL,202,12),
	 ('黑','黑','hēi','black',12,NULL,203,12),
	 ('黹','黹','zhǐ','embroidery',12,NULL,204,12),
	 ('黾','黽','mǐn','frog',12,NULL,205,8),
	 ('鼎','鼎','dǐng','tripod',12,NULL,206,12),
	 ('鼓','鼓','gǔ','drum',13,NULL,207,13),
	 ('鼠','鼠','shǔ','rat',13,NULL,208,13),
	 ('鼻','鼻','bí','nose',14,NULL,209,14),
	 ('齐','齊','qí','even',14,NULL,210,6);
INSERT INTO public.radicals (simplified,traditional,pinyin,english,strokes_traditional,variants,kangxi,strokes_simplified) VALUES
	 ('齿','齒','chǐ','tooth',15,NULL,211,8),
	 ('龙','龍','lóng','dragon',16,NULL,212,5),
	 ('龟','龜','guī','turtle',16,NULL,213,7),
	 ('龠','龠','yuè','flute',17,NULL,214,17);