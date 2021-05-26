import cv2
import time
import os
import tkinter
import PIL.Image
import PIL.ImageTk

file_path = os.path.dirname(__file__)
gallery_path = os.path.join(file_path, "gallery")
hand_path = os.path.join(gallery_path, "hand_templates")

main_windows = tkinter.Tk(className='open camera')
camera = cv2.VideoCapture(0)

frame_w = camera.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
frame_h = camera.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2
canvas = tkinter.Canvas(main_windows, width=frame_w, height=frame_h)
canvas.pack()

photo = None
counting = 0


def do_take_photo():
    global counting
    counting += 1


def enter_to_do(e):
    global counting
    counting += 1


def update_frame():
    global photo, camera, counting
    ret, frame = camera.read()
    cv2.rectangle(frame,
                  (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH) // 2 - 100),
                   int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2 - 100)),
                  (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH) // 2 + 100),
                   int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2 + 100)),
                  (0, 255, 0), 3)
    # resize frame fit to main_windows's canvas
    frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    # convert color system
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # convert numpy image to image
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    main_windows.after(1, update_frame)  # after 1 ms, refresh frame.

    if 0 < counting < 5:
        time.sleep(0.1)  # If don't wait, the image will be dark
        return_value, image = camera.read()
        cv2.imwrite(f"hand_{counting}.png", image)
        image = cv2.imread(f"hand_{counting}.png")
        # crop frame for main file
        face = image[140:340, 220:420]
        # writing to path
        cv2.imwrite(f"{hand_path}/final_{counting}.png", face)
        # remove hands picture
        os.remove(f"hand_{counting}.png")
        counting += 1

    elif counting >= 5:
        main_windows.quit()


button = tkinter.Button(main_windows, text='Press Enter or press the button here', activebackground='pale green',
                        command=do_take_photo)
button.pack()

main_windows.bind('<Return>', enter_to_do)
update_frame()
main_windows.mainloop()
