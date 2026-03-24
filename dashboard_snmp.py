import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

class DashboardSNMP:
    async def get_uptime(self, server_ip, server_port= 161):       # Universal OID= 1.3.6.1.2.1.25.1.1.0
        error_indication, error_status, error_index, var_binds= await get_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            ObjectType(ObjectIdentity('1.3.6.1.2.1.25.1.1.0'))
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

    async def get_cpu_usage(self, server_ip, server_port= 161):        # Universal OID= 1.3.6.1.2.1.25.3.3.1.2
        error_indication, error_status, error_index, var_binds= await get_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            ObjectType(ObjectIdentity('.1.3.6.1.4.1.2021.10.1.3.1'))
            )
        
        if error_indication:
            return error_indication
        elif error_status:
            return error_status
        elif error_status:
            return error_index
        elif var_binds:
            value_object= var_binds[0][1]
            raw_cpu_usage= str(value_object)
            return raw_cpu_usage
        
    async def get_cpu_cores(self, server_ip, server_port= 161):         # Universal OID= 1.3.6.1.2.1.25.3.3.1.2
        cores= 0
        error_indication, error_status, error_index, var_binds= await get_cmd(
            SnmpEngine(),
            CommunityData('public'),
            await UdpTransportTarget.create((server_ip, server_port)),
            ContextData(),
            ObjectType(ObjectIdentity('.1.3.6.1.2.1.25.3.3.1')),
            lexicographicMode=False
            )        
        if error_indication:
            return error_indication
        elif error_status:
            return error_status
        elif error_status:
            return error_index
        elif var_binds:
            core_count= cores + 1
            return core_count
                
    def get_ram_usage(self, server_ip, server_port= 161):        # Universal OID TOTAL RAM= 1.3.6.1.2.1.25.2.2.0
        pass
        #need to walk the table and subtract storage used from total storage

    def get_disk_usage(self, server_ip, server_port= 161):       # Universal IOD for disk table= 1.3.6.1.2.1.25.2.3.1
        pass
        #need to walk the table and subtract storage used from total storage

    def get_network_down_speed(self, server_ip, server_port= 161):       # Universal IOD= 1.3.6.1.2.1.31.1.1.1.6
        pass
        #need to take a a counter and b counter and calculate the speed over time. 

    def get_network_up_speed(self, server_ip, server_port= 161):      # Universal IOD= 1.3.6.1.2.1.31.1.1.1.10
        pass
        #need to take a a counter and b counter and calculate the speed over time. 
