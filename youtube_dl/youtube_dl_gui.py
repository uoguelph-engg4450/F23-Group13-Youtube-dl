import customtkinter as ctk
import subprocess
import threading
import re
import tkinter as tk
import json  # For parsing JSON data


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

def update_progress(value):
    progress_bar.set(value)
    percentage_label.configure(text=f"{value}%")

def capture_errors(command):
    try:
        # Run the command and capture the standard output and errors
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        # Return standard output and errors in case of an exception
        return e.stdout, e.stderr

# Function to download video
def download_video():
    url = url_entry.get()
    url_list = url.split()   #incase if the user enter mulitple urls
    
    N_sec = duration_entry.get()
    format_option = format_var.get()
    if url: 
        update_progress(0)
        command = ["python", "__main__.py", "-f", format_option]
        for url in url_list:
            command.append(url)
        textbox.insert("0.0", command)
        if N_sec:
            duration = f'-to {N_sec}'
            command.extend(["--external-downloader", "ffmpeg", "--external-downloader-args"])
            command.append(duration)
            progress.set("Downloading...")
        else:
            progress.set("Downloading...")

        def run_command():
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
            for line in process.stdout:
                print(line)
                match = re.search(r'\b(\d{1,3})\.\d%\b', line)
                if match:
                    app.after(0, update_progress, float(match.group(1)))
            
            output, errors = capture_errors(command)
            if errors:
                progress.set("Enter the Correct Link")
                textbox.delete("1.0", tk.END)
                textbox.insert(tk.END, errors)
            else:
                progress.set("Downloaded")
                app.after(0, update_progress, 100.0)
                textbox.delete("1.0", tk.END)
                textbox.insert("0.0", "Click the following link to confirm downloads through the webserver: http://127.0.0.1:5000 \n")
        # Run the youtube-dl command in a separate thread to prevent the GUI from freezing
        threading.Thread(target=run_command).start()

    else:
        progress.set("Please enter a URL")
        app.after(0, update_progress, 0)
    
def toggle_duration():
    if checkbox_state.get():
       duration_entry.configure(state ="normal")
    else:
        duration_entry.configure(state ="disable")


# Creating the main window
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry(f"{1100}x{500}")

#configure grid Layout
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure((2, 3), weight=0)
app.grid_rowconfigure((0, 1, 2), weight=0)
app.grid_rowconfigure((5, 6), weight=1)

#creating sidebar
sidebar_frame = ctk.CTkFrame(app, width=140, corner_radius=0)
sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
sidebar_frame.grid_rowconfigure(4, weight=1)
logo_label = ctk.CTkLabel(sidebar_frame, text="YouTube Downloader", font=ctk.CTkFont(size=20, weight="bold"))
logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

# Format Options
format_label = ctk.CTkLabel(sidebar_frame, text="Select Format:", anchor="center")
format_label.grid(row=1, column=0, padx=20, pady=(10,0))
format_options = ["best", "mp4", "webm"]  # Add more formats as needed
format_var = ctk.StringVar(value=format_options[0])  # default value
format_dropdown = ctk.CTkOptionMenu(sidebar_frame, variable=format_var, values=format_options)
format_dropdown.grid(row=2, column=0, padx=20, pady=(10,0))



#URL entry
url_label = ctk.CTkLabel(app, text="Enter Video URL:", font=ctk.CTkFont(size=20))
url_label.grid(row=0, column =1, padx=0, pady=(10,0))
url_entry = ctk.CTkEntry(app, placeholder_text="Enter URL Here...")
url_entry.grid(row=2, column =1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

#download Button
download_button = ctk.CTkButton(app, text="Download", command=download_video, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
download_button.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

#Progress bar
progress_bar = ctk.CTkProgressBar(app, width=450)
progress_bar.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="n")
#Progress percentage
percentage_label = ctk.CTkLabel(app, text="0%")
percentage_label.grid(row=3, column=2, padx=(20, 20), pady=(20, 0), sticky="n")

#Downloading Text
progress = ctk.StringVar()
progress.set("Enter a video URL and click download")
progress_display = ctk.CTkLabel(app, textvariable=progress)
progress_display.grid(row=4, column=1, padx=(0, 0), pady=(20, 20), sticky="nsew")

#N sec 
checkbox_state = tk.BooleanVar(value=False)
duration_check = ctk.CTkCheckBox(sidebar_frame, text="Download N sec, Enter below:", command=toggle_duration, variable=checkbox_state)
duration_check.grid(row=3, column=0, padx=0, pady=(50,0), sticky="s")

duration_entry = ctk.CTkEntry(sidebar_frame, state="disabled", placeholder_text="Enter")
duration_entry.grid(row=4, column=0, padx=20, pady=15)


#TextBox
textbox = ctk.CTkTextbox(app)
textbox.grid(row=6, column=1, columnspan=2, padx=5, pady=20, sticky="nsew")

progress_bar.set(0)
percentage_label.configure(text="0%")

# Run the app
app.mainloop()
