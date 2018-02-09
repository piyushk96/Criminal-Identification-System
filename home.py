from tkinter import *

root = Tk()
root.configure(background = '#202d42')
root.geometry("1200x1000")

pages = []
for i in range(4):
    pages.append(Frame(root, bg="#202d42"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)

######################################## Home Page ####################################
Label(pages[0], text="Criminal Identification System", fg="white", bg="#202d42",
      font="Arial 35 bold", pady=30).pack()

# img_frame = Frame(root)
# img_frame.pack()
logo = PhotoImage(file = "logo.png")
Label(pages[0], image=logo, bg="#202d42").pack()

# content = Frame(root, bg="#202d42",height=800)
# content.pack(fill=X)

btn_frame = Frame(pages[0], bg="#202d42", pady=30)
btn_frame.pack()

Button(btn_frame, text="Register Criminal", command=pages[1].lift)
Button(btn_frame, text="Detect Criminal", command=pages[2].lift)
Button(btn_frame, text="Video Surveillance", command=pages[3].lift)

for wid in btn_frame.winfo_children():
    wid.configure(font="Arial 20", width=17, bg="#2ea3ef", fg="white",
        pady=15, bd=0, highlightthickness=0, activebackground="#091428", activeforeground="white")
    wid.pack(pady=30)

######################################## Register Page ####################################
Label(pages[1], text="Register Criminal", fg="white", bg="#202d42",
      font="Arial 25 bold", pady=30).pack()

######################################## Detection Page ####################################
Label(pages[2], text="Detect Criminal", fg="white", bg="#202d42",
      font="Arial 25 bold", pady=30).pack()

######################################## video surveillance Page ####################################
Label(pages[3], text="Video Surveillance", fg="white", bg="#202d42",
      font="Arial 25 bold", pady=30).pack()




pages[0].lift()
root.mainloop()