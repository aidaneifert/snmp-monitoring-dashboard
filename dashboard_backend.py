import asyncio
from dashboard_snmp import DashboardSNMP as SNMP
from dashboard_conf import DashboardConfig as Config

#this works on the assumption that a month is 30 days always, eventually will add realtime month adjustment for 
#more acurate uptime. 

class DashboardBackend():
    def __init__(self):
        self.snmp= SNMP()
        self.config= Config()
        self.config_data= self.config.read_dashboard_config()
        self.full_oid_dict= self.config.read_oid_table()
        
    def get_device_names(self):
        device_dict= self.config.read_dashboard_config()
        device_names= device_dict.keys()
        return device_names

    def get_device_config(self, name):
        device_config= self.config_data[name]
        ip_addr= device_config["ip_address"]
        try:
            port= device_config["port"]
            return ip_addr, port
        
        except KeyError:
            print(ip_addr)
            return ip_addr
        
    def get_vendor_oid(self, ip, port= 161):
        print(ip, port)
        system_info= asyncio.run(self.snmp.get_system_info(ip, port))
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

    def system_uptime(self, vendor_OIDs, ip, port = 161):
        oid= vendor_OIDs["uptime"]
        snmp_requst= asyncio.run(self.snmp.get_uptime(oid, ip, server_port= port))
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
        return f"Months:{int(months)} Weeks:{int(weeks)} Days:{int(days)} Hours:{int(hours)} Minutes:{int(minutes)} Seconds:{int(rs)}"

    def system_cpu_usage(self, vendor_OIDs, ip, port = 161):
        cores_oid= vendor_OIDs["cpu_cores"]
        cpu_usage= asyncio.run(self.snmp.get_cpu_usage(cores_oid, ip, server_port= port))
        return f"CPU: {int(cpu_usage)}%"

    def system_ram_usage(self, vendor_OIDs, ip, port = 161):
        storage_desc_OID= vendor_OIDs["storage_types"]
        memory_used_OID= vendor_OIDs["storage_used"]
        memory_size_OID= vendor_OIDs["storage_size"]
    
        memory_idx_list= asyncio.run(self.snmp.get_memory_index(storage_desc_OID, ip, port))
        memory_used= asyncio.run(self.snmp.get_ram_usage(memory_used_OID, memory_idx_list, ip, port))
        total_memory= asyncio.run(self.snmp.get_ram_total_capacity(memory_size_OID, memory_idx_list, ip, port))
    
        try:
            usage_precentage= (memory_used / total_memory) * 100
        except ZeroDivisionError:
            usage_precentage= 0
        
        return f"RAM: {int(usage_precentage)}%"
  
    def system_disk_usage(self, vendor_OIDs, ip, port = 161):
        storage_description_OID= vendor_OIDs["storage_types"]
        storage_size_OID= vendor_OIDs["storage_size"]
        storage_used_OID= vendor_OIDs["storage_used"]
        sector_size_OID= vendor_OIDs["storage_sector_size"]

        disk_idx_list= asyncio.run(self.snmp.get_disk_index(storage_description_OID, ip, port))
        sector_size= asyncio.run(self.snmp.get_disk_sector_size(sector_size_OID, disk_idx_list, ip, port))
        storage_used= asyncio.run(self.snmp.get_disk_usage(storage_used_OID, disk_idx_list, ip, port))
        total_storage= asyncio.run(self.snmp.get_disk_total_capacity(storage_size_OID, disk_idx_list, ip, port))
    
        return
   
    def system_network_usage(self):
        self.snmp.get_network_down_speed()
        return
 
