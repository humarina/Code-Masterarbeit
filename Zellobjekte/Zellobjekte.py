from PIL import Image, ImageDraw
import numpy as np

# Define image dimensions
width, height = 2464, 2056

# Define dimensions for each cell and gap between cells
cell_width, cell_height = 500, 200
gap = 100

# Create a black image
image = Image.new("L", (width, height), "black")
draw = ImageDraw.Draw(image)


# Function to draw irregular ellipses
def draw_irregular_ellipse(draw, bbox, num_bulges=10, jaggedness=0):
    # Calculate center and radii of the ellipse
    cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    rx, ry = (bbox[2] - bbox[0]) / 2, (bbox[3] - bbox[1]) / 2

    # Number of points to draw the ellipse
    num_points = 200
    angle_step = 2 * np.pi / num_points
    points = []

    # Iterate through points to draw the ellipse
    for i in range(num_points):
        angle = i * angle_step
        offset_x = rx * np.cos(angle)
        offset_y = ry * np.sin(angle)
        bulge_factor = 1 + 0.3 * np.sin(num_bulges * angle)

        # Apply jaggedness if provided
        if jaggedness:
            bulge_factor *= 1 + jaggedness * (np.random.uniform(-1, 1) ** 3)

        # Calculate coordinates with bulge factor
        x = cx + offset_x * bulge_factor
        y = cy + offset_y * bulge_factor
        points.append((x, y))

    # Draw the polygon with the calculated points
    draw.polygon(points, fill="white")


# Number of cells per column
num_cells_per_column = 2

# Calculate total height of cells and gaps
total_cell_height = (num_cells_per_column - 1) * cell_height + (num_cells_per_column - 1) * gap + cell_width

# Calculate vertical padding to center cells vertically
vertical_padding = (height - total_cell_height) // 2

# Define x positions for the cells
x_positions = [gap, width // 2 + gap]

# Loop through each x position
for x in x_positions:
    # Initialize y position with vertical padding
    y_position = vertical_padding

    # Draw cells at each x position
    if x == gap:
        # First column with regular and irregular ellipses
        circle_size = cell_width / 2
        circle_offset = circle_size / 2

        # Draw circle
        bbox = [x + circle_offset, y_position, x + circle_offset + circle_size, y_position + circle_size]
        draw.ellipse(bbox, outline="white", fill="white")
        y_position += circle_size + gap

        # Draw regular ellipse
        bbox = [x, y_position, x + cell_width, y_position + cell_height]
        draw.ellipse(bbox, outline="white", fill="white")
        y_position += cell_height + gap

        # Draw irregular ellipse with 4 bulges
        bbox = [x, y_position, x + cell_width, y_position + cell_height]
        draw_irregular_ellipse(draw, bbox, num_bulges=4)
        y_position += cell_height + gap

        # Draw irregular ellipse with 6 bulges
        bbox = [x, y_position, x + cell_width, y_position + cell_height]
        draw_irregular_ellipse(draw, bbox, num_bulges=6)
    else:
        # Second column with irregular ellipses and jaggedness
        circle_size = cell_width / 2
        circle_offset = circle_size / 2

        # Draw irregular ellipse without bulges and with jaggedness
        bbox = [x + circle_offset, y_position, x + circle_offset + circle_size, y_position + circle_size]
        draw_irregular_ellipse(draw, bbox, num_bulges=0, jaggedness=0.05)
        y_position += circle_size + gap

        # Draw irregular ellipse without bulges and with jaggedness
        bbox = [x, y_position, x + cell_width, y_position + cell_height]
        draw_irregular_ellipse(draw, bbox, num_bulges=0, jaggedness=0.05)
        y_position += cell_height + gap

        # Draw irregular ellipse with 4 bulges and with jaggedness
        bbox = [x, y_position, x + cell_width, y_position + cell_height]
        draw_irregular_ellipse(draw, bbox, num_bulges=4, jaggedness=0.05)
        y_position += cell_height + gap

        # Draw irregular ellipse with 6 bulges and with jaggedness
        bbox = [x, y_position, x + cell_width, y_position + cell_height]
        draw_irregular_ellipse(draw, bbox, num_bulges=6, jaggedness=0.05)

# Save the image
image.save("Generated_cell_structures.tiff")
