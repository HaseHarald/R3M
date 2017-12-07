# -*- coding: utf-8 -*-

import yaml
import sys

class MyConfigParser(dict):
    '''A custom config parser to ensure, all required data is provided.
    '''
    def __init__(self, config_file):
        ''' Specify the needed values
        '''
        required_values = {
            'SMTP': {
                'server': str,
                'port': int,
                'starttls': bool,
                'user': str,
                'password': str
            },
            'Mail': {
                'from': str,
                'subject': str,
                'message': str
            },
            'Recipients': {
                # TODO: Make freely choosable keys possible
#                str: {
#                    'name': str,
#                    'mail': str
#                }
            }
        }
        
        config = self.parse_config(config_file)
        self.validate_config(config, required_values)
                
        self.update(config)
        
    def parse_config(self, config_file):
    
        try:
            with open(config_file) as conf_file:
                conf = yaml.safe_load(conf_file)
        except yaml.scanner.ScannerError as scann_err:
            print('Maleformed config file.', file=sys.stderr)
            print(scann_err, file=sys.stderr)
            exit(1)
        except (FileNotFoundError, PermissionError) as file_err:
            print('Could not open config file.', file=sys.stderr)
            print(file_err, file=sys.stderr)
            exit(1)
    
        return conf
    
    def validate_config(self, config, required_values):
        '''Make sure every required option is set.
        '''
        for req_key, req_type in required_values.items():
            if req_key not in config:
                raise ValueError("Missing key %s in config file" % req_key)
            
            if (type(req_type) == dict) and (type(config[req_key]) == dict):
                self.validate_config(config[req_key], required_values[req_key])
            elif (type(req_type) == dict) and (type(config[req_key]) != dict):
                raise ValueError("Wrong type %s in config file. Expected section." % req_key)
            elif type(config[req_key]) != req_type:
                raise ValueError("Wrong type %s in config file." % req_key)
            
