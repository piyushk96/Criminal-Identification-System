from tkinter import *
from PIL import Image
from PIL import ImageTk
from facerec import *

active_page = 0
video_loop = False

root = Tk()
root.configure(background = '#202d42')
root.geometry("1500x900")

pages = []
for i in range(4):
    pages.append(Frame(root, bg="#202d42"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)

back_button = PhotoImage(file="previous.png")

def goBack():
    global video_loop, active_page

    print(pages[active_page].winfo_children())
    for widget in pages[active_page].winfo_children():
        widget.destroy()

    pages[0].lift()
    video_loop = False
    active_page = 0

## Register Page ##
def getPage1():
    global active_page
    active_page = 1
    pages[1].lift()
    Button(pages[1], image=back_button, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack).place(x=10, y=10)
    Label(pages[1], text="Register Criminal", fg="white", bg="#202d42",
          font="Arial 20 bold", pady=10).pack()

## Detection Page ##
def getPage2():
    global active_page
    active_page = 2
    pages[2].lift()
    Button(pages[2], image=back_button, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack).place(x=10, y=10)
    Label(pages[2], text="Detect Criminal", fg="white", bg="#202d42",
      font="Arial 20 bold", pady=10).pack()

## video surveillance Page ##
def getPage3():
    global active_page, video_loop
    active_page = 3
    pages[3].lift()

    Button(pages[3], image=back_button, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack).place(x=10, y=10)
    Label(pages[3], text="Video Surveillance", fg="white", bg="#202d42",
          font="Arial 20 bold", pady=10).pack()

    content = Frame(pages[3], bg="pink", pady=100)
    content.pack(expand="true", fill="y")

    video_frame = Frame(content, bg="red", width=600, height=600, padx=50)
    video_frame.grid(row=0, column=0, sticky="NW")

    output = Frame(content, bg="yellow", width=600, height=600, padx=50)
    output.grid(row=0, column=1, sticky="NE")

    (model, names) = train_model()
    print('Training Successful. Detecting Faces')

    video_loop = True
    webcam = cv2.VideoCapture(0)

    while video_loop == True:
        # Loop until the camera is working
        while (True):
            # Put the image from the webcam into 'frame'
            (return_val, frame) = webcam.read()
            if (return_val == True):
                break
            else:
                print("Failed to open webcam. Trying again...")

        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_coords = detect_faces(gray_frame)


        ###########recognize        OpenCV=BGR  PIL=RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        vid = Label(video_frame, image=img)
        vid.image = img
        vid.pack(fill="both", expand=1)


    webcam.release()


######################################## Home Page ####################################
Label(pages[0], text="Criminal Identification System", fg="white", bg="#202d42",
      font="Arial 35 bold", pady=30).pack()

logo = PhotoImage(file = "logo.png")
Label(pages[0], image=logo, bg="#202d42").pack()


btn_frame = Frame(pages[0], bg="#202d42", pady=30)
btn_frame.pack()

Button(btn_frame, text="Register Criminal", command=getPage1)
Button(btn_frame, text="Detect Criminal", command=getPage2)
Button(btn_frame, text="Video Surveillance", command=getPage3)

for btn in btn_frame.winfo_children():
    btn.configure(font="Arial 20", width=17, bg="#2ea3ef", fg="white",
        pady=15, bd=0, highlightthickness=0, activebackground="#091428", activeforeground="white")
    btn.pack(pady=30)




pages[0].lift()
root.mainloop()