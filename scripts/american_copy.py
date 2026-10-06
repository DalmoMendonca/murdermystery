"""American spelling for current exports, including unchanged historical precursors."""
import re
WORDS={'colour':'color','colours':'colors','catalogue':'catalog','catalogues':'catalogs','programme':'program','programmes':'programs','theatre':'theater','centre':'center','centres':'centers','neighbourhood':'neighborhood','neighbours':'neighbors','cancelled':'canceled','labelled':'labeled','favourite':'favorite','favour':'favor','organise':'organize','organised':'organized','realise':'realize','realised':'realized','recognise':'recognize','recognised':'recognized','behaviour':'behavior','travelling':'traveling','travelled':'traveled','grey':'gray','licence':'license','defence':'defense'}
WORDS.update({'neighbour':'neighbor','cheque':'check','cheques':'checks','moustache':'mustache','moustaches':'mustaches','recognising':'recognizing','organising':'organizing','realising':'realizing','favourites':'favorites','coloured':'colored','colourful':'colorful','jewellery':'jewelry','humour':'humor','honour':'honor','labour':'labor'})
PATTERN=re.compile(r'\b('+'|'.join(WORDS)+r')\b',re.I)
def american(text):
    def replace(m):
        source=m[0];word=WORDS[source.lower()]
        return word.upper() if source.isupper() else word.capitalize() if source[0].isupper() else word
    return PATTERN.sub(replace,text)
