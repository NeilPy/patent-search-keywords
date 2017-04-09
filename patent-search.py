import random, pprint, requests, bs4
from pattern.search import Pattern, STRICT, search
from pattern.en import parsetree, wordnet

def re_search(text, search_string, strict=False):
    tree = parsetree(text, lemmata=True)
    if strict:
        results = search(search_string, tree, STRICT)
    else:
        results = search(search_string, tree)
    return results

def search_out(text, search_string, strict=False):
    results = re_search(text, search_string)
    output = []
    for match in results:
        sent = []
        for word in match:
            sent.append(word.string)
        output.append(" ".join(sent))
    return output

URL_set = ['https://patents.google.com/patent/US6816241B2/en', 
'https://patents.google.com/patent/US6224216B1/en', 
'https://patents.google.com/patent/US7759881B1/en',  
]

for num in range(0, len(URL_set)):
#patURL = 'https://patents.google.com/patent/US6816241B2/en'

    patURL = URL_set[num]

    res = requests.get(patURL)

    res.raise_for_status()

    noStarchSoup = bs4.BeautifulSoup(res.text, "lxml")

    type(noStarchSoup)

    elems = noStarchSoup.select('div > abstract')
    Abstract = elems[0].getText()

    elems2 = noStarchSoup.select('h1')
    title = elems2[0].getText()
   # print parsetree(Abstract, lemmata=False)
   # print parsetree(title, lemmata=False)
#print title
    search_patterns2 = [
                'DT|NP|NN NP|JJ|NN NN|NP|JJ NN|NP', 'JJ NN|NP', 'NNP NP NP']
       


    noun_phrases = search_out(Abstract, search_patterns2[0])

    for num in range(1, len(search_patterns2)):
        noun_phrases += search_out(Abstract, search_patterns2[num])

    noun_phrases_title = search_out(title, search_patterns2[0])

    for num in range(1, len(search_patterns2)):
        noun_phrases_title += search_out(title, search_patterns2[num])

    pprint.pprint (set(noun_phrases_title))

    pprint.pprint (set(noun_phrases).union(noun_phrases_title))

  #  pprint.pprint (set(noun_phrases).intersection(noun_phrases_title))
