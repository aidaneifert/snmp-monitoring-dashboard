import asyncio
from dashboard_snmp import DashboardSNMP as SNMP
from dashboard_conf import DashboardConfig as Config

#all methods need to return a string data type for display on gui!!!!!!
#need to figure out how to pass sytem specific config data to snmp class, (solved??)

class DashboardBackend():
    def __init__(self):
        self.snmp= SNMP()
        self.config= Config()
        self.config_data= self.config.read_dashboard_config()

    def get_device_config(self, system_id):
        device_config= self.config_data[system_id]
        ip_addr= device_config["ip_address"]
        try:
            port= device_config["port"]
            return ip_addr, port
        
        except KeyError:
            return ip_addr
        
    def system_uptime(self, system_id):
        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            snmp_requst= asyncio.run(self.snmp.get_uptime(ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            snmp_requst= asyncio.run(self.snmp.get_uptime(ip_addr))

        seconds= float(snmp_requst) / 100
        months= seconds // 2592000
        rs= seconds % 2592000
        weeks= rs // 604800
        rs= rs % 604800
        days= rs // 86400
        rs= rs % 86400
        hours= rs // 3600
        rs= rs % 3600
        minutes= rs // 60
        rs= rs % 60
        uptime= f"Months:{int(months)} Weeks:{int(weeks)} Days:{int(days)} Hours:{int(hours)} Minutes:{int(minutes)} Seconds:{int(rs)}"

        return uptime
    #this works on the assumption that a month is 30 days always, eventually will add realtime month adjustment for 
    #more acurate uptime. 
        
    def system_cpu_usage(self, system_id):
        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            snmp_cpu_usage= asyncio.run(self.snmp.get_cpu_usage(ip_addr, server_port= port))
            snmp_cpu_cores= asyncio.run(self.snmp.get_cpu_usage(ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            snmp_cpu_usage= asyncio.run(self.snmp.get_cpu_usage(ip_addr))
            snmp_cpu_cores= asyncio.run(self.snmp.get_cpu_usage(ip_addr))

        cpu_usage_precentage= float(snmp_cpu_usage) / float(snmp_cpu_cores)
        
        return snmp_cpu_usage, snmp_cpu_cores
    

    def system_ram_usage(self):
        self.snmp.get_ram_usage()
        return
    
    def system_disk_usage(self):
        self.snmp.get_disk_usage()
        return
    
    def system_download_speed(self):
        self.snmp.get_network_down_speed()
        return
    
    def system_upload_speed(self):
        self.snmp.get_network_up_speed()
        return

#this is test/ debug code. 
if __name__ == "__main__":
    DBBE= DashboardBackend()
    value= DBBE.system_cpu_usage("server 1")
    print(value)
