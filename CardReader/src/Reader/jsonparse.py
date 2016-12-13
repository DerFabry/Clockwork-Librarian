import json
from pprint import pprint
import webbrowser

with open('MTGJson/AllSets.json') as data_file:
    data = json.load(data_file)

SetName = 'SOI'
CardName = 'Triskaidekaphobia'
resultCardData = None
print('is ' + SetName + ' in file?')
isSetExisting = SetName in data
print(isSetExisting)
if(isSetExisting):
    dataResultSet = data[SetName]
    allCardDataInResultSet = dataResultSet['cards']
    for card in allCardDataInResultSet:
        if card['name'] == CardName:
            resultCardData = card
    MVID = resultCardData['multiverseid']
    imageURL = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(MVID)+'&type=card'

    webbrowser.open(imageURL)
else:
    print('Data not found')

