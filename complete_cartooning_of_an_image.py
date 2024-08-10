import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
from sketchify import sketch

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", ".jpg;.jpeg;*.png")])
    if file_path:
        # Perform cartoonizing, sketching, and alien effect
        cartoonize_image(file_path)
        sketch_image(file_path)
        alien_style_image(file_path)

        # Load and display images
        show_images()

def cartoonize_image(file_path):
    img = cv2.imread(file_path)
    img=increase_saturation(img, saturation_scale=1.5)
    img = cv2.resize(img, (900, 550))
    
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resize = cv2.resize(grey, (900, 550))
    smoothGrayScale = cv2.medianBlur(resize, 3)
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 9)
    
    colorImage = cv2.bilateralFilter(img, 9, 300, 300)
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    
    # Save cartoon image
    cartoon_image_path = 'cartoon_image.jpg'
    cv2.imwrite(cartoon_image_path, cartoonImage)

def sketch_image(file_path):
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the sketchify process
    sketch.normalsketch(file_path, output_dir, 'sketched_image')

    # Define paths
    sketched_image_path = os.path.join(output_dir, 'sketched_image.png')
    final_image_path = 'sketched_image.png'

    # Check if the final file already exists and remove it if necessary
    if os.path.exists(final_image_path):
        os.remove(final_image_path)

    # Check if the sketched image file exists before renaming
    if os.path.exists(sketched_image_path):
        os.rename(sketched_image_path, final_image_path)
        print("Sketch image saved as", final_image_path)
    else:
        print("Error: Sketched image file not found at", sketched_image_path)

def alien_style_image(file_path):
    # Load the image
    image = cv2.imread(file_path)
    if image is None:
        print("Error: Image not loaded.")
        return

    # Increase saturation
    saturated_image = increase_saturation(image, saturation_scale=1.5)

    # Apply a color map to create an alien-like effect
    alien_image = cv2.applyColorMap(saturated_image, cv2.COLORMAP_COOL)

    # Apply Gaussian blur to smoothen the image
    alien_image = cv2.GaussianBlur(alien_image, (7, 7), 0)

    # Convert to HSV and adjust hue for an alien skin tone
    hsv_image = cv2.cvtColor(alien_image, cv2.COLOR_BGR2HSV)
    hue_shift = 30
    hsv_image[:, :, 0] = (hsv_image[:, :, 0] + hue_shift) % 180

    # Convert back to BGR
    alien_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Enhance edges using Canny edge detector
    edges = cv2.Canny(alien_image, threshold1=100, threshold2=200)
    edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    # Combine edges with the original image
    alien_image_with_edges = cv2.addWeighted(alien_image, 0.8, edges_colored, 0.2, 0)

    # Save the alien-styled image
    output_path = 'alien_image.jpg'
    cv2.imwrite(output_path, alien_image_with_edges)

def increase_saturation(image, saturation_scale=1.5):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.clip(s * saturation_scale, 0, 255).astype(np.uint8)
    hsv_enhanced = cv2.merge([h, s, v])
    bgr_enhanced = cv2.cvtColor(hsv_enhanced, cv2.COLOR_HSV2BGR)
    return bgr_enhanced

def show_images():
    # Create a new window for displaying images
    image_window = tk.Toplevel()
    image_window.title("Processed Images")

    # Load and display cartoon image at the top
    cartoon_img = Image.open('cartoon_image.jpg')
    cartoon_img = cartoon_img.resize((600, 350))  # Resize for display purposes
    cartoon_photo = ImageTk.PhotoImage(cartoon_img)
    
    tk.Label(image_window, text="Cartoonized Image").grid(row=0, column=0, columnspan=3, pady=10)
    tk.Label(image_window, image=cartoon_photo).grid(row=1, column=0, columnspan=3, padx=10)
    
    # Load and display sketched image on the left
    sketched_img = Image.open('sketched_image.png')
    sketched_img = sketched_img.resize((275, 275))  # Resize for display purposes
    sketched_photo = ImageTk.PhotoImage(sketched_img)
    
    tk.Label(image_window, text="Sketched Image").grid(row=2, column=0, padx=10, pady=10)
    tk.Label(image_window, image=sketched_photo).grid(row=3, column=0, padx=10)
    
    # Load and display alien-styled image on the right
    alien_img = Image.open('alien_image.jpg')
    alien_img = alien_img.resize((275, 275))  # Resize for display purposes
    alien_photo = ImageTk.PhotoImage(alien_img)
    
    tk.Label(image_window, text="Alien-Styled Image").grid(row=2, column=1, padx=10, pady=10)
    tk.Label(image_window, image=alien_photo).grid(row=3, column=1, padx=10)
    
    # Keep references to prevent garbage collection
    image_window.cartoon_photo = cartoon_photo
    image_window.sketched_photo = sketched_photo
    image_window.alien_photo = alien_photo

# Create the main window
root = tk.Tk()
root.title("Image Processing")

# Set the window size
root.geometry("400x300")

# Set the background color
root.configure(bg='aqua')

# Add a title label
label = tk.Label(root, text="Upload an image to process", font=('Arial', 16), bg='aliceblue', fg='black', padx=20, pady=10)
label.pack(pady=(20, 10))

# Add an upload button
button = tk.Button(root, text="Upload", bg='azure', fg='black', command=upload_image)
button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
