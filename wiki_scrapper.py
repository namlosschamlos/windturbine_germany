import requests as req
import pandas as pd
from bs4 import BeautifulSoup

bundeslaender = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen"
]

def createScrappingLink(bundesland):
    baseLink = "https://de.wikipedia.org/wiki/Liste_von_Windkraftanlagen_in_"
    scrappingLink = f"{baseLink}{bundesland}"
    return scrappingLink

def getResponseInDataFrame(url):
    response = req.get(url)
    if response.status_code == 200:
        content = response.content.decode("utf-8")
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table),header=0)[0]
        return df
        
def scrapperMain():
    dataFrames = []
    for bundesland in bundeslaender:
        print(bundesland)
        url = createScrappingLink(bundesland)
        dataFrames.append(getResponseInDataFrame(url))
    
    dataSet = pd.concat(dataFrames)
    dataSet.to_csv("wkaData.csv",encoding="utf-16",sep="\t",index=False)



def prepareCSVData():
    colNames = ["name","constyear","output","type","location","district","dmscoordinates","stakeholder","comment"]
    df = pd.read_csv("wkaData.csv",sep="\t", encoding="utf-16",header=0)
    print(df["Koordinaten"])

    df["latTemp"] = df["Koordinaten"].str.rsplit(",").str[0]
    print(df["lat"])

prepareCSVData()




