import requests     # for making GET requests to kiwy tequila API
import pandas as pd # for reading and processing short.csv   (CSV) means comma separated values 
import json         # for saving result as a JSON file
import sys          # for reading arguments from command line


FLIGHT_MASTER_API_KEY = ""  # API key to make requests (stored in the header of https request)
FLIGHT_MASTER_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"  # URL for tequila


iata_db = pd.read_csv('short.csv')  # creating dataframe from csv file

# initializing parameters with arguments received from command line
default_list = ["Samarkand", "___", "", ""]   # taking default cities  (Easter egg)
try:
    for index, value in enumerate(sys.argv[1:]):
        default_list[index] = value
except:
    pass
from_, to_, fromdate, todate = default_list

try:  # trying to find the math with cities 
    try:
        row = iata_db.loc[iata_db['city'] == from_]   #specific row from dataframe
        fromiata = row['code'].to_list()[0]           # assign IATA code of the city
        fromairport = row['name'].to_list()[0]        # assigning airport name in the city
    except:                                           # in case if there are no matches with cities we select matches with names of airports
        row = iata_db.loc[iata_db['name'].str.contains(from_, case=False)]
        fromiata = row['code'].to_list()[0]
        fromairport = row['name'].to_list()[0]
except:   #default assignation will not go further 
    fromiata = "___"
    fromairport = ''

try:
    try:
        row = iata_db.loc[iata_db['city'] == to_]
        toiata = row['code'].to_list()[0]
        toairport = row['name'].to_list()[0]
    except:
        row = iata_db.loc[iata_db['name'].str.contains(to_, case=False)]
        toiata = row['code'].to_list()[0]
        toairport = row['name'].to_list()[0]

except:   #default assignation will not go further 
    toiata = ""
    toairport = ''


print(fromiata, toiata)


params = {"fly_from": fromiata,   #parameters of request   (will be in the body of https)
    "fly_to": f"{toiata}",
    "date_from": f"{fromdate}",
    "date_to": f"{todate}",
    }
headers = {                       #header of the request    (hidden )
    "apikey":FLIGHT_MASTER_API_KEY,
    }

response = requests.get(FLIGHT_MASTER_ENDPOINT, params = params,headers=headers)    #response from the API
try:
    response.raise_for_status()                 # raises an error with corresponding response 200-success 400-fail 300-forbidden
    data = response.json()["data"]
    response = response.json()
except:
    response = {'data':[]}      #default in case no options are found 

#respone --> dict   
#data  --> list
#data[i] --> dict

result = {                     #initializing final result 
        'options_available': 0,
        'options': []
}

for variant in response['data']:   #reading response
    temp = {}                      #creation and feeling temp dict with neccessary data
    temp['fromAirport'] = f'{variant["cityFrom"]} ** {fromairport} IATA: {variant["flyFrom"]}'
    temp['toAirport'] = f'{variant["cityTo"]} ** {toairport} IATA: {variant["flyTo"]}'

    departure = variant['utc_departure'].split('.')[0]   # converting time to convenient from
    ddate, dtime = departure.split('T')

    arrival = variant['utc_arrival'].split('.')[0]
    adate, atime = arrival.split('T')

    temp['departureDate'] = ddate
    temp['departureTime'] = dtime
    temp['arrivalDate'] = adate
    temp['arrivalTime'] = atime
    temp['price'] = variant['price']
    temp['id'] = variant['id']
    temp['token'] = variant['booking_token']
    

    result['options'].append(temp)                 # adding it to the resulting dict

result['options_available'] = len(response['data'])    #counting the number of options 
print(len(response['data']))

with open('response.json', 'w') as file:         # dumping result to response.json
    json.dump(result, file, indent=4)
with open('full_response.json', 'w') as file:    # dumping unfiltered full response
    json.dump(response, file, indent=4)