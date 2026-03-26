import asyncio
from dashboard_snmp import DashboardSNMP as SNMP
from dashboard_conf import DashboardConfig as Config

#all methods need to return a string data type for display on gui!!!!!!
#need to figure out how to pass system specific config data to snmp class without passing config to the front end. 
#this works on the assumption that a month is 30 days always, eventually will add realtime month adjustment for 
#more acurate uptime. 

class DashboardBackend():
    def __init__(self):
        self.snmp= SNMP()
        self.config= Config()
        self.config_data= self.config.read_dashboard_config()
        self.full_oid_dict= self.config.read_oid_table()
        
    def get_device_config(self, system_id):
        device_config= self.config_data[system_id]
        ip_addr= device_config["ip_address"]
        try:
            port= device_config["port"]
            return ip_addr, port
        
        except KeyError:
            return ip_addr
        
    def get_vendor_oid(self, system_id):
        
        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            system_info= asyncio.run(self.snmp.get_system_info(ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            system_info= asyncio.run(self.snmp.get_system_info(ip_addr))
            
        oid= system_info.strip(".").split(".")
        private_enterprise_number= oid[6]
  
        match private_enterprise_number:
            case "311":
                vendor_oids= self.full_oid_dict["Microsoft"]

            case "9":
                vendor_oids= self.full_oid_dict["Cisco"]

            case "11":
                vendor_oids= self.full_oid_dict["HP"]

            case "2636":
                vendor_oids= self.full_oid_dict["Juniper"] 

            case "674":
                vendor_oids= self.full_oid_dict["Dell"] 

            case "6876":
                vendor_oids= self.full_oid_dict["VMWare"] 

            case "8072":
                vendor_oids= self.full_oid_dict["Net-SNMP"] 

            case "41112":
                vendor_oids= self.full_oid_dict["Ubiquiti"] 
                
            case _:
                vendor_oids= self.full_oid_dict["0"] 

        return vendor_oids

    def system_uptime(self, system_id):
        
        vendor_oids= self.get_vendor_oid(system_id= system_id)
        oid= vendor_oids["uptime"]
        
        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            snmp_requst= asyncio.run(self.snmp.get_uptime(oid, ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            snmp_requst= asyncio.run(self.snmp.get_uptime(oid, ip_addr))

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

    def system_cpu_usage(self, system_id):
        vendor_oids= self.get_vendor_oid(system_id= system_id)
        usage_oid= vendor_oids["cpu_usage"]       
        cores_oid= vendor_oids["cpu_cores"]
        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            snmp_cpu_usage= asyncio.run(self.snmp.get_cpu_usage(usage_oid, ip_addr, server_port= port))
            snmp_cpu_cores= asyncio.run(self.snmp.get_cpu_usage(cores_oid, ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            snmp_cpu_usage= asyncio.run(self.snmp.get_cpu_usage(usage_oid, ip_addr))
            snmp_cpu_cores= asyncio.run(self.snmp.get_cpu_usage(cores_oid, ip_addr))
        print(snmp_cpu_cores)
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
    value= DBBE.get_vendor_oid("server 1")
    print(value)
