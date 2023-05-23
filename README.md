
# Yolo dummy data
This is under developement. and structure does not represent final package structure.

this is a project that aims to generate sample data for computer vision algorithms and the bounding boxes.

## Getting Started
-----------------------------
install the package using pip
```bash
pip install git+https://github.com/jslomkowski/yolo_dummy_data.git
```

The parameters that can be changed are the size of the image, the size of the boxes and the number of samples generated.

The code uses the argparse module to create a command-line interface for generating a shapes dataset. The program takes in various arguments to customize the dataset.

`--image_shape`: A tuple specifying the height and width of the generated images. This argument is optional and defaults to [200, 200]. It should be noted that the height and width must be greater or equal than the max box_size.

`--box_size`: A tuple specifying the minimum and maximum size of the bounding box around the shape in each image. This argument is optional and defaults to [10, 150].

`--samples`: An integer specifying the number of images to generate. This argument is optional and defaults to 10.

`--train_size`: A float specifying the percentage of samples to be used for training. This argument is optional and defaults to 0.8 (80%).

`--test_size`: A float specifying the percentage of samples to be used for testing. This argument is optional and defaults to 0.1 (10%).

Example usage:

```bash
generate_shapes_dataset --image_shape 200 200 --box_size 25 50 --samples 100 --train_size 0.7 --test_size 0.2
```
