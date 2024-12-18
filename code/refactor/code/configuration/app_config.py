from dataclasses import dataclass
import yaml

@dataclass
class AppConfig:
    """
        application configuration data contract
    """

    data_encryption_key: str
    """
        data encryption key
    """

    result_container_directory_path: str
    """
        result container directory path
    """

    classifiers_container_directory_path: str
    """
        classifiers container directory path
    """

    application_root_path: str
    """
        root path of the application
    """

    @staticmethod
    def load_from_yaml(application_root_path: str, config_file_path: str) -> object:
        """
        create an instance from a yaml configuration file
        :param application_root_path: application root path
        :param config_file_path: yaml file path from the root path
        :return:
        AppConfig: an instance of configuration class
        """

        try:
            with open(file= f"{application_root_path}{config_file_path}") as file:
                config_file_content = yaml.safe_load(stream= file)

                return AppConfig(
                    data_encryption_key=config_file_content["data-encryption-key"],
                    result_container_directory_path=config_file_content["result-container-directory-path"],
                    classifiers_container_directory_path=config_file_content["classifiers-container-directory-path"],
                    application_root_path=application_root_path,
                )
        except Exception as _:
            raise Exception("Fail to load the configuration file")