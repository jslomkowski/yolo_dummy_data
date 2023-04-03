import random
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

num_images = 100
img_size = 500
max_box_size = 200
min_box_size = 50
max_num_boxes = 1
min_num_boxes = 1
train_ratio = 0.7
test_ratio = 0.1
val_ratio = 0.2

try:
    shutil.rmtree('datasets')
except FileNotFoundError:
    pass

# Create directories to save images and labels
os.makedirs('datasets/shapes/images/train', exist_ok=True)
os.makedirs('datasets/shapes/images/test', exist_ok=True)
os.makedirs('datasets/shapes/images/val', exist_ok=True)
os.makedirs('datasets/shapes/labels/train', exist_ok=True)
os.makedirs('datasets/shapes/labels/test', exist_ok=True)
os.makedirs('datasets/shapes/labels/val', exist_ok=True)

# Calculate number of images for each set
num_train_images = int(num_images * train_ratio)
num_test_images = int(num_images * test_ratio)
num_val_images = int(num_images * val_ratio)

# Initialize counters for each set
train_counter = 0
test_counter = 0
val_counter = 0

for i in range(num_images):
    fig, ax = plt.subplots()
    ax.set_xlim([0, img_size])
    ax.set_ylim([0, img_size])
    ax.axis('off')  # Remove axis
    num_boxes = random.randint(min_num_boxes, max_num_boxes)
    shapes = ['rectangle', 'circle', 'triangle']
    boxes = []
    for j in range(num_boxes):
        shape = random.choice(shapes)
        if shape == 'rectangle':
            box_size = random.randint(min_box_size, max_box_size)
            x1 = random.randint(0, img_size - box_size)
            y1 = random.randint(0, img_size - box_size)
            x2 = x1 + box_size
            y2 = y1 + box_size
            boxes.append((x1, y1, x2, y2))
            rect = plt.Rectangle((x1, y1), box_size, box_size,
                                 linewidth=1, edgecolor='black', facecolor='black')
            ax.add_patch(rect)
        elif shape == 'circle':
            radius = random.randint(min_box_size // 2, max_box_size // 2)
            x_center = random.randint(radius, img_size - radius)
            y_center = random.randint(radius, img_size - radius)
            boxes.append((x_center - radius, y_center - radius,
                         x_center + radius, y_center + radius))
            circle = plt.Circle((x_center, y_center), radius,
                                linewidth=1, edgecolor='black', facecolor='black')
            ax.add_patch(circle)
        elif shape == 'triangle':
            size = random.randint(min_box_size, max_box_size)
            x1 = random.randint(0, img_size - size)
            y1 = random.randint(0, img_size - size)
            x2 = x1 + size
            y2 = y1
            x3 = x1 + size // 2
            y3 = y1 + size
            boxes.append((x1, y1, x2, y3))
            triangle = plt.Polygon(
                [(x1, y1), (x2, y2), (x3, y3)], linewidth=1, edgecolor='black', facecolor='black')
            ax.add_patch(triangle)

    # Save image to 'datasets/shapes/images/'
    filename = f'random_image_{i}.png'
    plt.savefig(f'datasets/shapes/images/{filename}')
    plt.close()

    # Save box positions to a text file in YOLO format to 'datasets/shapes/labels/'
    with open(f'datasets/shapes/labels/{os.path.splitext(filename)[0]}.txt', 'w') as f:
        for box in boxes:
            if len(box) == 4:  # Rectangle or triangle
                x_center = (box[0] + box[2]) / 2 / img_size
                y_center = (box[1] + box[3]) / 2 / img_size
                width = (box[2] - box[0]) / img_size
                height = (box[3] - box[1]) / img_size
                f.write(
                    f'0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n')
            elif len(box) == 2:  # Circle
                x_center = box[0] / img_size
                y_center = box[1] / img_size
                radius = (box[2] - box[0]) / 2
                f.write(f'1 {x_center:.6f} {y_center:.6f} {radius:.6f}\n')

    # Split the dataset into train, test, and val
    if train_counter < num_train_images:
        # Save image to 'datasets/shapes/images/train/'
        shutil.move(
            f'datasets/shapes/images/{filename}', 'datasets/shapes/images/train/')
        # Save label to 'datasets/shapes/labels/train/'
        shutil.move(
            f'datasets/shapes/labels/{os.path.splitext(filename)[0]}.txt', 'datasets/shapes/labels/train/')
        train_counter += 1
    elif test_counter < num_test_images:
        # Save image to 'datasets/shapes/images/test/'
        shutil.move(
            f'datasets/shapes/images/{filename}', 'datasets/shapes/images/test/')
        # Skip saving label for test set
        os.remove(
            f'datasets/shapes/labels/{os.path.splitext(filename)[0]}.txt')
        test_counter += 1
    elif val_counter < num_val_images:
        # Save image to 'datasets/shapes/images/val/'
        shutil.move(
            f'datasets/shapes/images/{filename}', 'datasets/shapes/images/val/')
        # Save label to 'datasets/shapes/labels/val/'
        shutil.move(
            f'datasets/shapes/labels/{os.path.splitext(filename)[0]}.txt', 'datasets/shapes/labels/val/')
        val_counter += 1
