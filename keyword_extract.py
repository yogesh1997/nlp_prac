import nltk
import gensim
import spacy
import rake_nltk
import yake
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import regexp_tokenize
from collections import Counter
from gensim.summarization import summarize
from gensim.summarization import keywords
from rake_nltk import Rake
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


porter_stemmer  = PorterStemmer()
lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")


def clean(text, remove_stopwords=True):
  text = text.lower()
  tokens = word_tokenize(text)
  stop_words = set(stopwords.words('english'))
  tokens = [w for w in tokens if not w in stop_words and len(w)>3]
  tokens = [lemmatizer.lemmatize(w) for w in tokens]
  processedtext = " ".join(tokens)
  sent = nlp(processedtext)
  tokens = []
  for token in sent:
    if not token.is_stop:
      tokens.append(token.lemma_)
  return " ".join(tokens)

sample_text = "A method for reading out an image sensor, the method includes the steps of integrating charge in a photodetector with the photodetector at a first capacitance; reading the resulting signal level at a first time with the photodetector at the first capacitance; changing the photodetector capacitance to a second capacitance; and reading the signal level associated with the photodetector at the second capacitance."
processed_sent = clean(sample_text)
#print(processed_sent)

def custom_stop_words(file_path):
  """loads custom defined stop words"""

  with open(file_path,'r',encoding='utf-8') as f:
    stopwords = f.readlines()
    stopwordset = set(m.strip() for m in stopwords)
    return frozenset(stopwordset)



defined_stopwords = custom_stop_words('texts/stopwords.txt')
cv = CountVectorizer(max_df=0.70,stop_words=defined_stopwords)
word_count_vector = cv.fit_transform(processed_sent)

#print(list(cv.vocabulary_.keys())[:10])

tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfidf_transformer.fit(word_count_vector)
#print(cv.get_feature_names())


df_test=pd.read_json("text/sample-test.json",lines=True)
df_test['text'] = df_test['title'] + df_test['description']
df_test['text'] =df_test['text'].apply(lambda x:clean(x))

doc_test=df_test['text'].tolist()

def extract_top(feature_names, items, top=5):
    """get the feature names and tf-idf score of top n items"""
    
    items = items[:top]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]
        
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])


    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results


feature_names=cv.get_feature_names()
doc=docs_test[0]
tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))
keywords=extract_topn_from_vector(feature_names,tf_idf_vector,10)

for word in keywords:
    print(word,keywords[word])




#Alternate way using spacy and (rake or yake) to extract keywords


#sent = nlp(processed_sent)
# for token in sent:
#   print(token,token.pos_,spacy.explain(token.dep_),spacy.explain(token.tag_))

# r = Rake()
# r.extract_keywords_from_text(text)
# phrases = r.get_ranked_phrases()

# kw_extractor = yake.KeywordExtractor()
# keywords = kw_extractor.extract_keywords(text)
# print(keywords)
