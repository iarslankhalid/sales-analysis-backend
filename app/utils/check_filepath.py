from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve the FILE_PATH from the environment variable
filepath = os.getenv("FILE_PATH")

# Function to correct the path format (backslashes and forward slashes)
def change_path(path: str) -> str:
    # Ensure the correct path format for Windows (backslashes)
    path = path.replace("/", "\\")  # Convert forward slashes to backslashes
    path = path.replace("\\", "\\\\")  # Convert single backslashes to double backslashes
    return path


# Check if the path exists and open the file
try:
    if not filepath:
        raise ValueError("FILE_PATH environment variable is not set.")

    # Check if the given filepath exists and is accessible
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            # You can process the file here if needed
            print("File opened successfully.")
    else:
        # If the original path doesn't work, try the corrected path
        corrected_path = change_path(filepath)
        if os.path.exists(corrected_path):
            # Update the FILE_PATH variable with the corrected path in the environment
            os.environ["FILE_PATH"] = corrected_path  # Change the environment variable for the runtime
            # You might want to save the corrected path back to the .env file here
            print(f"File found with corrected path: {corrected_path}")
            with open(corrected_path, 'r') as f:
                # You can process the file here if needed
                print("File opened successfully with the corrected path.")
        else:
            raise ValueError("The given path in .env file is not correct, please change the path first.")
except Exception as e:
    print(f"Error: {str(e)}")
