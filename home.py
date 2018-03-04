from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import threading
from facerec import *
from register import *

active_page = 0
thread_event = None
left_frame = None
right_frame = None
heading = None
webcam = None
img_label = None
img_read = None
img_list = []
slide_caption = None
slide_control_panel = None
current_slide = -1

root = Tk()
# root.configure(background = '#202d42')
root.geometry("1500x900")

# create Pages
pages = []
for i in range(4):
    pages.append(Frame(root, bg="#202d42"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)


def goBack():
    global active_page, thread_event, webcam

    if (active_page==3 and not thread_event.is_set()):
        thread_event.set()
        webcam.release()

    for widget in pages[active_page].winfo_children():
        widget.destroy()

    pages[0].lift()
    active_page = 0


def basicPageSetup(pageNo):
    global left_frame, right_frame, heading

    back_img = PhotoImage(file="back.png")
    back_button = Button(pages[pageNo], image=back_img, bg="#202d42", bd=0, highlightthickness=0,
           activebackground="#202d42", command=goBack)
    back_button.image = back_img
    back_button.place(x=10, y=10)

    heading = Label(pages[pageNo], fg="white", bg="#202d42", font="Arial 20 bold", pady=10)
    heading.pack()

    content = Frame(pages[pageNo], bg="#202d42", pady=20)
    content.pack(expand="true", fill="both")

    left_frame = Frame(content, bg="#202d42")
    left_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,
                             foreground="#2ea3ef", labelanchor=N)
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)


def showImage(frame, img_size):
    global img_label, left_frame

    img = cv2.resize(frame, (img_size, img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    if (img_label == None):
        img_label = Label(left_frame, image=img, bg="#202d42")
        img_label.image = img
        img_label.pack(padx=20)
    else:
        img_label.configure(image=img)
        img_label.image = img


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

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path = filedialog.askopenfilename(title="Choose a image", filetypes=filetype)

    if(len(path) > 0):
        img_read = cv2.imread(path)

        img_size =  left_frame.winfo_height() - 40
        showImage(img_read, img_size)


def getNewSlide(control):
    global img_list, current_slide

    if(len(img_list) > 1):
        if(control == "prev"):
            current_slide = (current_slide-1) % len(img_list)
        else:
            current_slide = (current_slide+1) % len(img_list)

        img_size = left_frame.winfo_height() - 200
        showImage(img_list[current_slide], img_size)

        slide_caption.configure(text = "Image {} of {}".format(current_slide+1, len(img_list)))


def selectMultiImage():
    global img_list, current_slide, slide_caption, slide_control_panel

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path_list = filedialog.askopenfilenames(title="Choose atleast 9 images", filetypes=filetype)

    if(len(path_list) > 0):
        img_list = []
        current_slide = -1
        if (slide_control_panel != None):
            slide_control_panel.destroy()

        for path in path_list:
            print(path)
            img_list.append(cv2.imread(path))


        # Creating slideshow of images
        img_size =  left_frame.winfo_height() - 200
        current_slide += 1
        showImage(img_list[current_slide], img_size)

        slide_control_panel = Frame(left_frame, bg="#202d42", pady=20)
        slide_control_panel.pack()

        back_img = PhotoImage(file="previous.png")
        next_img = PhotoImage(file="next.png")

        prev_slide = Button(slide_control_panel, image=back_img, bg="#202d42", bd=0, highlightthickness=0,
                            activebackground="#202d42", command=lambda : getNewSlide("prev"))
        prev_slide.image = back_img
        prev_slide.grid(row=0, column=0, padx=60)

        slide_caption = Label(slide_control_panel, text="Image 1 of {}".format(len(img_list)), fg="#ff9800",
                              bg="#202d42", font="Arial 15 bold")
        slide_caption.grid(row=0, column=1)

        next_slide = Button(slide_control_panel, image=next_img, bg="#202d42", bd=0, highlightthickness=0,
                            activebackground="#202d42", command=lambda : getNewSlide("next"))
        next_slide.image = next_img
        next_slide.grid(row=0, column=2, padx=60)


def register(name):
    global img_list

    if(len(img_list) == 0):
        messagebox.showerror("Error", "Select Images first.")
    elif(len(name) == 0):
        messagebox.showerror("Error", "Enter the name first.")
    else:
        # Setting Directory
        path = os.path.join('face_samples', name)
        if not os.path.isdir(path):
            os.mkdir(path)

        for i in range(len(img_list)):
            registerCriminal(img_list[i], path, i+1)


## Register Page ##
def getPage1():
    global active_page, left_frame, right_frame, heading
    active_page = 1
    pages[1].lift()

    basicPageSetup(1)
    heading.configure(text="Register Criminal")
    right_frame.configure(text="Enter Details")

    btn_grid = Frame(left_frame, bg="#202d42")
    btn_grid.pack()

    Button(btn_grid, text="Select Images", command=selectMultiImage, font="Arial 15 bold", bg="#2196f3",
           fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
           activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    # Button(btn_grid, text="Start Camera", command=startRecognition, font="Arial 15 bold", padx=20, bg="#2196f3",
    #        fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
    #        activeforeground="white").grid(row=0, column=1, padx=25, pady=25)


    name = Entry(right_frame)
    name.pack()
    Button(right_frame, text="Register", command=lambda: register(name.get())).pack()


## Detection Page ##
def getPage2():
    global active_page, left_frame, right_frame, img_label, heading
    img_label = None
    active_page = 2
    pages[2].lift()

    basicPageSetup(2)
    heading.configure(text="Detect Criminal")
    right_frame.configure(text="Detected Criminals")

    btn_grid = Frame(left_frame, bg="#202d42")
    btn_grid.pack()

    Button(btn_grid, text="Select Image", command=selectImage, font="Arial 15 bold", padx=20, bg="#2196f3",
            fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",
            activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    Button(btn_grid, text="Recognize", command=startRecognition, font="Arial 15 bold", padx=20, bg="#2196f3",
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
    global active_page, video_loop, left_frame, right_frame, thread_event, heading
    active_page = 3
    pages[3].lift()

    basicPageSetup(3)
    heading.configure(text="Video Surveillance")
    right_frame.configure(text="Detected Criminals")
    left_frame.configure(pady=40)

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
    btn.configure(font="Arial 20", width=17, bg="#2196f3", fg="white",
        pady=15, bd=0, highlightthickness=0, activebackground="#091428", activeforeground="white")
    btn.pack(pady=30)



pages[0].lift()
getPage1()
root.mainloop()

# aWidget.tk.call('tk', 'scaling', 1)