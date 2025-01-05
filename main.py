import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import json

class ImageLabelingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Labeling App")
        
        # Initialize Variables
        self.image = None
        self.image_tk = None
        self.canvas_image = None
        self.zoom_level = 1.0
        self.polygons = []
        self.current_polygon = []
        # self.labels = ["Label1", "Label2"]
        self.labels = ["Not Defined"]
        self.annotations = []
        self.selected_label = tk.StringVar(value="Select Label")

        # UI Elements
        self.create_ui()

    def create_ui(self):
        # Toolbar
        toolbar = tk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(toolbar, text="Load Image", command=self.load_image).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Add Label", command=self.add_label).pack(side=tk.LEFT)
        tk.Button(toolbar, text="Save Annotations", command=self.save_annotations).pack(side=tk.LEFT)

        # Canvas with Scrollbars
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.canvas_frame, bg="gray")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.h_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.v_scroll = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.canvas.bind("<MouseWheel>", self.zoom_image)
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.pan_image)
        self.canvas.bind("<Button-1>", self.add_polygon_point)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not file_path:
            return

        # Load Image
        self.image = Image.open(file_path)
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.delete("all")  # Clear canvas
        self.polygons.clear()
        self.current_polygon.clear()
        self.annotations.clear()
        self.zoom_level = 1.0

        # Display Image
        self.canvas_image = self.canvas.create_image(0, 0, image=self.image_tk, anchor=tk.NW)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def add_label(self):
        new_label = simpledialog.askstring("Add Label", "Enter new label:")
        if new_label and new_label not in self.labels:
            self.labels.append(new_label)
            messagebox.showinfo("Success", f"Label '{new_label}' added!")

    def add_polygon_point(self, event):
        if not self.image:
            return

        # Get the coordinates in the canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        # Adjust for zoom: divide canvas coordinates by zoom level
        image_x = canvas_x / self.zoom_level
        image_y = canvas_y / self.zoom_level

        if self.current_polygon:
            # Check for closure (if the polygon is closed, finalize it)
            first_x, first_y = self.current_polygon[0]
            if abs(image_x - first_x) < 10 and abs(image_y - first_y) < 10:
                self.finalize_polygon()
                return

        self.current_polygon.append((image_x, image_y))
        self.redraw_canvas()


    def finalize_polygon(self):
        if len(self.current_polygon) < 3:
            messagebox.showerror("Error", "A polygon must have at least 3 points.")
            self.current_polygon = []
            return

        # Create a new window for label selection
        label_window = tk.Toplevel(self.root)
        label_window.title("Select Label")
        label_window.geometry("300x150")

        tk.Label(label_window, text="Select a label for this polygon:").pack(pady=10)

        label_dropdown = ttk.Combobox(label_window, values=self.labels, state="readonly")
        label_dropdown.pack(pady=10)
        label_dropdown.set("Select Label")

        def on_confirm():
            selected_label = label_dropdown.get()
            if not selected_label or selected_label == "Select Label":
                messagebox.showerror("Error", "You must select a label.")
                return

            # Save Polygon
            self.annotations.append({
                "points": self.current_polygon,
                "label": selected_label
            })
            self.polygons.append((self.current_polygon, selected_label))
            self.current_polygon = []
            self.redraw_canvas()
            label_window.destroy()

        tk.Button(label_window, text="Confirm", command=on_confirm).pack(pady=10)

        # Block interaction with the main window until the label is selected
        self.root.wait_window(label_window)


    def redraw_canvas(self):
        self.canvas.delete("polygon_temp")
        for polygon, label in self.polygons:
            # Scale the polygon points based on the zoom level
            scaled_polygon = [(x * self.zoom_level, y * self.zoom_level) for x, y in polygon]
            self.canvas.create_polygon(
                scaled_polygon, outline="red", fill="", width=2, tags="polygon_temp"
            )
            # Scale the centroid position for the label
            centroid_x = sum(p[0] for p in scaled_polygon) / len(scaled_polygon)
            centroid_y = sum(p[1] for p in scaled_polygon) / len(scaled_polygon)
            self.canvas.create_text(
                centroid_x, centroid_y, text=label, fill="white", tags="polygon_temp"
            )

        # Draw the current polygon (in-progress)
        if self.current_polygon:
            scaled_current_polygon = [
                (x * self.zoom_level, y * self.zoom_level) for x, y in self.current_polygon
            ]
            self.canvas.create_polygon(
                scaled_current_polygon, outline="blue", fill="", dash=(4, 2), tags="polygon_temp"
            )


    def save_annotations(self):
        if not self.annotations:
            messagebox.showerror("Error", "No annotations to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if not file_path:
            return

        data = {
            "annotations": [
                {
                    "points": annotation["points"],
                    "label": annotation["label"]
                }
                for annotation in self.annotations
            ]
        }
        with open(file_path, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Success", f"Annotations saved to {file_path}.")

    def zoom_image(self, event):
        if not self.image:
            return

        scale = 1.1 if event.delta > 0 else 0.9
        new_zoom_level = self.zoom_level * scale

        # Avoid zooming too far in or out
        if new_zoom_level < 0.1 or new_zoom_level > 10:
            return

        self.zoom_level = new_zoom_level
        resized_image = self.image.resize(
            (int(self.image.width * self.zoom_level), int(self.image.height * self.zoom_level))
        )
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.canvas.itemconfig(self.canvas_image, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

        # Redraw shapes and labels with the updated zoom level
        self.redraw_canvas()


    def start_pan(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def pan_image(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageLabelingApp(root)
    root.mainloop()
