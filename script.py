import csv
import math
#import pyproj

######################################################################################
# Problem:
# -Given a list of potential antenna locations and a list of potential customers,
#  select the minimum number of antennas to cover all customers.
# -Each antenna has a range, throughput, and cost.
# -Each customer has a location.
# Solution: 
# -Prioritizing Coverage minimizing costs
# -least number of antennas
# -highest throughput
# -lowest cost
#######################################################################################

# Load CSV file into a list of lists
def load_csv(filename):
    with open(filename, 'r') as file: 
        reader = csv.reader(file)
        next(reader)
        return list(reader)
    
#Using Haversine formula to calculate distance between two points on a sphere (planet earth)
#https://en.wikipedia.org/wiki/Haversine_formula
def distance(lat1, lon1, lat2, lon2):
    R = 20925524.9
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
    a = (math.sin(dlat/2) * math.sin(dlat/2) +
         math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) *
         math.sin(dlon/2) * math.sin(dlon/2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c #feet 

#Load CSV files
customers = load_csv('potentialCustomers.xlsx - house.csv')
antennas = load_csv('possibleAntennaLocations.xlsx - street.csv')

#Dictionary of antenna types
antenna_types = {
    'T-1': {'range':100, 'throughput': 500, 'cost': 1000},
    'T-2': {'range':200, 'throughput': 400, 'cost': 2000},
    'T-3': {'range':300, 'throughput': 300, 'cost': 3000},
    'T-4': {'range':400, 'throughput': 200, 'cost': 4000},
    'T-5': {'range':500, 'throughput': 100, 'cost': 5000},
}

#############################################################################################
#Step 1: Prioritize Throughput
    # Algorithm:
    # 1. Find Antennas with ranges for range for each customer
    # 2. Prioritize based on throughput
    # 3. Append to customer coverage dictionary
def prioritize_throughput():
    customer_coverage = {} # Dictionary for results = key: customer location, value: (antena, antenna_type)
    for customer in customers: #Iterate through each customer
        best_throughput = 0; 
        best_antenna = None; 
        best_antenna_type = None;
        for antenna in antennas: #Iterate through antennas
            for antena_type, details in antenna_types.items(): #Iterate through all antenna types
                if(distance(customer[2], customer[3], antenna[2], antenna[3]) <= details['range']): #Check if antenna is within range
                    if(details['throughput'] > best_throughput):
                        best_throughput = details['throughput']
                        best_antenna = antenna[0]
                        best_antenna_type = antena_type
        if(best_antenna):
            customer_coverage[(customer[0])] = (best_antenna, best_antenna_type)
        else:
            print("No antenna found for customer: ", customer)
    return customer_coverage

    

###################################################################################################
#Step 2: Cost Minimization 
    # Algorithm:
    # get total cost
    # get total throughput
    # get total number of antennas

def total_cost():
    customer_coverage = prioritize_throughput()
    total_cost = 0;
    for customer, antenna in customer_coverage.items():
        total_cost += antenna_types[antenna[1]]['cost']
    return total_cost

def minimize_cost():
    customer_coverage = prioritize_throughput()
    
####################################################################################################

with open ('solution.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for customer, (antenna, antenna_type) in prioritize_throughput().items():
        writer.writerow([antenna, antenna_type])
