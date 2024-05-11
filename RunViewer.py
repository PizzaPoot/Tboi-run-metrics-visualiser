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
    loadinfopage(savedata)

def loadfile():
    file = fd.askopenfile(mode="r", filetypes=[("DAT files", "*.dat")])
    savedata = json.load(file)
    file.close()
    loadinfopage(savedata)

def loaddefaultpage():
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    infotitle.configure(text="Run Viewer\nBy PizzaPoot", font=("Arial", 30))
    infotext.configure(text="Stupid ahh program\n\nIdk what tf to write here\n\nSome stupid shit XD")

scroll_frame = tk.CTkScrollableFrame(app, width=200, height=500)
info_frame = tk.CTkFrame(app, width=500, height=510)
infotitle = tk.CTkLabel(info_frame, text="", font=("Arial", 30))
infotext = tk.CTkLabel(info_frame, text="", font=("Arial", 22), anchor="w", justify="left")
tempscroll_frame = tk.CTkFrame(app, width=220, height=510)
progress_frame = tk.CTkFrame(info_frame, width=500, height=500)
progressbar = tk.CTkProgressBar(progress_frame, mode='determinate')
progresstext1 = tk.CTkLabel(progress_frame, text="0%", anchor="w")
progresstext2 = tk.CTkLabel(progress_frame, text="0/0", anchor="e")
buttons_frame = tk.CTkFrame(app, width=1000, height=50)
buttons_frame.grid(row=0, column=0, padx=20, pady=20, columnspan=2)
info_frame.grid(row=1, column=1, padx=20, pady=20, sticky="w")
info_frame.grid_propagate(False)
tempscroll_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")
infobutton = tk.CTkButton(buttons_frame, text="Info", command=loaddefaultpage, width=125, height=35)
infobutton.grid(padx=10, pady=15, row=0, column=0)
browsebutton = tk.CTkButton(buttons_frame, text="Browse", command=loadfile, width=125, height=35)
browsebutton.grid(padx=10, pady=15, row=0, column=1)
infotitle.place(relx=0.5, rely=0.05, anchor="n")
infotext.place(relx=0.05, rely=0.5, anchor="w")
loaddefaultpage()

for num, i in enumerate(os.listdir("C:/Program Files (x86)/Steam/steamapps/common/The Binding of Isaac Rebirth/data/tboi mod")):
    button_event = lambda i=i: loadsave(i)
    button = tk.CTkButton(buttons_frame, text=i, command=button_event ,width=125, height=35)
    button.grid(padx=10, pady=15, row=0, column=num+2)


def loadsaveinfo(index, savedata):
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
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    infotitle.configure(text="")
    infotext.configure(text="")

    scroll_frame.grid_remove()
    progress_frame.place(relx=0.5, rely=0.5, anchor="center", )
    tempscroll_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    progressbar.grid(row=1, column=0, sticky='ew')

    progresstext1.grid(row=1, column=0, sticky='w')
    progresstext2.grid(row=1, column=0, sticky='e')

    app.update()
    for i in range(len(savedata)):
        i += 1
        if "datestarted" in savedata[i-1]:
            buttontime = "- " + convertdate(savedata[i-1]["datestarted"])[0:10] + " " + converttime(savedata[i-1]["totalruntime"])
        else:
            buttontime = "- " + converttime(savedata[i-1]["totalruntime"])
        button_event = lambda i=i: loadsaveinfo(i, savedata)
        button = tk.CTkButton(scroll_frame, text=f"Run {i} {buttontime}", command=button_event, width=200, height=35)
        button.pack()

        progressbar.set(i / len(savedata))
        progresstext1.configure(text=f"{round(i*100/len(savedata))}%")
        progresstext2.configure(text=f"{i}/{len(savedata)}")
        app.update_idletasks()

    scroll_frame.grid(row=1, column=0, padx=20, pady=20, sticky="w")

    tempscroll_frame.grid_remove()
    progress_frame.place_forget()

app.mainloop()
