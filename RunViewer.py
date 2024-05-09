import customtkinter as tk
import tkinter.filedialog as fd
import os
import json

app = tk.CTk()
app.title("Run data viewer")

def loadsave(filename):
    file = open(f"C:/Program Files (x86)/Steam/steamapps/common/The Binding of Isaac Rebirth/data/tboi mod/{filename}", encoding="utf-8")
    savedata = json.load(file)
    file.close()
    saves_frame.grid_remove()
    loadinfopage(savedata)

def loadfile():
    file = fd.askopenfile(mode="r", filetypes=[("DAT files", "*.dat")])
    savedata = json.load(file)
    print(savedata)
    file.close()
    saves_frame.grid_remove()
    loadinfopage(savedata)

saves_frame = tk.CTkFrame(app, width=500, height=500)
saves_frame.grid(row=0, column=0, padx=20, pady=20)
saves_frame.pack_propagate(False)
tk.CTkLabel(saves_frame, text="Select a save file\nfrom your TBoI folder", font=("Arial", 30)).pack(pady=15, side="top")
tk.CTkButton(saves_frame, text="Browse", command=loadfile, width=200, height=35).pack(pady=20, side="bottom") 
tk.CTkLabel(saves_frame, text="Or pick a save file from your computer", font=("Arial", 20)).pack(pady=5, side="bottom")

for i in os.listdir("C:/Program Files (x86)/Steam/steamapps/common/The Binding of Isaac Rebirth/data/tboi mod"):
    button_event = lambda i=i: loadsave(i)
    button = tk.CTkButton(saves_frame, text=i, command=button_event ,width=200, height=35)
    button.pack()

scroll_frame = tk.CTkScrollableFrame(app, width=200, height=500)
info_frame = tk.CTkFrame(app, width=500, height=500)
infotitle = tk.CTkLabel(info_frame, text="Info", font=("Arial", 30))
infotext = tk.CTkLabel(info_frame, text="", font=("Arial", 22), anchor="w", justify="left")
tempscroll_frame = tk.CTkFrame(app, width=200, height=500)
progress_frame = tk.CTkFrame(info_frame, width=500, height=500)
progressbar = tk.CTkProgressBar(progress_frame, mode='determinate')
progresstext1 = tk.CTkLabel(progress_frame, text="0%", anchor="w")
progresstext2 = tk.CTkLabel(progress_frame, text="0/0", anchor="e")
#{"bosscount":0,"roomsentered":2,"floor":"Basement I","runid":2,"exited":false,"totalruntime":56587,"enemyCount":6,"diedEnding":true,"dateended":"20240508130847"}
def loadinfo(index, savedata):
    if index == 3:
        reloadsave()
    infotitle.configure(text=f"Run #{index} stats")
    if savedata[index-1]["exited"]:
        ended = "Exited the run"
    elif savedata[index-1]["diedEnding"]:
        ended = "Died"
    elif savedata[index-1]["exited"] == False and savedata[index-1]["diedEnding"] == False:
        ended = "Finished the run"
    keys = ["totalruntime", "enemyCount", "bosscount", "roomsentered", "floor", "dateended", "datestarted"]
    values = {}
    for key in keys:
        values[key] = savedata[index-1].get(key, "Not available")
    text = f"Runtime: {converttime(values["totalruntime"])}\n\nEnemies killed: {values["enemyCount"]}\n\nBosses killed: {values["bosscount"]}\n\nRooms entered: {values["roomsentered"]}\n\nLast floor: {values["floor"]}\n\nStarted: {convertdate(values["datestarted"])}\n\nEnded: {convertdate(values["dateended"])}\n\nEnding: {ended}"
    infotext.configure(text=text)
    print(index)

def reloadsave():
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    loadfile()

def convertdate(date):
    if date == "Not available":
        return date
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    hour = date[8:10]
    minute = date[10:12]
    second = date[12:14]
    return f"{day}/{month}/{year} {hour}:{minute}:{second}"

def converttime(ms):
    ms = int(ms)
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    return f"{hours}h {minutes%60}m {seconds%60}s"

def loadinfopage(savedata):
    info_frame.grid(row=0, column=1, padx=20, pady=20)
    info_frame.grid_propagate(False)

    tempscroll_frame.grid(row=0, column=0, padx=20, pady=20)
    scroll_frame.grid_remove()
    progress_frame.place(relx=0.5, rely=0.5, anchor="center", )

    progressbar.grid(row=0, column=0, sticky='ew')

    progresstext1.grid(row=1, column=0, sticky='w')
    progresstext2.grid(row=1, column=0, sticky='e')

    app.update()
    for i in range(len(savedata)):
        i += 1
        if "datestarted" in savedata[i-1]:
            buttontime = "- " + convertdate(savedata[i-1]["datestarted"])[0:10] + " " + converttime(savedata[i-1]["totalruntime"])
        else:
            buttontime = "- " + converttime(savedata[i-1]["totalruntime"])
        button_event = lambda i=i: loadinfo(i, savedata)
        button = tk.CTkButton(scroll_frame, text=f"Run {i} {buttontime}", command=button_event, width=200, height=35)
        button.pack()

        progressbar.set(i / len(savedata))
        progresstext1.configure(text=f"{round(i*100/len(savedata))}%")
        progresstext2.configure(text=f"{i}/{len(savedata)}")
        app.update_idletasks()

    scroll_frame.grid(row=0, column=0, padx=20, pady=20)
    infotitle.place(relx=0.5, rely=0.05, anchor="n")
    infotext.place(relx=0.05, rely=0.5, anchor="w")

    tempscroll_frame.grid_remove()
    progress_frame.place_forget()

app.mainloop()
