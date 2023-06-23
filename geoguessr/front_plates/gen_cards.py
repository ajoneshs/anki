import csv
from data.state_abbrev import abbrev

data = open('data/data.txt', 'r').read().splitlines()

both = data[1].split(', ')
rear_only = data[3].split(', ')
most_both = data[5].split(', ')

master = []


# tag format: Geo::Country::US::State/territory Geo::Front_Plates
def add_to_master(state_list, req):
    for state in state_list:
        tags = f"Geo::Country::US::{abbrev[state]} Geo::Front_Plates::{req.replace(' ', '_')}"
        master.append([state, req, tags])


add_to_master(both, 'yes')
add_to_master(rear_only, 'no')
add_to_master(most_both, 'mostly')

with open('data/front_plates_cards.csv', 'w', newline='') as f:
    writer = csv.writer(f)

    field = ["location", "requirements", "tag"]
    #writer.writerow(field)
    
    for i in master:
        writer.writerow(i)