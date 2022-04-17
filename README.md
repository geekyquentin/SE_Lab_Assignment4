# Software Lab Assignment 4

## Python GUI Assignment (tkinter)

This is a follow up assignment to the [Python Datascience](https://github.com/geekyquentin/SE_Lab_Assignment3) assignment. A GUI is designed in this project using `tkinter` which would have the following overall functionality:

-   The GUI would provide the user to select a file from the computer.
-   It will have a dropdown menu to toggle between two output options: `Segmentation` and `Bounding-box`
-   If `Segmentation` is selected then it should show the segmentation map of the selected image file along with the original image file side-by-side.
-   For `Bounding-box` it should display the bounding boxes instead of the segmentation maps.
-   We will obtain the segmentation maps and the bounding boxes by taking help from the previous assignment (which you have already done).

When the user runs the [`ImageViewerGUI`](https://github.com/geekyquentin/SE_Lab_Assignment4/blob/master/ImageViewerGUI.py), a GUI pops-up with a `Browse` button and a dropdown menu with options `Segmentation` and `Bounding box`.

#### `Browse`:
Show a pop-up a dialog for the user to select an input image file. Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor. Once the output is computed it should be shown automatically based on choice the dropdown button is at.

#### `Process`:
Once the image is processed after selecting the input image file and the option in the dropdown menu is changed, click process to process the updated image.
