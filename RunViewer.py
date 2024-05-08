import customtkinter as tk
import os
import json
os.chdir("Proge-stuff/python")
fail = open("save1.dat", encoding="utf-8")
jarjend = json.load(fail)
fail.close()

app = tk.CTk()
app.title("Run data viewer")

scroll_frame = tk.CTkScrollableFrame(app, width=200, height=500)

info_frame = tk.CTkFrame(app, width=500, height=500)
info_frame.grid(row=0, column=1, padx=20, pady=20)
info_frame.grid_propagate(False)

infotitle = tk.CTkLabel(info_frame, text="Info", font=("Arial", 30))
infotext = tk.CTkLabel(info_frame, text="", font=("Arial", 22), anchor="w", justify="left")

tempscroll_frame = tk.CTkFrame(app, width=200, height=500)
tempscroll_frame.grid(row=0, column=0, padx=20, pady=20)

progress_frame = tk.CTkFrame(info_frame, width=500, height=500)
progress_frame.place(relx=0.5, rely=0.5, anchor="center", )

progressbar = tk.CTkProgressBar(progress_frame, mode='determinate')
progressbar.grid(row=0, column=0, sticky='ew')

progresstext1 = tk.CTkLabel(progress_frame, text="0%", anchor="w")
progresstext2 = tk.CTkLabel(progress_frame, text="0/0", anchor="e")
progresstext1.grid(row=1, column=0, sticky='w')
progresstext2.grid(row=1, column=0, sticky='e')

def loadinfo(index):
    infotitle.configure(text=f"Run nr. {index} stats")
    runtime = jarjend[index-1]["totalruntime"]
    enemycount = jarjend[index-1]["enemyCount"]
    bosscount = jarjend[index-1]["bosscount"]
    roomsentered = jarjend[index-1]["roomsentered"]
    if jarjend[index-1]["exited"]:
        ended = "Exited the run"
    elif jarjend[index-1]["diedEnding"]:
        ended = "Died"
    text = f"Runtime: {converttime(runtime)}\n\nEnemies killed: {enemycount}\n\nBosses killed: {bosscount}\n\nRooms entered: {roomsentered}\n\n{ended}"
    infotext.configure(text=text)
    print(index)

def converttime(ms):
    ms = int(ms)
    seconds = ms // 1000
    minutes = seconds // 60
    hours = minutes // 60
    return f"{hours}h {minutes%60}m {seconds%60}s"

app.update()

for i in range(len(jarjend)):
    i += 1
    button_event = lambda i=i: loadinfo(i)
    button = tk.CTkButton(scroll_frame, text=f"Run {i}", command=button_event, width=200, height=35)
    button.pack()

    progressbar.set(i / len(jarjend))
    progresstext1.configure(text=f"{round(i*100/len(jarjend))}%")
    progresstext2.configure(text=f"{i}/{len(jarjend)}")
    app.update_idletasks()

scroll_frame.grid(row=0, column=0, padx=20, pady=20)
infotitle.place(relx=0.5, rely=0.05, anchor="n")
infotext.place(relx=0.05, rely=0.5, anchor="w")

tempscroll_frame.grid_remove()
progress_frame.place_forget()

app.mainloop()
