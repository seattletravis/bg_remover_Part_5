# Uncha - by Travis Lamberte & YouTube Video Tutorial Part 5

## [2 Minute Video Demonstration](https://youtu.be/wbjmltaJSnk?si=5yTFNpAzOgBgU7Dy)

# Batch background removal tool with GUI

Uncha is a Windows Application for removing all image backgrounds from images located in a specified folder and saving those transparent image files to another file folder also specified by the user. This is an opensource project and all the source code is here to use. GUI is written using tkinter and backgrounds are removed using rembg.

Run bg_remover_with_GUI, then select both folders using the GUI navigation.

## [Video Tutorial!](https://youtu.be/qfmpTftg2bY)

In this video tutorial we add the progress bar and some error handling! Watch this video to see the code in action, or if you have issues running it, or if you want to learn how it was written. This is a coding tutorial video. [Video Link](https://youtu.be/qfmpTftg2bY)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rembg, Pillow, and Tkinter.

```bash
pip install rembg
```

```bash
pip install Pillow
```

```bash
pip install tk
```


## See all the code here
```python
from rembg import remove
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading 


def stop_tool():
  stop_event.set()

def select_app_info():
  if named_directory_in.get() == '' and named_directory_out.get() == '':
    app_info.set("PLEASE SELECT PATH IN & PATH OUT")
  elif named_directory_in.get() == '':
    app_info.set("PLEASE SELECT PATH IN")
  elif named_directory_out.get() == '':
    app_info.set("PLEASE SELECT PATH OUT")
  elif named_directory_out.get() == named_directory_in.get():
    app_info.set("WARNING: PATH OUT CANNOT BE THE SAME AS PATH IN")
  else:
    app_info.set("PATH IN & PATH OUT ACCEPTED")
    
def set_default_in():
  with open("default_in.txt", "w") as file:
    file.write(named_directory_in.get())

def set_default_out():
  with open("default_out.txt", "w") as file:
    file.write(named_directory_out.get())

def get_path_in():
  named_directory_in.set(filedialog.askdirectory())
  select_app_info()

def get_path_out():
  named_directory_out.set(filedialog.askdirectory())
  select_app_info()

def run_batch_removal_tool():
  total_items = 0
  image_processed_count = 0
  nonimage_count = 0
  already_processed_count = 0
  
  already_processed.set(f"Images already processed, skipped: {already_processed_count}")
  image_processed.set(f"Images processed: {image_processed_count}")
  nonimage.set(f"Not an image file, skipped: {nonimage_count}")
  
  run_batch_removal_tool_button.configure(text="Stop Background Removal Tool", command=stop_tool)
  pic_list = os.listdir(named_directory_in.get())
  app_info.set("PROCESSING")

  #Loop over all Images
  for pic in pic_list:
    total_items = image_processed_count + nonimage_count + already_processed_count
    processing_status.set(f"Processing: {total_items} files of {len(pic_list)} total files in folder")
    if stop_event.is_set():
      break
    input_path = fr'{named_directory_in.get()}\{pic}'
    
    # Store path of the output image in the variable output_path
    output_path = fr'{named_directory_out.get()}\{pic}'

    # Check if image exists
    if os.path.exists(output_path):
      already_processed_count += 1
      already_processed.set(f"Images already processed, skipped: {already_processed_count}")
      continue
    
    try:
      # Processing the image, open, remove bg, save image to out path
      input = Image.open(input_path)
      output = remove(input)
      output.save(output_path)
      image_processed_count += 1
      image_processed.set(f"Images processed: {image_processed_count}")
    except:
      nonimage_count += 1
      nonimage.set(f"Not an image file, skipped: {nonimage_count}")
      
    
    
  app_info.set("PROCESS REPORT" if pic_list else "FOLDER IS EMPTY")
  if stop_event.is_set() == False:
    total_items += 1
    processing_status.set(f"Processing: {total_items} files of {len(pic_list)} total files in folder")
    
    
  processing_status.set(f"Processed: {total_items} files of {len(pic_list)} total files in folder")
  image_thread = threading.Thread(target=run_batch_removal_tool) 
  run_batch_removal_tool_button.configure(text="Run Background Removal Tool", command=image_thread.start) 
  stop_event.clear()


root = tk.Tk()

with open("default_in.txt", "r") as file:
  saved_default_in = file.read()
    
with open("default_out.txt", "r") as file:
  saved_default_out = file.read()

named_directory_in = tk.StringVar(root, saved_default_in)
named_directory_out = tk.StringVar(root, saved_default_out)
app_info = tk.StringVar(root)
select_app_info()

processing_status = tk.StringVar(root)
image_processed = tk.StringVar(root)
nonimage = tk.StringVar(root)
already_processed = tk.StringVar(root)


root.geometry("640x400")
root.title("UNCHA - Batch Background Removal Tool")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

stop_event = threading.Event()

#GUI Title
ttk.Label(root, text="Uncha - Batch Background Removal Tool", padding=(30, 30)).grid(row=0, column=1)

#File In Button and Info Lable
choose_path_in_button = ttk.Button(root, text="Choose Input Path", command=get_path_in).grid(row=1, column=0, sticky="EW")
ttk.Label(root, textvariable=named_directory_in, relief="sunken").grid(row=1, column=1, sticky="EW")
set_default_out_button = ttk.Button(root, text="Set as Default", command=set_default_in).grid(row=1, column=2)

#File Out Button and Info Lable
choose_path_out_button = ttk.Button(root, text="Choose Output Path", command=get_path_out).grid(row=2, column=0, sticky="EW")
ttk.Label(root, textvariable=named_directory_out, relief="sunken").grid(row=2, column=1, sticky="EW")
set_default_out_button = ttk.Button(root, text="Set as Default", command=set_default_out).grid(row=2, column=2)

#Run Tool Button
run_batch_removal_tool_button = ttk.Button(root, text="Start background Removal Tool", command=threading.Thread(target=run_batch_removal_tool).start)
run_batch_removal_tool_button.grid(row=3, column=1, pady=10)

#Quit GUI and process Button
quit_button = ttk.Button(root, text="Quit", command=root.destroy).grid(row=4, column=1)

information = ttk.Label(root, textvariable=app_info).grid(row=5, column=1, pady=10)

processing_line_1 = ttk.Label(root, textvariable=processing_status).grid(pady=6, row=6, column=1)
processing_line_1 = ttk.Label(root, textvariable=image_processed).grid(row=7, column=1)
processing_line_1 = ttk.Label(root, textvariable=already_processed).grid(row=8, column=1)
processing_line_1 = ttk.Label(root, textvariable=nonimage).grid(row=9, column=1)


root.mainloop()

```
