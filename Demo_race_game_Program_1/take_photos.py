import cv2
import time
import os
import tkinter


main_windows = tkinter.Tk(className='open camera')

main_windows.geometry('80x80')


def take_photo():
    counting = 0
    camera = cv2.VideoCapture(0)
    while counting < 4:
        ret, frame = camera.read()
        if ret:
            cv2.imshow('video', frame)

        if cv2.waitKey(1) == ord('a'):
            while counting < 4:
                time.sleep(0.1)  # If don't wait, the image will be dark
                counting += 1
                return_value, image = camera.read()
                cv2.imwrite(f"hand_{counting}.png", image)

                image = cv2.imread(f"hand_{counting}.png")

                # face = image[220:420, 140:340]
                face = image[140:340, 220:420]
                cv2.imwrite(f"final_{counting}.png", face)
                os.remove(f"hand_{counting}.png")
        if cv2.waitKey(1) == ord('q'):
            break
        main_windows.quit()

    # camera.release()
    cv2.destroyAllWindows()
    del camera  # so that others can use the camera as soon as possible


B = tkinter.Button(main_windows, width=10, height=5, text="OK", bg='red', activebackground='red', command=take_photo)
B.pack()
main_windows.mainloop()
