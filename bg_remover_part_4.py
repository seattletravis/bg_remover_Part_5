from rembg import remove
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import threading

  
def stop_tool():
  stop_event.set()
  # run_batch_removal_tool_button.configure(text="Run Background Removal Tool", command=threading.Thread(target=run_batch_removal_tool).start) 


def select_app_info():
  if named_directory_out.get() == '' and named_directory_in.get() == '':
    app_info.set("PLEASE SELECT PATH IN & PATH OUT")
  elif named_directory_in.get() == '':
    app_info.set("PLEASE SELECT PATH IN")
  elif named_directory_out.get() == '':
    app_info.set("PLEASE SELECT PATH OUT")
  elif named_directory_in.get() == named_directory_out.get():
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
  run_batch_removal_tool_button.configure(text="Stop Background Removal Tool", command=stop_tool)
  pic_list = os.listdir(named_directory_in.get())
  app_info.set("PROCESSING")

  #Loop over all Images
  for pic in pic_list:
    if stop_event.is_set():
      break
    
    input_path = fr'{named_directory_in.get()}\{pic}'
    
    # Store path of the output image in the variable output_path
    output_path = fr'{named_directory_out.get()}\{pic}'

    # Check if image exists
    if os.path.exists(output_path):
        continue
    
    # Processing the image
    input = Image.open(input_path)

    # Removing the background from the given Image
    output = remove(input)

    #Saving the image in the given path
    output.save(output_path)  
    
  app_info.set("PROCESS STOPPED" if pic_list else "FOLDER IS EMPTY")
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
app_info = tk.StringVar(root, "")
select_app_info()


root.geometry("640x275")
root.title("UNCHA - Batch Background Removal Tool")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)


#GUI Title
ttk.Label(root, text="Uncha - Batch Background Removal Tool", padding=(30, 30)).grid(row=0, column=1)

#File in Button and Label
choose_path_in_button = ttk.Button(root, text="Choose Input Path", command=get_path_in).grid(pady=2, row=1, column=0, sticky="EW")
ttk.Label(root, textvariable=named_directory_in, relief="sunken").grid(row=1, column=1, sticky="EW")
set_default_in_button = ttk.Button(root, text="Set as Default", command=set_default_in).grid(row=1, column=2)

#File out Button and Label
choose_path_out_button = ttk.Button(root, text="Choose Output Path", command=get_path_out).grid(row=2, column=0, sticky="EW")
ttk.Label(root, textvariable=named_directory_out, relief="sunken").grid(row=2, column=1, sticky="EW")
set_default_out_button = ttk.Button(root, text="Set as Default", command=set_default_out).grid(row=2, column=2)

#define event
stop_event = threading.Event()

#Run Tool Button
run_batch_removal_tool_button = ttk.Button(root, text="Run Background Romoval Tool", command=threading.Thread(target=run_batch_removal_tool).start)
run_batch_removal_tool_button.grid(row=3, column=1, pady=10)

#Quit out of Application
quit_button = ttk.Button(root, text="Quit", command=root.destroy).grid(row=4, column=1)

#Application Information
information = ttk.Label(root, textvariable=app_info).grid(pady=10, row=5, column=1)

root.mainloop()