import json
from datetime import datetime

#Code made by Eduardo Gómez Rodríguez, mail: egomezr1300@alumno.ipn.mx
#Complexity:
#	n = number of cars
#	m = number of rentals
#	p = number of options
#Time complexity, because of the fact the sets and maps are hashed elements, it should be O(n+m+p)
#Memory complexity, because of the creation of rental_price obj, all the attributes are saved,
#Taking |n| as the sum of the size of the elements inside cars the memory complexity is O(|n|+|m|+|p|)

rental_price = { #This is out object to be dumped as the json
	"rentals" : []
}

optionsMap = {} #This is a map that will cotain a set of strings with the options of each rental
cars = {} #We save the existing cars to then verify if they exists

def getDays(sDate, eDate):  #This uses the datetime obj of python to calculate only the days of difference
	return (datetime.strptime(eDate, "%Y-%m-%d") - datetime.strptime(sDate, "%Y-%m-%d")).days+1

def getDaysPrice(days, ppDay): #This fuctions return only the total price of the days with the discounts
	daysPrice = 0
	daysPrice += ppDay #At least it should have one day of it would not be possible to be rented
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

def getActions(days, totalPrice, rentalId):  #Here is constructed the actions array (debit/credit and who)
	us = int(totalPrice*0.3) #Firstly is calculated the comissions
	insurance = int(us*0.5)
	assistance = int(days*100)
	us -= (insurance+assistance)
	owner = int(totalPrice-us-insurance-assistance)

	#Then, is added the aditional money for the selected option
	if rentalId in optionsMap: #Firstly is checked if the current rental choosed options for their trip
		for option in optionsMap[rentalId]: #If there are options, we iterate over them
			if option == "gps": #It's guaranteed that two Ifs cannot be accessed on the same iteration
				totalPrice += 500*days
				owner += 500*days
			if option == "baby_seat":
				totalPrice += 200*days
				owner += 200*days
			if option == "additional_insurance":
				totalPrice += 1000*days
				us += 1000*days

	actions = [] #Once that all the commissions were distributed, its created the array with the actions
	actions.append({"who": "driver","type": "debit","amount": int(totalPrice)})
	actions.append({"who": "owner","type": "credit","amount": owner})
	actions.append({"who": "insurance","type": "credit","amount": insurance})
	actions.append({"who": "assistance","type": "credit","amount": assistance})
	actions.append({"who": "drivy","type": "credit","amount": us})

	return actions

def getOptions(rentalId): #Here is constructed out array of selected options for rental
	options = []

	if rentalId in optionsMap: #If for this rental, they choosed an option, we add the option to an array
		for option in optionsMap[rentalId]:
			options.append(option)

	return options

with open("./data/input.json",'r') as file:
	jsonTxt = file.read()
	data = json.loads(jsonTxt) #Firsly is loaded the input json file

	for row in range(len(data["cars"])):
		cars[int(data["cars"][row]["id"])] = {}

	for row in range(len(data["options"])): #Then we check the options in order to link them with their rental
		try:#If the set exists, we insert the new value
			optionsMap[data["options"][row]["rental_id"]].add(data["options"][row]["type"])
		except KeyError: #If the set doesn't exists, we create it 
			optionsMap[data["options"][row]["rental_id"]] = {data["options"][row]["type"]}

	for row in range(len(data["rentals"])): #Now we had to iterate over the rentals
		#Firsly the data on the json file, is loaded into separated variables in order to make them clearer to read
		days = getDays(data["rentals"][row]["start_date"], data["rentals"][row]["end_date"])
		distance = int(data["rentals"][row]["distance"])
		car_id = data["rentals"][row]["car_id"] - 1
		ppDay = int(data["cars"][car_id]["price_per_day"])
		ppDistance = int(data["cars"][car_id]["price_per_km"])
		rentalId = data["rentals"][row]["id"]

		#Here we make some validations, it's supposed that they shouldn't have inconsistent data
		#But I decided to make them in order to show that I considered the edge cases
		if (days < 0) or (distance < 0) or (ppDay < 0) or (ppDistance < 0): #If any value is negative, we stop
			print("on " + str(rentalId) + " rental, exists inconsistent data, please verify your input file")
			continue
		if not ((car_id+1) in cars):
			print("car with id=" + str(car_id+1) + " does not exists, please verify your input file")
			continue 

		#Now that the data is loaded and the all the verifications are passed, its time to calcule the anwers
		totalPrice = getDaysPrice(days, ppDay) + distance*ppDistance
		rental_price["rentals"].append({"id":rentalId, "options":getOptions(rentalId) ,"actions":getActions(days, totalPrice, rentalId)})

with open("./data/output.json", "w") as oFile:
	json.dump(rental_price,oFile,indent=2) #And now we already constructed our anwer object, we dump it
	#With indent equals 2 in order to match with the expected output
