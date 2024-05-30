import csv

# Example list of lists
data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Open the CSV file for writing
with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write all rows (inner lists) to the CSV file
    writer.writerows(data)