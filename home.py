from tkinter import *

root = Tk()
root.configure(background = '#202d42')
root.geometry("1200x1000")

Label(root, text="Criminal Identification System", fg="white", bg="#202d42",
      font="Arial 35 bold", pady=30).pack()

# img_frame = Frame(root)
# img_frame.pack()
logo = PhotoImage(file = "logo.png")
Label(root, image=logo, bg="#202d42").pack()

# content = Frame(root, bg="#202d42",height=800)
# content.pack(fill=X)

btn_frame = Frame(root, bg="#202d42", pady=30)
btn_frame.pack()

Button(btn_frame, text="Register Criminal")
Button(btn_frame, text="Detect Criminal")
Button(btn_frame, text="Video Surveillance")

for wid in btn_frame.winfo_children():
    wid.configure(font="Arial 20", width=17, bg="#2ea3ef", fg="white",
        pady=15, bd=0, highlightthickness=0, activebackground="#091428", activeforeground="white")
    wid.pack(pady=30)


root.mainloop()