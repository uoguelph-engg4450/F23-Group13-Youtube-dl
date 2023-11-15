from flask import Flask, url_for, render_template, send_from_directory
import os

# Intiialze Flask object will be used late to run the webserver this object is used by flask to run the webserver.

app = Flask(__name__)

# Collect the path to the directory where this python webserver script is located in order to collect the video data as it will also be downloaded here.

script_dir = os.path.dirname(os.path.realpath(__file__))

# The homepage where all the vidoe's will appear will be given a flask route to host the webpage this will be the only page on the server.

@app.route('/')

def homepage():
    directory_video_stored = script_dir
    # Collect all the videos into a list from the same file direcotry after the program downloads each of them.
     
    videos = [video for video in os.listdir(directory_video_stored) if video.endswith(('.mp4', '.webm', '.mkv'))]

    # Encoding the video filenames this step is crucial to confirming data integrity. Essentially if this fails the data will not be posted on the webserver and the user knows that they will have a missing video
    
    encoded_videos = [url_for('video', filename=video) for video in videos]

    # This will render the new homepage for the app.
    
    return render_template('homepage.html', videos=zip(videos, encoded_videos))

# Collect the route to each video also each video is stored in the same directory so send each video from there.
@app.route('/video/<filename>')

def video(filename):
    directory_video_stored = script_dir
    return send_from_directory(directory_video_stored, filename)

# Run the program since this is not the main that will be run this is never reached which is fine, it was used during debugging but is not used in original program.
# if __name__ == '__main__':
#     app.run(debug = False)