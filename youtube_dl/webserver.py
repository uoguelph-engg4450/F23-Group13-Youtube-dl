from flask import Flask, url_for, render_template
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

    # Encoding the video filenames this step is crucial to confirming data integrity. Essentially if this fails the data will not be posted on the webserver and the user knows that they will have a missing video
    
    encode_vids = [url_for('video', filename = video) for video in video_data_list]    

    # This will render the new homepage for the app.
    
    return render_template('homepage.html', videos_to_display = zip(video_data_list, encode_vids))

