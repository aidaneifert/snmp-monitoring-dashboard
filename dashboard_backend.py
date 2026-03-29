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
        cores_oid= vendor_oids["cpu_cores"]
        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            cpu_usage= asyncio.run(self.snmp.get_cpu_usage(cores_oid, ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            cpu_usage= asyncio.run(self.snmp.get_cpu_usage(cores_oid, ip_addr))
        
        return f"CPU: {int(cpu_usage)}%"

    def system_ram_usage(self, system_id):
        vendor_oids= self.get_vendor_oid(system_id= system_id)
        storage_desc_oid= vendor_oids["storage_types"]
        storage_size= vendor_oids["storage_size"]
        storage_used= vendor_oids["storage_used"]
        used_oids= (storage_desc_oid, storage_used)
        total_oids= (storage_desc_oid, storage_size)

        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            storage_used= asyncio.run(self.snmp.get_ram_usage(used_oids, ip_addr, server_port= port))
            total_storage= asyncio.run(self.snmp.get_ram_total_capacity(total_oids, ip_addr, server_port= port))
           
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            storage_used= asyncio.run(self.snmp.get_ram_usage(used_oids, ip_addr))
            total_storage= asyncio.run(self.snmp.get_ram_total_capacity(total_oids, ip_addr))
        try:
            usage_precentage= (storage_used / total_storage) * 100
        except ZeroDivisionError:
            usage_precentage= 0
        return f"RAM: {int(usage_precentage)}%"
  
    def system_disk_usage(self, system_id):
        vendor_oids= self.get_vendor_oid(system_id= system_id)
   

        storage_desc_oid= vendor_oids["storage_types"]
        storage_size_oid= vendor_oids["storage_size"]
        storage_used_oid= vendor_oids["storage_used"]
        sector_size_oid= vendor_oids["storage_sector_size"]

        used_oids= (storage_desc_oid, storage_used_oid)
        total_oids= (storage_desc_oid, storage_size_oid)
        sector_size_oid= (storage_desc_oid, sector_size_oid)

        try:
            ip_addr, port= self.get_device_config(system_id= system_id)
            sector_size= asyncio.run(self.snmp.get_disk_sector_size(sector_size_oid, ip_addr, server_port= port))
            storage_used= asyncio.run(self.snmp.get_disk_usage(used_oids, sector_size, ip_addr, server_port= port))
            total_storage= asyncio.run(self.snmp.get_disk_total_capacity(total_oids, sector_size, ip_addr, server_port= port))
            
        except ValueError:
            ip_addr= self.get_device_config(system_id= system_id)
            sector_size= asyncio.run(self.snmp.get_disk_sector_size(sector_size_oid, ip_addr))
            storage_used= asyncio.run(self.snmp.get_disk_usage(used_oids, sector_size, ip_addr))
            total_storage= asyncio.run(self.snmp.get_disk_total_capacity(total_oids, sector_size, ip_addr))
            

        try:
        

            usage_precentage= storage_bytes_used / storage_bytes_total * 100
            gb_used= storage_bytes_used /  1000000000
            total_gb= storage_bytes_total / 1000000000
            
        except ZeroDivisionError:
            usage_precentage= 0
            gb_used= 0
            total_gb= 0            

        return f"Disk: {int(gb_used)}GB / {int(total_gb)}GB | {usage_precentage}%"
   
    def system_network_usage(self):
        self.snmp.get_network_down_speed()
        return
 
