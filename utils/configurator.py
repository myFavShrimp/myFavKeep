from settings import ENV, DevelopmentConfig, ProductionConfig


def get_config():
    if ENV == 'development':
        return DevelopmentConfig()
    elif ENV == 'production':
        return ProductionConfig()
    else:
        print('\033[91m', 'ERROR!! :',
              'The environment (ENV) must be set to either \'production\' or \'development\' in the settings file')
        exit()


def get_config_name():
    return ENV
