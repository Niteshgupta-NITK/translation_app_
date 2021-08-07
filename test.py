import translators as ts
from textblob import TextBlob
# ts = Translator(to_lang="eng")

def tb(strg):
  lang = TextBlob(strg)
  detected_lang=lang.detect_language()
  return detected_lang

with open('./untranslated/bengali_test1.txt', encoding='utf-8') as file:
	text = file.read()
	language = tb(text)
	with open('./translated/translated.txt', 'w', encoding='utf-8') as new_file:
		new_file.write(ts.google(text, from_language = language, to_language='en'))