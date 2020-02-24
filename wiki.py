import wikipedia as wp
import warnings
import json

warnings.filterwarnings("ignore")
def codesworth_wikipedia(term):
    try:
        text = wp.summary(term, sentences = 2)
        url = wp.page(term).url
        title = wp.page(term).title
        img = wp.page(term).images[0]
        return(0, title, text, url, img)
    except wp.exceptions.DisambiguationError as e:
        err = "{}".format(e).split('\n')
        if len(err)>6:
            err = '\n'.join(err[:6])+'...'
        else:
            err = '\n'.join(err)
        return(1, err,"\nPlease search again.")

