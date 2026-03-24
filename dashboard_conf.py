import yaml

class DashboardConfig:
    def __init__(self):
        self.config= "dashboard_devices.yaml"
        self.oid_table= "vendor_oid.yaml"

    def read_dashboard_config(self):
        with open(self.config, 'r') as config_file:
            config_data= yaml.safe_load(config_file)
        return config_data
    
    def read_oid_table(self):
        with open(self.oid_table, 'r') as config_file:
            config_data= yaml.safe_load(config_file)
        return config_data
