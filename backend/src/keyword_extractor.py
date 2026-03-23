from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



#used to return the string as it will store in db and sqlite doesn't support list
# #, we can convert it back to list when we retrieve it for retrieval augmentation and all this in the same order otherwise the output is not as it is required 
def extract_keywords(chunk_text:str, ) -> str:                  
    word_token = word_tokenize(chunk_text)                         # performing tokenization
    pos_tags = pos_tag(word_token)                              # performing POS tagging, for noun, verb
   #filtering the words based on POS tags, we can further filter it by only keeping nouns and verbs, as they are more likely to be relevant for retrieval augmentation
    filtered_words = [word for word, tag in pos_tags if tag.startswith(('NN', 'VB'))]
    #performing lemmatization,calling the instance of a class using import as its class 
    lemmitizer = WordNetLemmatizer()
    lemmitized_words = [lemmitizer.lemmatize(word)for word in filtered_words]
    #using stopwords to remove common english words 
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in lemmitized_words if word not in stop_words]
    # don't use space as the separator as it is fragile and can break if the spacing is inconsistent while again converting into list 
    return ','.join(keywords)
