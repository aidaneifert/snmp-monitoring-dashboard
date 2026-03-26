import customtkinter as ctk
from dashboard_conf import DashboardConfig
from dashboard_backend import DashboardBackend

class UserInterface:
    def __init__(self):
        self.config= DashboardConfig()
        self.backend= DashboardBackend()

        self.devices= self.config.read_dashboard_config()
        self.main_window= ctk.CTk()
        self.window_name= "Dashboard"
        self.ui_frames= {}
    
    def size_window(self):
        user_screen_width= self.main_window.winfo_screenwidth()
        user_screen_height= self.main_window.winfo_screenheight()
        screen_startup_width= user_screen_width //2
        screen_startup_height= user_screen_height //2
        return screen_startup_width, screen_startup_height
    
    def place_window(self):
        screen_width= self.main_window.winfo_screenwidth()
        screen_height= self.main_window.winfo_screenheight()
        window_width, window_height= self.size_window()
        x= screen_width //2 - int(window_width) //2
        y= screen_height //2 - int(window_height) //2
        window_placement= f"+{x}+{y}"
        return window_placement
    
    def make_frames(self):
        for device, items in self.devices.items():
            device_name= str(device)

            self.ui_frames[device_name]= ctk.CTkFrame(master=self.main_window, corner_radius=10)
            self.ui_frames[device_name].grid(padx=10, pady=10)

            system_name= ctk.CTkLabel(master= self.ui_frames[device_name], text= items['name'])
            system_name.grid(padx=5, pady=5)

    def make_widgets(self):
        for frame_name, frame in self.ui_frames.items():
            
            up_time= ctk.CTkLabel(frame, text= self.backend.system_uptime(frame_name))
            up_time.grid(padx=5, pady=1)

            cpu_usage= ctk.CTkLabel(frame, text= self.backend.system_cpu_usage(frame_name))
            cpu_usage.grid(padx=5, pady=1)

            ram_usage= ctk.CTkLabel(frame, text= "")
            ram_usage.grid(padx=5, pady=1)

            disk_usage= ctk.CTkLabel(frame, text= "")
            disk_usage.grid(padx=5, pady=1)

            network_downlink_speed= ctk.CTkLabel(frame, text= "")
            network_downlink_speed.grid(padx=5, pady=1)

            network_uplink_speed= ctk.CTkLabel(frame, text= "")
            network_uplink_speed.grid(padx=5, pady=1)
    
    def start_window(self):
        self.main_window.title(self.window_name)
        window_width, window_height= self.size_window()
        self.main_window.geometry(f"{window_width}x{window_height}{self.place_window()}") 
        self.main_window.resizable(False, False)
        self.make_frames()
        self.make_widgets()
        self.main_window.mainloop()

if __name__ == "__main__":
    ui = UserInterface()
    ui.start_window()

# get window to stay where it left off/ where it was closed 
# make it so that frames/tiles cannot outgrow the main window 
#make it so frame size and widget size is standardized, currently they size differently;
#for different length values making the frames inconsistant. 