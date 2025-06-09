import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Run the streamlit app
if __name__ == "__main__":
    os.system("streamlit run app.py")