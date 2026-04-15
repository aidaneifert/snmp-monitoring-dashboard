import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

class DashboardSNMP:
    async def get_system_info(self, server_ip, server_port= 161):
        error_indication, error_status, error_index, var_binds= await get_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.1.2.0'))
            )
        
        if error_indication:
            return error_indication
        elif error_status:
            return error_status
        elif error_status:
            return error_index
        elif var_binds:        
            value_object= var_binds[0][1]
            sys_object_id= str(value_object)
            return sys_object_id
                
    async def get_uptime(self, oid, server_ip, server_port):
        error_indication, error_status, error_index, var_binds= await get_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
            )
        
        if error_indication:
            return error_indication
        elif error_status:
            return error_status
        elif error_status:
            return error_index
        elif var_binds:
            value_object= var_binds[0][1]
            raw_uptime= str(value_object)
            return raw_uptime
    
    async def get_cpu_usage(self, oid, server_ip, server_port):
        cores= 0
        total_load= 0
        error_indication, error_status, error_index, var_binds = await bulk_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            0, 50,
            ObjectType(ObjectIdentity(oid))
            )

        if error_indication:
            return
        elif error_status:
            return
        else:
            request_oid= oid[0:22]
            for oid_val, value in var_binds:
                response_oid= str(oid_val[0:11])         
                if response_oid == request_oid:
                    cores +=1 
                    total_load += value
                else:
                    break

        cpu_usage_average= total_load / cores
        return cpu_usage_average
                
    async def get_memory_index(self, memory_idx_OID, server_ip, server_port):
        phys_mem_index = []
        error_indication, error_status, error_index, var_binds = await bulk_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            0, 50,
            ObjectType(ObjectIdentity(memory_idx_OID))
            )
    
        if error_indication:
            return
        elif error_status:
            return
        else:
            for oid_val, value in var_binds:
                
                if str(value) == "Physical memory":
                    idx= oid_val[-1]
                    phys_mem_index.append(idx)
                else: 
                    break
        return phys_mem_index         

    async def get_ram_usage(self, memory_used_OID, memory_idx_list, server_ip, server_port):    
        used_memory= 0

        for idx in memory_idx_list:
            oid_with_idx= memory_used_OID + "." + str(idx)
            error_indication, error_status, error_index, var_binds= await get_cmd(
                SnmpEngine(),
                CommunityData('public'),
                await UdpTransportTarget.create((server_ip, server_port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid_with_idx))
                )

            if error_indication:
                return
            elif error_status:
                return
            else:
                value= var_binds[0][1]
                used_memory += int(value)

        return used_memory

    async def get_ram_total_capacity(self, memory_size_OID, memory_idx_list, server_ip, server_port):
        total_memory= 0

        for idx in memory_idx_list:
            oid_with_idx= memory_size_OID + "." + str(idx)
            error_indication, error_status, error_index, var_binds= await get_cmd(
                SnmpEngine(),
                CommunityData('public'),
                await UdpTransportTarget.create((server_ip, server_port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid_with_idx))
                )
    
            if error_indication:
                return
            elif error_status:
                return
            else:
                value= var_binds[0][1]
                total_memory += int(value)
        return total_memory

    async def get_disk_info(self, disk_idx_OID, server_ip, server_port):    #try to get rid of lists and pack everything directly into a dict 
        idx_sector_dict= {}
        partition_index_list= []
        sector_size_list= []

        error_indication, error_status, error_index, var_binds = await bulk_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            0, 50,
            ObjectType(ObjectIdentity(disk_idx_OID))
            )

        if error_indication:
            return
        elif error_status:
            return
        else:
            for oid_val, value in var_binds:
                val = str(value)
                if val[0] == "/":
                    oid_split= str(oid_val).split(".")
                    idx= oid_split[-1]
                    partition_index_list.append(int(idx))

                match str(value):
                    case "128":
                        sector_size_list.append(int(value))
                    case "256":
                        sector_size_list.append(int(value))
                    case "512":
                        sector_size_list.append(int(value))
                    case "520":
                        sector_size_list.append(int(value))
                    case "528":
                        sector_size_list.append(int(value))
                    case "1024":
                        sector_size_list.append(int(value))
                    case "2048":
                        sector_size_list.append(int(value))
                    case "4096":
                        sector_size_list.append(int(value))
                    case "4112":
                        sector_size_list.append(int(value))
                    case "4160":
                        sector_size_list.append(int(value))
                    
        return dict(zip(partition_index_list, sector_size_list))

    async def get_disk_usage(self, storage_used_OID, disk_info, server_ip, server_port):
        used_storage= 0
  
        for idx, sector_size in disk_info.items():
            oid_with_idx= storage_used_OID + "." + str(idx)
            error_indication, error_status, error_index, var_binds= await get_cmd(
                SnmpEngine(),
                CommunityData('public'),
                await UdpTransportTarget.create((server_ip, server_port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid_with_idx))
                )
    
            if error_indication:
                return
            elif error_status:
                return
            else:
                value= var_binds[0][1]
                total = int(value) * int(sector_size)
                used_storage += total

        return used_storage

    async def get_disk_total_capacity(self, storage_total_OID, disk_info, server_ip, server_port):
        total_storage= 0

        for idx, sector_size in disk_info.items():
            oid_with_idx= storage_total_OID + "." + str(idx)
            error_indication, error_status, error_index, var_binds= await get_cmd(
                SnmpEngine(),
                CommunityData('public'),
                await UdpTransportTarget.create((server_ip, server_port)),
                ContextData(),
                ObjectType(ObjectIdentity(oid_with_idx))
                )
    
            if error_indication:
                return
            elif error_status:
                return
            else:
                value= var_binds[0][1]
                total = int(value) * int(sector_size)
                total_storage += total
        
        return total_storage

    # async def get_network_down_speed(self, server_ip, server_port= 161):
    #     pass
    #     #need to take a a counter and b counter and calculate the speed over time. 

    # async def get_network_up_speed(self, server_ip, server_port= 161):
    #     pass
    #     #need to take a a counter and b counter and calculate the speed over time. 

if __name__ == "__main__":
    temp_obj= DashboardSNMP()
    info= asyncio.run(temp_obj.get_disk_info("1.3.6.1.2.1.25.2.3.1.3", "192.168.10.10", 161))
