import json
from datetime import datetime

rental_price = {
	"rentals" : []
}

def getDays(sDate, eDate):
	return (datetime.strptime(eDate, "%Y-%m-%d") - datetime.strptime(sDate, "%Y-%m-%d")).days+1

with open("./data/input.json",'r') as file:
	jsonTxt = file.read()
	data = json.loads(jsonTxt)
	for row in range(len(data["rentals"])):
		days = getDays(data["rentals"][row]["start_date"], data["rentals"][row]["end_date"])
		distance = int(data["rentals"][row]["distance"])
		if (days < 0) or (distance < 0):
			exit()
		car_id = data["rentals"][row]["car_id"] - 1
		ppDay = int(data["cars"][car_id]["price_per_day"])
		ppDistance = int(data["cars"][car_id]["price_per_km"])

		rental_price["rentals"].append({"id":(data["rentals"][row]["id"]), "price":int(days*ppDay + distance*ppDistance)})


with open("./data/output.json", "w") as oFile:
	json.dump(rental_price,oFile,indent=2)
