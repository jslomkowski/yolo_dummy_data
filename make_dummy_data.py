import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import random

parser = argparse.ArgumentParser(description='Generate shapes dataset')
parser.add_argument('--image_shape', type=int, nargs=2,
                    default=[200, 200], help='image shape (height, width)')
parser.add_argument('--box_size', type=int, nargs=2,
                    default=[10, 150], help='min and max box size')
parser.add_argument('--samples', type=int, default=10,
                    help='number of samples to generate')
parser.add_argument('--train_size', type=float, default=0.8,
                    help='train set size (percentage)')
parser.add_argument('--test_size', type=float, default=0.1,
                    help='test set size (percentage)')

args = parser.parse_args()

IMAGE_SHAPE = tuple(args.image_shape)
BOX_SIZE = np.random.randint(args.box_size[0], args.box_size[1])
SAMPLES = args.samples
TRAIN_SIZE = args.train_size
TEST_SIZE = args.test_size

# Remove existing dataset directory, if present
shutil.rmtree('datasets', ignore_errors=True)

# Create directories to save images and labels
for dataset_type in ['train', 'test', 'val']:
    for data_type in ['images', 'labels']:
        os.makedirs(
            f'datasets/shapes/{data_type}/{dataset_type}', exist_ok=True)

print("working...")
# Generate images and labels
for i in range(SAMPLES):
    # Generate random shape and box size and position
    shape_class = np.random.randint(0, 3)
    box_position = np.random.randint(
        0, IMAGE_SHAPE[0] - BOX_SIZE), np.random.randint(0, IMAGE_SHAPE[1] - BOX_SIZE)

    # Create figure and shape
    fig, ax = plt.subplots(figsize=(6, 6))
    if shape_class == 0:
        shape = plt.Rectangle(box_position, BOX_SIZE, BOX_SIZE,
                              linewidth=1, edgecolor='black', facecolor='black')
    elif shape_class == 1:
        shape = plt.Circle((
            box_position[0] + BOX_SIZE / 2, box_position[1] + BOX_SIZE / 2),
            BOX_SIZE / 2, linewidth=1, edgecolor='black', facecolor='black')
    else:
        shape = plt.Polygon(np.array(
            [(box_position[0] + BOX_SIZE / 2, box_position[1]),
             (box_position[0],
             box_position[1] + BOX_SIZE),
             (box_position[0] + BOX_SIZE, box_position[1] + BOX_SIZE)]),
            linewidth=1, edgecolor='black', facecolor='black')
    ax.add_patch(shape)

    # Set axis limits and remove axis
    ax.set_xlim(0, IMAGE_SHAPE[0])
    ax.set_ylim(0, IMAGE_SHAPE[1])
    # ax.invert_yaxis()
    ax.set_axis_off()

    # Save image and define YOLO labels
    image_path = f'datasets/shapes/random_{i}.png'
    plt.savefig(image_path, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()

    class_name = str(shape_class)
    x_center = (box_position[0] + BOX_SIZE / 2) / IMAGE_SHAPE[0]
    y_center = (IMAGE_SHAPE[1] - box_position[1] -
                BOX_SIZE / 2) / IMAGE_SHAPE[1]
    width = BOX_SIZE / IMAGE_SHAPE[0]
    height = BOX_SIZE / IMAGE_SHAPE[1]

    # Save YOLO labels to a text file
    label_path = f'datasets/shapes/random_{i}.txt'
    with open(label_path, 'w') as f:
        f.write(
            f"{class_name} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

# Get a list of all the generated images and shuffle it
images = [f'datasets/shapes/random_{i}.png' for i in range(SAMPLES)]
random.shuffle(images)

# Split the images into train, test, and validation sets
train_size = int(len(images) * TRAIN_SIZE)
test_size = int(len(images) * TEST_SIZE)

train_images = images[:train_size]
test_images = images[train_size:train_size + test_size]
val_images = images[train_size + test_size:]

# Move the images and labels to their respective directories
for dataset_type, images in zip(['train', 'test', 'val'], [train_images, test_images, val_images]):
    for image_path in images:
        shutil.move(image_path, f'datasets/shapes/images/{dataset_type}')
        label_path = image_path.replace('.png', '.txt')
        shutil.move(label_path, f'datasets/shapes/labels/{dataset_type}')
print("done...")
