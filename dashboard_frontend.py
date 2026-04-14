import customtkinter as ctk
from dashboard_backend import DashboardBackend

# get window to stay where it left off/ where it was closed 
# make it so that frames/tiles cannot outgrow the main window 
#make it so frame size and widget size is standardized, currently they size differently;
#for different length values making the frames inconsistant. 

class UserInterface:
    def __init__(self):
        self.backend= DashboardBackend()
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
        device_list= self.backend.get_device_names()

        for name in device_list:
            self.ui_frames[name]= ctk.CTkFrame(master=self.main_window, corner_radius=10)
            self.ui_frames[name].grid(padx=10, pady=10)

            system_name= ctk.CTkLabel(master= self.ui_frames[name], text= name)
            system_name.grid(padx=5, pady=5)

    def make_widgets(self):
        for name, frame in self.ui_frames.items():
            try:
                ip, port= self.backend.get_device_config(name)
                vendor_OIDs= self.backend.get_vendor_oid(ip, port)

                up_time= ctk.CTkLabel(frame, text= self.backend.system_uptime(vendor_OIDs, ip, port))
                up_time.grid(padx=5, pady=1)

                cpu_usage= ctk.CTkLabel(frame, text= self.backend.system_cpu_usage(vendor_OIDs, ip, port))
                cpu_usage.grid(padx=5, pady=1)

                ram_usage= ctk.CTkLabel(frame, text= self.backend.system_ram_usage(vendor_OIDs, ip, port))
                ram_usage.grid(padx=5, pady=1)

                disk_usage= ctk.CTkLabel(frame, text= self.backend.system_disk_usage(vendor_OIDs, ip, port))
                disk_usage.grid(padx=5, pady=1)

                network_usage= ctk.CTkLabel(frame, text= "")
                network_usage.grid(padx=5, pady=1)

            except ValueError: 
                ip= self.backend.get_device_config(name)
                vendor_OIDs= self.backend.get_vendor_oid(ip)

                up_time= ctk.CTkLabel(frame, text= self.backend.system_uptime(vendor_OIDs, ip))
                up_time.grid(padx=5, pady=1)

                cpu_usage= ctk.CTkLabel(frame, text= self.backend.system_cpu_usage(vendor_OIDs, ip))
                cpu_usage.grid(padx=5, pady=1)

                ram_usage= ctk.CTkLabel(frame, text= self.backend.system_ram_usage(vendor_OIDs, ip))
                ram_usage.grid(padx=5, pady=1)

                disk_usage= ctk.CTkLabel(frame, text= self.backend.system_disk_usage(vendor_OIDs, ip))
                disk_usage.grid(padx=5, pady=1)

                network_usage= ctk.CTkLabel(frame, text= "")
                network_usage.grid(padx=5, pady=1)
                ip = self.backend.get_device_config(name)
            


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

 