import sys


sys.path.append("/Users/edwardlance/MMR_Labs/mmr_labs_and_exercises/")

from gui_module.base_controller import BaseController
from gui_module.app import app
import os  # Module for interacting with the operating system
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

"""
Things to know:
1. initialize_folders method and how it's called from init
2. 
"""
class RealController(BaseController):

    def __init__(self):
        self.initialize_folders()

    def retrieve_response(self, user_input):
        print(f"The user input was: {user_input}")
        response = "The response is:" + user_input.upper()
        return response
    
            
    def initialize_folders(self):
        # Get the folder paths from environment variables
        image_output_dir = os.getenv("IMAGE_OUTPUT_DIR")
        input_files = os.getenv("INPUT_FILES")

        # Function to check and create directories if they don't exist
        def create_directory(folder_path):
            path = Path(folder_path)
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)  # Creates directories and ignores if already exists
                print(f"Folder '{folder_path}' created.")
            else:
                print(f"Folder '{folder_path}' already exists.")

        # Create the folders using the paths from the .env file
        create_directory(image_output_dir)
        create_directory(input_files)


    if __name__ == "__main__":
        app.run(debug=True, port=8082)  # Run the Flask app with debugging enabled on
