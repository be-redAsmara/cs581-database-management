from urllib.request import urlopen
from random import randint
import json
import csv
import random

def preprocess():
    slat = "40.6413"
    slong = "-73.7781"
    tuple_record = []
    professionals = {1:['Student','Professor'],2:['Driver'],3:['Engineer'],4:['Doctor','Nurse'],5:['Social Worker'],
                   6:['Cop','Lawyer','Journalist'],7:['Stylist','Model'],8:['Artist'],9:['Chef'],10:['Banker']}
    with open('final_input_data.csv', "rt", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            passengercount = row[3].strip()
            dlat = row[8].strip()
            dlong = row[7].strip()
            url = "http://localhost:5000/route/v1/driving/" + slong + "," + slat + ";"
            url += dlong + "," + dlat
            response = urlopen(url)
            decoded = response.read().decode('utf-8')
            json_obj = json.loads(decoded)
            trip_distance = json_obj['routes'][0]['distance'] * float(0.000621371)
            trip_duration = json_obj['routes'][0]['duration'] / float(60)
            willing_to_walk = randint(0, 1)
            if(willing_to_walk):
                wthreshold = min(0.2*trip_distance,0.2)
            else:
                wthreshold = 0
            dthreshold = 0.15 * trip_duration
            professions = []
            for i in range(int(passengercount)):
                professions += random.sample(professionals.keys(),1)
            profession = "-".join(str(x) for x in professions)
            tuple_record.append([row[0].strip(),row[1].strip(),row[2].strip(),passengercount,slong,slat,dlong,dlat,row[4].strip(),trip_distance,trip_duration,dthreshold,willing_to_walk,wthreshold,profession])

    with open('dump_data.csv','w') as out:
        csv_out = csv.writer(out)
        for row in tuple_record:
            csv_out.writerow(row)

preprocess()
