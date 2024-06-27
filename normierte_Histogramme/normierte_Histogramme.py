import os
import numpy as np
import matplotlib.pyplot as plt
import csv

input_folder = "Input"
output_folder = "Output"


def create_histogram(input_folder, output_folder):
    # List of files in the input folder
    file_list = os.listdir(input_folder)

    # Loop through the files
    for file_name in file_list:
        if file_name.endswith('.tif'):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, file_name.replace('.tif', '.csv'))

            # Read the images and convert to grayscale if necessary
            image = plt.imread(input_file_path)
            if len(image.shape) == 3:
                image = np.mean(image, axis=2)

            # Calculate the histogram
            histogram, bin_edges = np.histogram(image, bins=256, range=(0, 256))

            # Calculate the total number of pixels in the image
            total_pixels = np.sum(histogram)

            # Save the total and normalized histogram in a CSV file
            with open(output_file_path, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['pixel value', 'frequency', 'frequency in percent'])

                for value, frequency in zip(bin_edges[:-1], histogram):
                    percentage = (frequency / total_pixels) * 100 if total_pixels > 0 else 0
                    writer.writerow([int(value), int(frequency), "{:.16f}".format(percentage)])


create_histogram(input_folder, output_folder)
