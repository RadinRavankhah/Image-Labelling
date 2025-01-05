# Image-Labelling
A simple app made to label items in images for training computer vision models


# Image Labeling App

An intuitive desktop application built with Python and Tkinter that allows users to label images by creating polygons over regions of interest and associating them with custom labels. The labeled data is saved as a JSON file, which can be used for tasks such as image annotation, machine learning datasets, and more.

## Features
- **Load Images:** Import images (PNG, JPG, JPEG) for labeling.
- **Add Labels:** Create custom labels dynamically.
- **Draw Polygons:** Label specific areas of an image by drawing polygons.
- **Zoom and Pan:** Adjust the view of the image with zoom and pan functionalities for precise labeling.
- **Save Annotations:** Save labeled polygons and their associated labels in a JSON file.

## Requirements
- Python 3.8 or higher
- Required Python Libraries:
  - `tkinter`
  - `Pillow`
  - `json`

You can install the required libraries using the following command:
```bash
pip install Pillow
```

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/image-labeling-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd image-labeling-app
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## How to Use
1. **Launch the App:** Run the Python script to start the application.

2. **Load an Image:** Click the `Load Image` button and select an image file (PNG, JPG, JPEG).

3. **Add Labels:**
   - Click the `Add Label` button to create a new label.
   - Enter the label name in the dialog box and click `OK`. The new label will be added to the list of available labels.

4. **Annotate the Image:**
   - Click on the image to add points of a polygon.
   - To close a polygon, click near the starting point. This will automatically finalize the polygon.
   - Select a label for the polygon in the pop-up window, then confirm.

5. **Zoom and Pan:**
   - Use the mouse scroll wheel to zoom in and out.
   - Click and drag the image to pan.

6. **Save Annotations:**
   - Click the `Save Annotations` button.
   - Choose a location to save the annotations as a JSON file.

## JSON Output Format
The annotations are saved in the following structure:
```json
{
  "annotations": [
    {
      "points": [[x1, y1], [x2, y2], [x3, y3], ...],
      "label": "LabelName"
    },
    ...
  ]
}
```
- `points`: List of (x, y) coordinates of the polygon's vertices.
- `label`: The label assigned to the polygon.

## Example Workflow
1. **Load Image:** Open an image for labeling.
2. **Create Labels:** Add labels such as "Cat", "Dog", or "Tree".
3. **Annotate:** Draw polygons over areas of interest and assign labels.
4. **Save:** Save the annotations to `annotations.json`.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the app.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Developed using the [Tkinter](https://docs.python.org/3/library/tkinter.html) library.
- Image handling powered by [Pillow](https://python-pillow.org/).

