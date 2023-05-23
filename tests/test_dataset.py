# this is manual test after building dataset
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pathlib

# those should be changed to your own values based on dataset you want to test:
file = "random_3"
data_set = 'train'

path = pathlib.Path(__file__).parents[1]
image = fr"{path}\datasets\shapes\images\{data_set}\{file}.png"
label = fr"{path}\datasets\shapes\labels\{data_set}\{file}.txt"

# Load image
img = plt.imread(image)

# Read label file
with open(label, 'r') as f:
    label = f.readline().split()

# Extract coordinates
x, y, w, h = [float(i) for i in label[1:]]

# Convert to pixel values
height, width, _ = img.shape
x1 = (x - w / 2) * width
y1 = (y - h / 2) * height
x2 = (x + w / 2) * width
y2 = (y + h / 2) * height

# Create figure and axis
fig, ax = plt.subplots()

# Display image
ax.imshow(img)

# Create rectangle patch
rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1,
                         linewidth=1, edgecolor='r', facecolor='none')

# Add patch to axis
ax.add_patch(rect)

# Show plot
plt.show()
