import logging
import os
import cv2
import numpy as np
import json


def pick_point_in_image(rim_dir, points, npoints=4):
    """
    A function to pick the screen corners on the reference image,
    returns the corners points, and the ref image in openCV
    :param points:
    :param rim_dir: the directory of the reference image
    :param npoints: the number of corners to pick
    """
    # Pick the image
    image_path = os.path.join(rim_dir, "reference_image.jpeg")
    # Read the image
    image = cv2.imread(image_path)
    if points is None:
        # Create a downsample image for displaying in the corner selection. 480p height
        copy_image = image.copy()
        h, w = image.shape[0:2]
        resize_factor = 480 / h
        copy_image = cv2.resize(copy_image, (int(w * (480 / h)), 480))
        backup = copy_image.copy()
        points = []

        def pick_corners(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                if len(points) < npoints:
                    cv2.circle(param, (x, y), int(50 * resize_factor), (0, 0, 255), -1)
                    points.append((x, y))
                    logging.info(f"Picked point: {(x, y)}")
                    if len(points) == npoints:
                        cv2.putText(
                            param,
                            "Done, press Q to continue",
                            (int(param.shape[0] / 4), int(param.shape[1] / 2)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            5 * resize_factor,
                            (0, 0, 255),
                            int(15 * resize_factor),
                            2,
                        )
            elif event == cv2.EVENT_FLAG_RBUTTON:
                if len(points) > 0:
                    points.pop()
                    logging.info("Removed last point")
                    cv2.addWeighted(param, 0.1, backup, 0.9, 0, param)
                    for point in points:
                        cv2.circle(
                            param, point, int(50 * resize_factor), (0, 0, 255), -1
                        )
                else:
                    logging.info("No points to remove")

        cv2.namedWindow("Pick the corners of your ROI by clicking on the image")
        cv2.setMouseCallback(
            "Pick the corners of your ROI by clicking on the image",
            pick_corners,
            copy_image,
        )
        while True:
            cv2.imshow(
                "Pick the corners of your ROI by clicking on the image", copy_image
            )
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cv2.destroyAllWindows()
        # Get the points back to the original image size
        points = [
            (int(point[0] / resize_factor), int(point[1] / resize_factor))
            for point in points
        ]
    # Copy the points to the ref image
    for point in points:
        cv2.circle(image, point, 50, (0, 0, 255), -1)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Reorder the corners
    points = np.array(points)
    center = np.average(points, axis=0)
    diff_points = np.sign(points - center)
    points = points[np.lexsort((diff_points[:, 1], diff_points[:, 0]))]
    points = {
        "upper left": points[0, :],
        "lower left": points[1, :],
        "upper right": points[2, :],
        "lower right": points[3, :],
    }
    logging.info(points)
    return points, image

def parse_corners_file(corners_points: str, corners_image: str):
    with open(corners_points, "r") as points_file:
        # Load the JSON data from the file
        points_data = json.load(points_file)
    with open(corners_image, "r") as image_file:
        # Load the JSON data from the file
        image_data = json.load(image_file)

    points_dict = {key: np.array(value) for key, value in points_data.items()}

    # Convert to NumPy array
    image_array = np.array(image_data)

    # Convert to uint8 if needed
    image_array = image_array.astype(np.uint8)

    return points_dict, image_array


# import tkinter as tk
# from tkinter import filedialog

# def get_directory_path(title) -> str:
#     """
#     :param title: The title of the directory dialog.
#     :return: The path for the directory the user chose.
#     """
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window
#     directory_path: str = filedialog.askdirectory(
#         title=title,
#         initialdir="/path/to/default/directory")
#
#     if directory_path:
#         print("You chose the directory:", directory_path)
#     else:
#         raise NotADirectoryError("No directory selected")
#     return directory_path

# points, img = parse_corners_file("points.json", "image.json")
# rim_dir = get_directory_path("rim")
# points2, img2 = pick_point_in_image(
#     rim_dir,
#     None
# )
#
# print(type(points["upper left"][0]))
# print(type(points2["upper left"][0]))
# print(type(points) == type(points2))
#
# print(type(img[0][0][0]))
# print(type(img2[0][0][0]))
# print(type(img) == type(img2))