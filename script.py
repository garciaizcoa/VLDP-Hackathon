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

 #Set of selected antennas (no duplicates)

###################################################################################################
#Step 2: Cost Minimization 
    # Algorithm:
    # get total cost
    # get total throughput
    # get total number of antennas

def total_cost(customer_coverage, antenna_types):
    #extract antenna types from customer coverage
    antenna_types_selected = [antenna_type for _, antenna_type in customer_coverage]
    #get total cost
    cost = sum(antenna_types[antenna_type]['cost'] for antenna_type in antenna_types_selected)
    return cost

def minimize_cost():
    customer_coverage = prioritize_throughput()

selected_antennas = set(prioritize_throughput().values()) #set of selected antennas (no duplicates) 

####################################################################################################
#Step 3: Output Testing

#check if customer is within range of antenna
def is_within_range(customer, antenna, antenna_type_details):
    return distance(float(customer[2]), float(customer[3]), float(antenna[2]), float(antenna[3])) <= antenna_type_details['range']

#check if all customers have coverage
def all_customers_have_coverage(customers, antennas, customer_coverage, antenna_types):
    for customer in customers:
        has_coverage = False

        #check all antennas
        for antenna_code, antenna_type in customer_coverage:
            antenna_details = next(a for a in antennas if a[0] == antenna_code) #get antenna details
            if is_within_range(customer, antenna_details, antenna_types[antenna_type]): #check if customer is within range of antenna
                has_coverage = True
                break
        if not has_coverage:
            print(f"Customer {customer[0]} does not have coverage")
            return False
    return True

# #PRINT TESTS W/O MINIMIZING COST
#---------------------------------------------------------------------
# #print total number of antennas
# print(f"Total number of antennas: {len(prioritize_throughput())}")

# # -Print total cost for an antenna for each customer
# total_cost_value = total_cost(prioritize_throughput().values(), antenna_types)
# print(f"Total Cost for an Antenna for each customer: ${total_cost_value}")

# #Coverage Status
# coverage_status = all_customers_have_coverage(customers, antennas, prioritize_throughput().values(), antenna_types)

# if coverage_status:
#     print("All customers have coverage")
# else:
#     print("Not all customers have coverage")
#-----------------------------------------------------------------------
# PRINT TESTS W/ MINIMIZING COST
#
# -Print total number of antennas
print(f"Total number of antennas: {len(selected_antennas)}")

# -Print total cost for an antenna for unique antennas only
total_cost_value = total_cost(selected_antennas, antenna_types)
print(f"Total Cost having unique antennas only: ${total_cost_value}")

#Coverage Status
coverage_status = all_customers_have_coverage(customers, antennas, selected_antennas, antenna_types)

print("All customers have coverage: ", coverage_status) 


########################################################################################################
#Step 4: Output to CSV
with open ('solution.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for (antenna_code, antenna_type) in selected_antennas:
        writer.writerow([antenna_code, antenna_type])
    
