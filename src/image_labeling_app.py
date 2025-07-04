import streamlit as st
import os
import random
import json
from PIL import Image
from collections import defaultdict

# Set folder names
FOLDER_A = "FOLDER_A"
FOLDER_B = "FOLDER_B"

# Define results storage file for image stats
RESULTS_FILE = "image_stats.json"

# Load image paths
def load_images():
    images = []
    for folder in [FOLDER_A, FOLDER_B]:
        if os.path.exists(folder):
            for file in os.listdir(folder):
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    images.append((os.path.join(folder, file), folder))
    return images

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = {'correct': 0, 'incorrect': 0}
if 'image_stats' not in st.session_state:
    st.session_state.image_stats = defaultdict(lambda: {'correct': 0, 'incorrect': 0})
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'guess' not in st.session_state:
    st.session_state.guess = None
if 'feedback' not in st.session_state:
    st.session_state.feedback = None  # Stores feedback (Correct/Incorrect)

# Load all images
all_images = load_images()

# Function to pick a new image
def pick_new_image():
    if all_images:
        st.session_state.current_image = random.choice(all_images)

# Function to load existing image stats from file
def load_image_stats():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save image stats to file
def save_image_stats(image_stats):
    with open(RESULTS_FILE, "w") as file:
        json.dump(image_stats, file, indent=4)

# Load existing image stats from file into session state
existing_stats = load_image_stats()
for image, stats in existing_stats.items():
    st.session_state.image_stats[image]['correct'] = stats.get('correct', 0)
    st.session_state.image_stats[image]['incorrect'] = stats.get('incorrect', 0)

# Title
st.title("Real or Synthetic?")

# Show current image or pick a new one
if st.session_state.current_image is None:
    pick_new_image()

if st.session_state.current_image:
    image_path, true_folder = st.session_state.current_image
    print(f"Image Path: {image_path}, True Folder: {true_folder}")
    image = Image.open(image_path)
    st.image(image, caption="Is this image Real or Synthetic?", use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Real"):
            st.session_state.guess = FOLDER_A
            print(f"User guessed Real, value: {st.session_state.guess}")
    with col2:
        if st.button("Synthetic"):
            st.session_state.guess = FOLDER_B
            print(f"User guessed Synthetic, value: {st.session_state.guess}")


    if st.session_state.guess:
        if st.session_state.guess == true_folder:
            print(f"User guessed correctly: {st.session_state.guess} matches {true_folder}\n")
            st.session_state.score['correct'] += 1
            st.session_state.feedback = "Correct!"
            # st.success("Correct!") #Comment this in case you dont want to give feedback after selection
            st.session_state.image_stats[image_path]['correct'] += 1
        else:
            print(f"User guessed incorrectly: {st.session_state.guess} does not match {true_folder}\n")
            st.session_state.score['incorrect'] += 1
            st.session_state.feedback = "Incorrect."
            # st.error("Incorrect.") #Comment this in case you dont want to give feedback after selection
            st.session_state.image_stats[image_path]['incorrect'] += 1

        save_image_stats(st.session_state.image_stats)
        
        st.session_state.guess = None
        pick_new_image()
        st.rerun()

# # Display feedback (if available) from last interaction # Comment this in case you dont want to give feedback after selection
# if st.session_state.feedback:
#     st.write(st.session_state.feedback)  # Show Correct/Incorrect message
#     st.session_state.feedback = None  # Clear feedback after displaying

# Stop and show results
if st.button("Stop and Show Results"):

    # Show session summary results
    st.subheader("Session Summary Results")
    st.write(f"Correct: {st.session_state.score['correct']}")
    st.write(f"Incorrect: {st.session_state.score['incorrect']}")

    st.subheader("General Per-Image Accuracy")
    for img_path, stats in st.session_state.image_stats.items():
        total = stats['correct'] + stats['incorrect']
        accuracy = stats['correct'] / total if total > 0 else 0
        st.write(f"{os.path.basename(img_path)} Accuracy: {accuracy:.2%} ({stats['correct']} correct, {stats['incorrect']} incorrect)")

    # # Displays saved image stats file contents (debugging)
    # st.subheader("Saved Image Stats")
    # st.json(load_image_stats())