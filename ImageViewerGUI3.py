####### REQUIRED IMPORTS FROM THE PREVIOUS ASSIGNMENT #######
from my_package.model import InstanceSegmentationModel
from my_package.data import Dataset
from my_package.analysis import plot_visualization
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
from PIL import Image

####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from tkinter import Tk, StringVar, Button, Entry, OptionMenu, filedialog, Label
from itertools import chain
from PIL import ImageTk
import numpy as np
import os


# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor):
    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.

    # declare the global variable
    global selected_option

    # get the folder path
    path = os.path.join(os.getcwd(), 'data', 'imgs').replace('\\', '/') + '/'

    # get the filetypes
    filetypes = ("jpeg files", "*.jpg"), ("all files", "*.*")

    # pop up the file browser
    file_browser = filedialog.askopenfilename(initialdir=path, title="Select file", filetypes=filetypes)

    # get the selected file
    selected_image = Image.open(file_browser)

    # update the entry box
    e.delete(0, 'end')
    e.insert(0, "Image: " + file_browser.split('/')[-1])

    # get the selected file index
    index = file_browser.split('/')[-1].split('.')[0]

    # get the data item with the corresponding index
    data_item = dataset[int(index)]

    # get the image
    image = data_item['image']

    # get the predictions from the segmentor
    pred_boxes, pred_masks, pred_class, pred_score = segmentor(image)

    # get the top 3 predictions
    if len(pred_score) > 3:
        pred_boxes = pred_boxes[:3]
        pred_masks = pred_masks[:3]
        pred_class = pred_class[:3]
        pred_score = pred_score[:3]

    # get the bboxes from the data item
    data_item['bboxes'] = []
    for j in range(len(pred_score)):
        temp_dict = {}
        temp_dict['bbox'] = list(chain.from_iterable(pred_boxes[j]))

        # Convert the bounding box to integers
        for k in range(len(temp_dict['bbox'])):
            temp_dict['bbox'][k] = int(temp_dict['bbox'][k])

        # Add the category and append to the dictionary
        temp_dict['category'] = pred_class[j]
        data_item['bboxes'].append(temp_dict)

    # Get the segmented image and bounding box image
    segmented_image, bboxed_image = plot_visualization(data_item, image.transpose((1, 2, 0)), index, pred_masks)

    # Display the selected image and modified image
    if clicked.get() == "Segmentation":
        modified_image = segmented_image
    elif clicked.get() == "Bounding-box":
        modified_image = bboxed_image

    # Update the selected option
    selected_option = clicked.get()

    ############### Display the selected image and modified image ###############

    # Remove the previous selected image from the root window
    for slave in root.grid_slaves(row=1, column=0):
        slave.grid_forget()

    # Convert the selected image to PIL format
    selected_image = ImageTk.PhotoImage(selected_image)

    # Create a label for the selected image
    selected_image_label = Label(root, image=selected_image)
    selected_image_label.image = selected_image

    # Set the position of the label
    selected_image_label.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

    # Remove the previous modified image from the root window
    for slave in root.grid_slaves(row=1, column=4):
        slave.grid_forget()

    # Convert the modified image to PIL format
    modified_image = ImageTk.PhotoImage(modified_image)

    # Create a label for the modified image
    modified_image_label = Label(root, image=modified_image)
    modified_image_label.image = modified_image

    # Set the position of the label
    modified_image_label.grid(row=1, column=4, padx=10, pady=10)

####### CODE REQUIRED (END) #######


# `process` function definition starts from here.
# will process the output when clicked.
def process(clicked):
    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.

    # declare the global variable
    global selected_option

    # check if any image is selected
    if e.get() == "":
        print("Select an image to process")
        return

    # check if the options in the dropdown are changed
    if clicked.get() == selected_option:
        return

    ############### change the modify image ###############

    # get the index of the selected image
    index = e.get().split(' ')[-1].split('.')[0]

    # get the path of the outputs folder
    path = os.path.join(os.getcwd(), 'outputs').replace('\\', '/') + '/'

    # get the image from the outputs folder
    if clicked.get() == "Segmentation":
        modified_image = Image.open(path + 'segmented_images/' + index + '.png')
    elif clicked.get() == "Bounding-box":
        modified_image = Image.open(path + 'bounding_boxes/' + index + '.png')

    ############### Update the modified image ###############

    # Remove the previous modified image from the root window
    for slave in root.grid_slaves(row=1, column=4):
        slave.grid_forget()

    # Convert the modified image to PIL format
    modified_image = ImageTk.PhotoImage(modified_image)

    # Create a label for the modified image
    modified_image_label = Label(root, image=modified_image)
    modified_image_label.image = modified_image

    # Set the position of the label
    modified_image_label.grid(row=1, column=4, padx=10, pady=10)

    # update the selected option
    selected_option = clicked.get()

    ####### CODE REQUIRED (END) #######


    # `main` function definition starts from here.
if __name__ == '__main__':

    # CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = Tk()
    root.title("Image Viewer")

    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)

    # Declare the options.
    options = ["Segmentation", "Bounding-box"]
    clicked = StringVar()
    clicked.set(options[0])

    e = Entry(root, width=70)
    e.grid(row=0, column=0)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    browse_button = Button(root, text="Browse", command=lambda: fileClick(clicked, dataset, segmentor))
    browse_button.grid(row=0, column=1)

    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    dropdown_button = OptionMenu(root, clicked, *options)
    dropdown_button.grid(row=0, column=2)

    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process", command=lambda: process(clicked))
    myButton.grid(row=0, column=3)

    # CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()

    ####### CODE REQUIRED (END) #######
