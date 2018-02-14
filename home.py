from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import threading
from facerec import *

active_page = 0
thread_event = None
left_frame = None
right_frame = None
webcam = None
img_label = None
img_read = None

root = Tk()
root.configure(background = '#202d42')
root.geometry("1500x900")

# create Pages
pages = []
for i in range(4):
    pages.append(Frame(root, bg="#202d42"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)

back_button = PhotoImage(file="previous.png")

def goBack():
    global active_page, thread_event, webcam

    if (active_page==3 and not thread_event.is_set()):
        thread_event.set()
        webcam.release()

    for widget in pages[active_page].winfo_children():
        widget.destroy()

    pages[0].lift()
    active_page = 0

def showImage(frame, img_size):
    global img_label, left_frame

    img = cv2.resize(frame, (img_size, img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    if (img_label == None):
        img_label = Label(left_frame, image=img, bg="#202d42")
        img_label.image = img
        img_label.pack(expand=True, fill="both", padx=20)
    else:
        img_label.configure(image=img)
        img_label.image = img


## Register Page ##
def getPage1():
    global active_page
    active_page = 1
    pages[1].lift()
    Button(pages[1], image=back_button, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack).place(x=10, y=10)
    Label(pages[1], text="Register Criminal", fg="white", bg="#202d42",
          font="Arial 20 bold", pady=10).pack()


def startRecognition():
    global img_read, img_label

    if(img_label == None):
        messagebox.showerror("Error", "No image selected. ")
        return

    # frame = img_read
    crims_found_labels = []
    for wid in right_frame.winfo_children():
        wid.destroy()

    frame = cv2.flip(img_read, 1, 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_coords = detect_faces(gray_frame)

    if (len(face_coords) != 0):
        (model, names) = train_model()
        print('Training Successful. Detecting Faces')
        (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

        for i in range(len(recognized)):
            crims_found_labels.append(Label(right_frame, text=recognized[i][0], bg="orange",
                                            font="Arial 15 bold", pady=20))
            crims_found_labels[i].pack(fill="x", padx=20, pady=10)

    img_size = left_frame.winfo_height() - 40

    frame = cv2.flip(frame, 1, 0)
    showImage(frame, img_size)

    if(len(face_coords) == 0):
        messagebox.showerror("Error", "Image doesn't contain any face or face is too small.")
    elif(len(recognized) == 0):
        messagebox.showerror("Error", "No criminal recognized.")


def selectImage():
    global left_frame, img_label, img_read
    for wid in right_frame.winfo_children():
        wid.destroy()

    path = filedialog.askopenfilename(title="Choose a image")
    if len(path) > 0:
        if(path.split(".")[-1].lower() not in ['png','jpg','jpeg','gif','pgm']):
            messagebox.showerror("Error", "Selected file is not an image. ")
            return

        img_read = cv2.imread(path)

        img_size =  left_frame.winfo_height() - 40
        showImage(img_read, img_size)


## Detection Page ##
def getPage2():
    global active_page, left_frame, right_frame, img_label
    img_label = None
    active_page = 2
    pages[2].lift()
    Button(pages[2], image=back_button, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack).place(x=10, y=10)
    Label(pages[2], text="Detect Criminal", fg="white", bg="#202d42",
      font="Arial 20 bold", pady=10).pack()

    content = Frame(pages[2], bg="#202d42", pady=50)
    content.pack(expand="true", fill="both")

    left_frame = Frame(content, bg="#202d42")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,
                             foreground="#2ea3ef", labelanchor=N)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)

    btn_grid = Frame(left_frame, bg="#202d42")
    btn_grid.pack()

    Button(btn_grid, text="Select Image", command=selectImage, font="Arial 15 bold", width=15, bg="#2ea3ef",
            fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
            activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    Button(btn_grid, text="Recognize", command=startRecognition, font="Arial 15 bold", width=10, bg="#2ea3ef",
           fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").grid(row=0, column=1, padx=25, pady=25)


def videoLoop(model, names):
    global thread_event, left_frame, webcam, img_label
    webcam = cv2.VideoCapture(0)
    old_recognized = []
    crims_found_labels = []
    img_label = None

    try:
        while not thread_event.is_set():
            # Loop until the camera is working
            while (True):
                # Put the image from the webcam into 'frame'
                (return_val, frame) = webcam.read()
                if (return_val == True):
                    break
                else:
                    print("Failed to open webcam. Trying again...")

            # Flip the image (optional)
            frame = cv2.flip(frame, 1, 0)
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect Faces
            face_coords = detect_faces(gray_frame)
            (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

            # Recognize Faces
            recog_names = [item[0] for item in recognized]
            if(recog_names != old_recognized):
                for wid in right_frame.winfo_children():
                    wid.destroy()
                del(crims_found_labels[:])

                for i in range(len(recognized)):
                    crims_found_labels.append(Label(right_frame, text=recognized[i][0], bg="orange",
                                                    font="Arial 15 bold", pady=20))
                    crims_found_labels[i].pack(fill="x", padx=20, pady=10)

                old_recognized = recog_names

            # Display Video stream
            img_size = min(left_frame.winfo_width(), left_frame.winfo_height()) - 20

            showImage(frame, img_size)

    except RuntimeError:
        print("[INFO]Caught Runtime Error")
    except TclError:
        print("[INFO]Caught Tcl Error")


## video surveillance Page ##
def getPage3():
    global active_page, video_loop, left_frame, right_frame, thread_event
    active_page = 3
    pages[3].lift()

    Button(pages[3], image=back_button, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack).place(x=10, y=10)
    Label(pages[3], text="Video Surveillance", fg="white", bg="#202d42",
          font="Arial 20 bold", pady=10).pack()

    content = Frame(pages[3], bg="#202d42", pady=50)
    content.pack(expand="true", fill="both")

    left_frame = Frame(content, bg="#202d42", pady=20)
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,
                             foreground="#2ea3ef", labelanchor=N)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)

    (model, names) = train_model()
    print('Training Successful. Detecting Faces')

    thread_event = threading.Event()
    thread = threading.Thread(target=videoLoop, args=(model, names))
    thread.start()




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