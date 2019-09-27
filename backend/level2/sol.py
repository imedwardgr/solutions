import json
from datetime import datetime

rental_price = {
	"rentals" : []
}

def getDays(sDate, eDate):
	return (datetime.strptime(eDate, "%Y-%m-%d") - datetime.strptime(sDate, "%Y-%m-%d")).days+1

def getDaysPrice(days, ppDay):
	daysPrice = 0
	daysPrice += ppDay
	days -= 1

	if days <= 3:
		daysPrice += days*ppDay*0.9
	else:
		daysPrice += 3*ppDay*0.9
		days -= 3
		if days <= 5:
			daysPrice += days*ppDay*0.7
		else:
			daysPrice += 6*ppDay*0.7
			days -= 6
			daysPrice += days*ppDay*0.5
	return daysPrice

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

		rental_price["rentals"].append({"id":(data["rentals"][row]["id"]), "price": int(getDaysPrice(days,ppDay) + distance*ppDistance)})

with open("./data/output.json", "w") as oFile:
	json.dump(rental_price,oFile,indent=2)
