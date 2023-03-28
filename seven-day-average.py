import csv
import requests

def main():
	# Read NYTimes Covid Database
	download = requests.get(
		"https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
	)
	decoded_content = download.content.decode("utf-8")
	file = decoded_content.splitlines()
	reader = csv.DictReader(file)
	
	# Construct 14 day lists of new cases for each states
	new_cases = calculate(reader)

	# Create a list to store selected states
	states = []
	print("Choose one or more states to view average COVID cases.")
	print("Press enter when done.\n")

	while True:
		state = input("State: ")
		if state in new_cases:
			states.append(state)
		if len(state) == 0:
			break

	print(f"\nSeven-Day Averages")

	# Print out 7-day averages for this week vs last week
	comparative_averages(new_cases, states)



# Creates dictionary which stores 14 most recent days of new cases by state
def calculate(reader):
	# Create a dictionary of cases per date
	# Each day contains an array of cases
	# Each case stores the state's name and its number of cases
	cases_per_date = {}
	for row in reader:
		case = {}
		case["state"] = row["state"]
		case["cases"] = int(row["cases"])
		date = row["date"]
		if not(date in cases_per_date):
			cases_per_date[date] = []
			cases_per_date[date].append(case)
		else:
			cases_per_date[date].append(case)

	# Initialize dictionary of new cases
	# keys: [state name] -> [number of new cases]
	new_cases = {}

	# Initialize dictionary of previous cases
	# keys: [state name] -> [number of previous cases]
	# will use this to create new_cases dictionary
	prev_cases = {}

	# Iterate over the last 14 days data
	# and compute new_cases
	i = 1
	while i <= 14:
		today = list(cases_per_date)[-i]
		for case in cases_per_date[today]:
			state = case["state"]
			cases_count = case["cases"]
			if not(state in prev_cases):
				prev_cases[state] = cases_count
				new_cases[state] = 0
			else:
				new_cases[state] += prev_cases[state] - cases_count
				prev_cases[state] = cases_count
		i += 1
	
	return new_cases



# Calculates and prints out seven day average for given state
def comparative_averages(new_cases, states):
	# Iterate over states
	# For each state calculate its 7-day average
	# based on the last 14-days data
	for state in states:
		average = round(new_cases[state] / 14 * 7)
		print(f"{state} had a 7-day average of {average}")



# Run the program
main()
