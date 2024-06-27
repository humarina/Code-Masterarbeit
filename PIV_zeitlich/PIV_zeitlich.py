import os
import numpy as np

# Set input and output folders
input_folder = "Input"
output_folder = "Output"

# Get a list of all text files in the input folder
input_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]


# Function to calculate velocity magnitude g
def calculate_g(u, v, sign_u):
    return sign_u * np.sqrt(u ** 2 + v ** 2)


# Store results for each file
results = []

# Loop over all text files
for file_name in input_files:
    # Create the full path to the file
    file_path = os.path.join(input_folder, file_name)

    # Open the file and read lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Skip the first 3 lines of metadata
        data_lines = lines[3:]

        # Extract values for u (velocity in the x direction), v (velocity in the y direction), sign_u, typ, and g
        g_values = []
        for line in data_lines:
            values = line.split(',')
            u = float(values[2])  # velocity in the x direction
            v = float(values[3])  # velocity in the y direction
            sign_u = 1 if u > 0 else (-1 if u < 0 else 0)  # sign of velocity in the x direction
            typ = int(values[4])  # Typevector is 0 for masked vector, 1 for regular vector, 2 for filtered vector

            # Ignore lines where typ is not equal to 1 and u, v are not NaN
            if typ != 1 or np.isnan(u) or np.isnan(v):
                continue

            g = calculate_g(u, v, sign_u)
            g_values.append(g)

        # Calculate mean and standard deviation of g
        mean_g = np.mean(g_values)
        std_g = np.std(g_values)

        # Extract file identifier for output
        file_identifier = file_name.split("_")[-1][:4]

        # Store results for the current file
        results.append((file_identifier, mean_g, std_g))

# Write results to a text file in the output folder

os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, 'output.txt')
with open(output_path, 'w') as output_file:
    output_file.write("File, Mean of g, Standard Deviation of g\n")
    for result in results:
        output_file.write(f"{result[0]}, {result[1]}, {result[2]}\n")
