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
        print(oid)
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
        print(oid)
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
            return value_object
        
    async def get_cpu_cores(self, oid, server_ip, server_port= 161):
        cores= 0
        generator= next_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False
            )        
        async for error_indication, error_status, error_index, var_binds in generator:
            if error_indication:
                return error_indication
            elif error_status:
                return error_status
            elif error_status:
                return error_index
            elif var_binds:
                core_count= cores + 1
        print (core_count)
        return core_count
        
    def get_ram_usage(self, server_ip, server_port= 161):
        pass
        #need to walk the table and subtract storage used from total storage

    def get_disk_usage(self, server_ip, server_port= 161):
        pass
        #need to walk the table and subtract storage used from total storage

    def get_network_down_speed(self, server_ip, server_port= 161):
        pass
        #need to take a a counter and b counter and calculate the speed over time. 

    def get_network_up_speed(self, server_ip, server_port= 161):
        pass
        #need to take a a counter and b counter and calculate the speed over time. 

