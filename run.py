import subprocess

def run_streamlit():
    # Command to run Streamlit with the main.py script
    command = ["streamlit", "run", "main.py"]

    try:
        # Running the command
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to run Streamlit: {e}")

if __name__ == "__main__":
    run_streamlit()
