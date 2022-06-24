import json
import csv
from flask import Flask, render_template, request
import requests



#dane importowane z pliku
'''
with open("Module9/data_waluty.json", "r") as f:
    data = json.load(f)
list_ind0 = data[0]
list_of_dict = list_ind0["rates"]
'''

#dane importowane z sieci
response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data= response.json()
list_ind0 = data[0]
list_of_dict = list_ind0["rates"]

        
def write_to_csv():
    with open("Module9/data_waluty.csv", "w", newline='') as f:
        fieldnames = list_of_dict[0].keys()
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()
        for i in list_of_dict:
            writer.writerow(i)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def website():
    koszt = 0
    if request.method == 'POST':
        for i in list_of_dict:
            if i.get("code") == request.form["currency"]:
                koszt_uncut = float(i['ask']) * float(request.form["quantity"])
                koszt = "{:.2f}".format(koszt_uncut)
                
    return render_template("waluty.html", koszt=koszt)


if __name__ == "__main__":
    app.run(debug=True)


        


