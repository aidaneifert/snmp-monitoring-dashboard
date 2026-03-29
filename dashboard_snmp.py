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
                
    async def get_uptime(self, oid, server_ip, server_port= 161):
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
    
    async def get_cpu_usage(self, oid, server_ip, server_port= 161):
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
                
    async def get_memory_index(self, oid, server_ip, server_port= 161):
        phys_mem_index = []
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
            for oid_val, value in var_binds:
                
                if str(value) == "Physical memory":
                    idx= oid_val[-1]
                    phys_mem_index.append(idx)
                else: 
                    break
        return phys_mem_index         

    async def get_ram_usage(self, oid, server_ip, server_port= 161):    
        used_memory= 0
        storage_desc_oid, storage_used_oid= oid
        mem_index= await self.get_memory_index(storage_desc_oid, server_ip, server_port= server_port)

        for idx in mem_index:
            oid_with_idx= storage_used_oid + "." + str(idx)
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

    async def get_ram_total_capacity(self, oid, server_ip, server_port= 161):
        total_memory= 0
        storage_desc_oid, storage_total_oid= oid
        mem_index= await self.get_memory_index(storage_desc_oid, server_ip, server_port= server_port)

        for idx in mem_index:
            oid_with_idx= storage_total_oid + "." + str(idx)
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

    async def get_disk_index(self, oid, server_ip, server_port= 161):
        partition_index = []
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
            for oid_val, value in var_binds:
                val = str(value)
                if val[0] == "/":
                    idx= oid_val[-1]
                    partition_index.append(idx)
        return partition_index

    async def get_disk_sector_size(self, oid, server_ip, server_port= 161):
        storage_desc_oid, sector_size_oid= oid
        partition_index= await self.get_disk_index(storage_desc_oid, server_ip, server_port= server_port)
        sector_sizes= []
        for idx in partition_index:
            oid_with_idx= sector_size_oid + "." + str(idx)
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
                sector_sizes.append(var_binds[0][1])
        print(sector_sizes)
        return sector_sizes

    async def get_disk_usage(self, oid, sector_sizes, server_ip, server_port= 161):
        used_storage= 0
        storage_desc_oid, storage_used_oid= oid
        partition_index= await self.get_disk_index(storage_desc_oid, server_ip, server_port= server_port)

        for idx in partition_index:
            oid_with_idx= storage_used_oid + "." + str(idx)
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

                sector_size= sector_sizes.pop()
                storage_bytes= sector_size * sector_size

                used_storage += int(storage_bytes)
        return used_storage

    async def get_disk_total_capacity(self, oid, sector_sizes, server_ip, server_port= 161):
        total_storage= 0
        storage_desc_oid, storage_used_oid= oid
        partition_index= await self.get_disk_index(storage_desc_oid, server_ip, server_port= server_port)

        for idx in partition_index:
            oid_with_idx= storage_used_oid + "." + str(idx)
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
                
                sector_size= sector_sizes.pop()
                storage_bytes= sector_size * sector_size

                total_storage += int(value)
        return total_storage
        
    async def get_network_down_speed(self, server_ip, server_port= 161):
        pass
        #need to take a a counter and b counter and calculate the speed over time. 

    async def get_network_up_speed(self, server_ip, server_port= 161):
        pass
        #need to take a a counter and b counter and calculate the speed over time. 

