import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import random

image_shape = (200, 200)
box_size = np.random.randint(10, 150)
samples = 10

# Remove existing dataset directory, if present
shutil.rmtree('datasets', ignore_errors=True)

# Create directories to save images and labels
for dataset_type in ['train', 'test', 'val']:
    for data_type in ['images', 'labels']:
        os.makedirs(
            f'datasets/shapes/{data_type}/{dataset_type}', exist_ok=True)


# Generate images and labels
for i in range(samples):
    # Generate random shape and box size and position
    shape_class = np.random.randint(0, 3)
    box_position = np.random.randint(
        0, image_shape[0] - box_size), np.random.randint(0, image_shape[1] - box_size)

    # Create figure and shape
    fig, ax = plt.subplots(figsize=(6, 6))
    if shape_class == 0:
        shape = plt.Rectangle(box_position, box_size, box_size,
                              linewidth=1, edgecolor='black', facecolor='black')
    elif shape_class == 1:
        shape = plt.Circle((box_position[0] + box_size / 2, box_position[1] + box_size / 2),
                           box_size / 2, linewidth=1, edgecolor='black', facecolor='black')
    else:
        shape = plt.Polygon(np.array([(box_position[0] + box_size / 2, box_position[1]),
                                      (box_position[0],
                                       box_position[1] + box_size),
                                      (box_position[0] + box_size, box_position[1] + box_size)]),
                            linewidth=1, edgecolor='black', facecolor='black')
    ax.add_patch(shape)

    # Set axis limits and remove axis
    ax.set_xlim(0, image_shape[0])
    ax.set_ylim(0, image_shape[1])
    ax.invert_yaxis()
    ax.set_axis_off()

    # Save image and define YOLO labels
    image_path = f'datasets/shapes/random_{i}.png'
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

    class_name = str(shape_class)
    x_center = (box_position[0] + box_size / 2) / image_shape[0]
    y_center = (image_shape[1] - box_position[1] -
                box_size / 2) / image_shape[1]
    width = box_size / image_shape[0]
    height = box_size / image_shape[1]

    # Save YOLO labels to a text file
    label_path = f'datasets/shapes/random_{i}.txt'
    with open(label_path, 'w') as f:
        f.write(
            f"{class_name} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

# Get a list of all the generated images and shuffle it
images = [f'datasets/shapes/random_{i}.png' for i in range(samples)]
random.shuffle(images)

# Split the images into train, test, and validation sets
train_size = int(len(images) * 0.8)
test_size = int(len(images) * 0.1)

train_images = images[:train_size]
test_images = images[train_size:train_size + test_size]
val_images = images[train_size + test_size:]

# Move the images and labels to their respective directories
for dataset_type, images in zip(['train', 'test', 'val'], [train_images, test_images, val_images]):
    for image_path in images:
        shutil.move(image_path, f'datasets/shapes/images/{dataset_type}')
        label_path = image_path.replace('.png', '.txt')
        shutil.move(label_path, f'datasets/shapes/labels/{dataset_type}')
