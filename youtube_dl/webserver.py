from flask import Flask
import os

# Intiialze Flask object will be used late to run the webserver this object is used by flask to run the webserver.

app = Flask(__name__)

# Collect the path to the directory where this python webserver script is located in order to collect the video data as it will also be downloaded here.

directory_of_script = os.path.dirname(os.path.realpath(__file__))

# The homepage where all the vidoe's will appear will be given a flask route to host the webpage this will be the only page on the server.

@app.route('/')

def homepage():
    
    # Collect all the videos into a list from the same file direcotry after the program downloads each of them.
     
    video_data_list = [video for video in os.listdir(directory_of_script) if video.endswith(('.mp4', '.webm', '.mkv'))]

    
