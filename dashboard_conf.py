import yaml

class DashboardConfig:
    def __init__(self):
        self.config= "dashboard_devices.yaml"

    def read_dashboard_config(self):
        with open(self.config, 'r') as config_file:
            config_data= yaml.safe_load(config_file)
        return config_data
    
