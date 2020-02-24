import requests, json 

def codesworth_currency(amt, frm, to):
    api_key = "95e87a3b0d43c8950ed6"
    base_url = "https://free.currconv.com" 
    complete_url = base_url + "/api/v7/convert?q=" + frm.upper() + "_" + to.upper() + "&compact=ultra&apiKey=" + api_key

    try:
        response = requests.get(complete_url) 
        x = response.json()
        calc = "{0:.{1}f}".format(amt * float(x["{}_{}".format(frm.upper(), to.upper())]), 2)
        amt = "{0:.{1}f}".format(amt, 2)
        return ("{} {} amounts to {} {}.".format(amt, frm.upper(), calc, to.upper()))
    except:
        return("An error occured, please try again.")

