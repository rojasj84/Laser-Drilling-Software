# Import libraries from Python
import tkinter as tk
import numpy as np
import cv2

from threading import Thread
from PIL import ImageTk, Image, ImageFont, ImageDraw

# ************** Defining General Functions **************

def do_nothing():
    x = 1

# ************** Defining Classes **************

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Laser Drilling System')
        self.geometry('1300x1000')
        self.configure(bg="light gray")

        PositionControl = PositionControlFrame(self, 900, 20)        
        InterlockFrame = InterlockSafetyFrame(self, 900, 380)
        CameraDisplayWindow = CameraFrame(self, 2, 2)
        CameraDisplayWindow = CameraFrame2(self, 0, 500)

class CameraFrame(tk.Frame):
    def __init__(self, container, x_position, y_position):
        super().__init__(container)
        # tk.Frame.__init__(self, master)

        self.x_position = x_position
        self.y_position = y_position
        self.config(background=win_color)
        self.place(x=self.x_position,y=self.y_position,width = 644, height = 484)

        # Display Camera 1
        Camera1_x_position = 2
        Camera1_y_position = 2
        Camera1 = DisplayCamera(self, Camera1_x_position, Camera1_y_position)       

class CameraFrame2(tk.Frame):
    def __init__(self, container, x_position, y_position):
        super().__init__(container)
        # tk.Frame.__init__(self, master)

        self.x_position = x_position
        self.y_position = y_position
        self.config(background=win_color)
        self.place(x=self.x_position,y=self.y_position,width = 660, height = 500)

        # Display Camera 1
        Camera1_x_position = 2
        Camera1_y_position = 2
        Camera1 = DisplayCamera(self, Camera1_x_position, Camera1_y_position) 

class CameraWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Camera Window')
        self.geometry('660x1000')
        self.configure(bg=win_color)

        # Display Camera 1
        Camera1_x_position = 10
        Camera1_y_position = 10
        Camera1 = DisplayCamera(self, Camera1_x_position, Camera1_y_position)        

class DisplayCamera(tk.Frame):
    def __init__(self, master,x_position,y_position):
        # super().__init__()
        tk.Frame.__init__(self, master)
        
        self.x_position = x_position
        self.y_position = y_position
        
        self.config(background=win_color)
        self.place(x=x_position,y=y_position,height = 480,width = 640)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3,640)     #horizontal pixels
        self.cap.set(4,480)     #vertical pixels
        self.cap.set(5, 30)      #Camera frame rate
        
        # Label to display camera image
        self.image_display_label = tk.Label(self, text="", relief=tk.FLAT)
        self.image_display_label.place(x=0,y=0)       
        
        show_camera_thread = Thread(target=self.show_camera)
        show_camera_thread.start()

    def show_camera(self):
        # get frame
        ret, frame = self.cap.read()
        
        if ret:
            # cv2 uses `BGR` but `GUI` needs `RGB`
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # frame = cv2.flip(frame, 1) #Mirror the image

            # convert to PIL image
            img = Image.fromarray(frame)

            # convert to Tkinter image
            converted_to_tkinter = ImageTk.PhotoImage(image=img)

            # solution for bug in `PhotoImage`
            self.image_display_label.photo = converted_to_tkinter
            self.image_display_label.configure(image=converted_to_tkinter)            
            
        # run again after 20ms (0.02s)
        self.after(10, self.show_camera)

class LaserPower(tk.Frame):
    def __init__(self, container, x_position, y_position):
        
        super().__init__(container)
        # tk.Frame.__init__(self, master)

        self.x_position = x_position
        self.y_position = y_position
        self.config(background="black")
        self.place(x=self.x_position,y=self.y_position,width = 382, height = 352)

        button_scale = 5

        self.border_frame = tk.Frame(self, bd = 0, relief=tk.RIDGE, bg = win_color)
        self.border_frame.place(x = 1, y = 1, width = 380, height = 350)

class PositionControlFrame(tk.Frame):
    def __init__(self, container, x_position, y_position):
        super().__init__(container)
        # tk.Frame.__init__(self, master)

        self.x_position = x_position
        self.y_position = y_position
        self.config(background="black")
        self.place(x=self.x_position,y=self.y_position,width = 382, height = 352)

        button_scale = 5

        self.border_frame = tk.Frame(self, bd = 0, relief=tk.RIDGE, bg = win_color)
        self.border_frame.place(x = 1, y = 1, width = 380, height = 350)

        self.up_image = ImageTk.PhotoImage(self.scale_images("images/up.png", button_scale))
        self.up_button = tk.Button(self, image = self.up_image, text="Up", command=do_nothing, relief=tk.FLAT, bg=win_color)
        self.up_button.place(x = 100, y = 15)

        self.down_image = ImageTk.PhotoImage(self.scale_images("images/down.png", button_scale))
        self.down_button = tk.Button(self, image = self.down_image, text="Down", command=do_nothing, relief=tk.FLAT, bg=win_color)
        self.down_button.place(x = 100, y = 125)

        self.right_image = ImageTk.PhotoImage(self.scale_images("images/right.png", button_scale))
        self.right_button = tk.Button(self, image = self.right_image, text="Down", command=do_nothing, relief=tk.FLAT, bg=win_color)
        self.right_button.place(x = 155, y = 70)

        self.left_image = ImageTk.PhotoImage(self.scale_images("images/left.png", button_scale))
        self.left_button = tk.Button(self, image = self.left_image, text="Down", command=do_nothing, relief=tk.FLAT, bg=win_color)
        self.left_button.place(x = 45, y = 70)

        self.focus_plus_image = ImageTk.PhotoImage(self.scale_images("images/focus_plus.png", 5))
        self.focus_plus_button = tk.Button(self, image = self.focus_plus_image, text="focus_plus", command=do_nothing, relief=tk.FLAT, bg=win_color)
        self.focus_plus_button.place(x = 275, y = 30)

        self.focus_minus_image = ImageTk.PhotoImage(self.scale_images("images/focus_minus.png", 5))
        self.focus_minus_button = tk.Button(self, image = self.focus_minus_image, text="focus_minus", command=do_nothing, relief=tk.FLAT, bg=win_color)
        self.focus_minus_button.place(x = 275, y = 110)
        
        self.step_size_1 = tk.Button(self, text = "1 μm", command=lambda: self.set_custom_stepsize("1"))
        self.step_size_1.place(x = 30, y = 250, width= 60)

        self.step_size_5 = tk.Button(self, text = "5 μm", command=lambda: self.set_custom_stepsize("5"))
        self.step_size_5.place(x = 95, y = 250, width= 60)
        
        self.step_size_50 = tk.Button(self, text = "50 μm", command=lambda: self.set_custom_stepsize("50"))
        self.step_size_50.place(x = 160, y = 250, width= 60)

        self.step_size_100 = tk.Button(self, text = "100 μm", command=lambda: self.set_custom_stepsize("100"))
        self.step_size_100.place(x = 225, y = 250, width= 60)

        self.step_size_300 = tk.Button(self, text = "300 μm", command=lambda: self.set_custom_stepsize("300"))
        self.step_size_300.place(x = 290, y = 250, width= 60)

        self.custom_step_size = tk.Text(self)
        self.custom_step_size.place(x = 230, y = 290, width=80, height = 25)

        self.custom_step_size_label = tk.Label(self, text="Custom Step Size (μm):", bg = win_color)
        self.custom_step_size_label.place(x = 65, y = 290, width=150, height = 25)
        
        
        font_tuple = ("/fonts/Impact.ttf", 20)
        self.position_label = tk.Label(self, text="POSITION", font = font_tuple, bg = win_color)
        self.position_label.place(x = 65, y = 190, width = 125)

        self.focus_label = tk.Label(self, text="FOCUS", font = font_tuple, bg = win_color)
        self.focus_label.place(x = 260, y = 190, width = 90)

        self.set_custom_stepsize("100")

    def scale_images(self, file_loc, scale):
        img = Image.open(file_loc)
        img_width, img_height = img.size
        img = img.resize((50, 50), resample=Image.Resampling.LANCZOS)
        return img

    def set_custom_stepsize(self, value):
        self.custom_step_size.delete("1.0",tk.END)
        self.custom_step_size.insert(tk.END,value)
        
class InterlockSafetyFrame(tk.Frame):
    def __init__(self, container, x_position, y_position):
        super().__init__(container)
        # tk.Frame.__init__(self, master)

        self.x_position = x_position
        self.y_position = y_position
        self.config(background="black")
        self.place(x=self.x_position,y=self.y_position,width = 382, height = 142)

        self.border_frame = tk.Frame(self, bd = 0, relief=tk.RIDGE, bg = win_color)
        self.border_frame.place(x = 1, y = 1, width = 380, height = 140)

        self.motor_driver_status = 0
        self.front_door_interlock_status = 0
        self.pulse_generator_status = 0
        self.laser_power_status = 0
        self.laser_ready_status = 0
        
        # Switching light on or off images
        self.on_image = tk.PhotoImage(width=20, height=20)
        self.off_image = tk.PhotoImage(width=20, height=20)
        self.on_image.put(("green",), to=(2, 2, 18,18))
        self.off_image.put(("red",), to=(2, 2, 18, 18))

        self.motor_driver_status_label = tk.Label(self, text = "Motor Driver Status", bg="white", anchor = tk.E)
        self.motor_driver_status_label.place(x = 10, y = 10, width = 140, height = 20)
        self.motor_driver_status_image = tk.Label(self, text = "", image = self.off_image, relief=tk.RAISED)
        self.motor_driver_status_image.place(x = 155, y = 10, width = 20, height = 20 )

        self.front_door_interlock_status_label = tk.Label(self, text = "Door Interlock", bg="white", anchor = tk.E)
        self.front_door_interlock_status_label.place(x = 10, y = 35, width = 140, height = 20)
        self.front_door_interlock_status_image = tk.Label(self, text = "", image = self.off_image, relief=tk.RAISED)
        self.front_door_interlock_status_image.place(x = 155, y = 35, width = 20, height = 20 )

        self.pulse_generator_status_label = tk.Label(self, text = "Pulse Generator", bg="white", anchor = tk.E)
        self.pulse_generator_status_label.place(x = 10, y = 60, width = 140, height = 20)
        self.pulse_generator_status_image = tk.Label(self, text = "", image = self.off_image, relief=tk.RAISED)
        self.pulse_generator_status_image.place(x = 155, y = 60, width = 20, height = 20 )

        self.laser_power_status_label = tk.Label(self, text = "Laser Power", bg="white", anchor = tk.E)
        self.laser_power_status_label.place(x = 10, y = 85, width = 140, height = 20)
        self.laser_power_status_image = tk.Label(self, text = "", image = self.off_image, relief=tk.RAISED)
        self.laser_power_status_image.place(x = 155, y = 85, width = 20, height = 20 )
        
        self.laser_ready_status_label = tk.Label(self, text = "Laser Ready", bg="white", anchor = tk.E)
        self.laser_ready_status_label.place(x = 10, y = 110, width = 140, height = 20)
        self.laser_ready_status_image = tk.Label(self, text = "", image = self.off_image, relief=tk.RAISED)
        self.laser_ready_status_image.place(x = 155, y = 110, width = 20, height = 20 )

        
        self.ir_laser_test_label = tk.Label(self, text = "IR Laser Test", bg="white", anchor = tk.W)
        self.ir_laser_test_label.place(x = 200, y = 10, width = 140, height = 20)
        self.ir_laser_test_label_image = tk.Label(self, text = "", image = self.off_image, relief=tk.RAISED)
        self.ir_laser_test_label_image.place(x = 340, y = 40, width = 20, height = 20 )
        
        self.ir_laser_test_on = tk.Button(self, text = "ON", command= lambda: self.ir_laser_test_function(1))
        self.ir_laser_test_on.place(x = 200, y = 35, width = 60, height = 30 )

        self.ir_laser_test_off = tk.Button(self, text = "OFF", command= lambda: self.ir_laser_test_function(0))
        self.ir_laser_test_off.place(x = 270, y = 35, width = 60, height = 30 )

    def ir_laser_test_function(self, state):
        if state == 1:
            self.ir_laser_test_label_image.config(image=self.on_image)
        elif state == 0:
            self.ir_laser_test_label_image.config(image=self.off_image)
    
        
        
        


        


        


if __name__ == "__main__":
    win_color = 'white'
    COMPORT = "COM10"

    # Creating the main window and camera display window
    window = MainWindow()
    

    window.mainloop()
