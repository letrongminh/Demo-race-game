import cv2
import time
import os
import tkinter
import PIL.Image
import PIL.ImageTk

main_windows = tkinter.Tk(className='open camera')
camera = cv2.VideoCapture(0)
# main_windows.geometry('80x80')
frame_w = camera.get(cv2.CAP_PROP_FRAME_WIDTH) // 2
frame_h = camera.get(cv2.CAP_PROP_FRAME_HEIGHT) // 2
canvas = tkinter.Canvas(main_windows, width=frame_w, height=frame_h)
canvas.pack()

photo = None

counting = 0


def do_take_photo():
    global counting
    counting += 1


def update_frame():
    global photo, camera, counting
    ret, frame = camera.read()
    frame = cv2.resize(frame, dsize=None, fx=0.5, fy=0.5)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # convert numpy image to image
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    main_windows.after(1, update_frame)  # after 1 ms, refresh frame.

    if 0 < counting < 4:
        time.sleep(0.1)  # If don't wait, the image will be dark
        return_value, image = camera.read()
        cv2.imwrite(f"hand_{counting}.png", image)
        image = cv2.imread(f"hand_{counting}.png")
        # face = image[220:420, 140:340]
        face = image[140:340, 220:420]
        cv2.imwrite(f"final_{counting}.png", face)
        os.remove(f"hand_{counting}.png")
        counting += 1
    elif counting > 4:
        main_windows.quit()
#
# # camera.release()
# cv2.destroyAllWindows()
# del camera  # so that others can use the camera as soon as possible


button = tkinter.Button(main_windows, text='take photos', command=do_take_photo)
button.pack()

update_frame()
main_windows.mainloop()
print(counting)
