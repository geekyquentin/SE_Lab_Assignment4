# Imports
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def plot_visualization(image_dict, image, index, pred_masks):
    #################### Get the bounding box image ####################

    # Create the image to draw on
    bboxed_image = Image.fromarray((image * 255).astype(np.uint8)).convert('RGB')
    draw = ImageDraw.Draw(bboxed_image)

    # Set the font
    font = ImageFont.truetype("arial.ttf", 15)

    # Iterate over the annotations
    for annotation in image_dict['bboxes']:
        # Draw the bounding box
        draw.rectangle(annotation['bbox'], outline='red')

        # Draw the category
        draw.text((annotation['bbox'][0], annotation['bbox'][1]), annotation['category'], font=font, fill='yellow')

    # Save the bounding box image
    bboxed_image.save('outputs/bounding_boxes/' + index + '.png')

    #################### Get the segmented image ####################
    segmented_image = image * 255

    # apply the mask to the image
    for mask in pred_masks:
        segmented_image = segmented_image + ((np.transpose(mask, (1, 2, 0))) * [0, 1, 0.5] * 255)

    # convert the image numpy array to PIL image
    segmented_image = Image.fromarray(np.uint8(segmented_image)).convert('RGB')

    # Save the segmented image
    segmented_image.save('outputs/segmented_images/' + index + '.png')

    # return the segmented image and bounding box image
    return segmented_image, bboxed_image
