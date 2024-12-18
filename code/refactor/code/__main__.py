import os

from configuration.appconfig import AppConfig

if __name__ != '__main__':
    exit(1)

app_config = AppConfig.load_from_yaml(application_root_path= os.getcwd(),config_file_path= "/secure-storage/env.yaml")

print(app_config.data_encryption_key)