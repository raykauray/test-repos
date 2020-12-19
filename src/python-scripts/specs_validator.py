#!/usr/bin/env python

import sys
import yaml
from yaml_util import YamlUtil

class specsValidator:
    def __init__(self, name, debug_flag = False):
        self.name = name
        self.debug_flag = debug_flag
        self.project_key_defined = ''
        self.project_name_defined = ''
        self.project_description_defined = ''
        self.build_plan_os_defined = ''
        self.repository_defined = ''

    def set_debug(self, debug_flag):
        self.debug_flag = debug_flag
    def get_debug(self, debug_flag):
        return self.debug_flag

    ### --------------------------- validate_main_keys -------------------------
    def validate_main_keys(self, yaml_obj, yaml_util_obj):
        mainKey = [
            "GLOBAL_PROPERTIES",
            "COMPONENTS",
            "PIPELINE"]

        for i in mainKey:
            if not yaml_util_obj.keyExist(yaml_obj, i):
                print("\nMissing key: " + i + "\n")
                exit(1)
         

    ### ------------------ validate_global_properties --------------------------
    def validate_global_properties(self, yaml_obj, yaml_util_obj):
        '''Validate global properties key words'''    
        global_properties = [
            "APP_NAME",
            "APP_REPOSITORY",
            "ATM_ID",
            "PROJECT_KEY",
            "XLD_HOST",
            "XLD_PKG_REPO"
            ]

        if self.debug_flag:
            print('\nDEBUG: validating GLOBAL_PROPERTIES')

        for i in global_properties:
            if not yaml_util_obj.keyExist(yaml_obj, i):
                print(yaml.dump(yaml_obj))
                print("\nMissing global properties key: " + i + "\n")
                sys.exit(1)
                
    ### ------------------------------ reuse_key -------------------------------
    def reuse_key(self, key_name, yaml_obj, key_defined, yaml_util_obj):
        '''reuse key from defined '''

        if not yaml_util_obj.keyExist(yaml_obj, key_name): ### if not defined
            if len(key_defined) > 0: ### it is ok, uses previous defined one 
                if self.debug_flag:
                    print('DEBUG: use previous defined PROJECT_KEY = ' + key_defined)
            else:
                print(yaml.dump(yaml_obj))
                print("\nMissing key: " + key_name + "\n")
                sys.exit(1)
                return key_defined 
        else: ### user defined it, then  use it
            return yaml_obj[key_name]                

    ### ----------------------- validate_reusable_key --------------------------
    def validate_reusable_key(self, yaml_obj, yaml_util_obj):
        '''validate all reusable keys that will be inherited to next plan'''
        reusable_key = [     ### the following keys
            "BUILD_PLAN_OS", ### can use previous defined one
            "REPOSITORY"
            ]

        for i in reusable_key:   
            if i == 'BUILD_PLAN_OS':
                self.build_plan_os_defined = yaml_util_obj.reuse_key(i,
                    yaml_obj, self.build_plan_os_defined, yaml_util_obj)

            elif i == 'REPOSITORY':
                self.repository_defined = yaml_util_obj.reuse_key(i,
                    yaml_obj, self.repository_defined, yaml_util_obj)

    ### ------------------------- validate_component --------------------------------
    def validate_component(self, yaml_obj, yaml_util_obj):
        '''Validate component key words'''
        component_key = [
            "CG_APP_NAME",
            "CG_COMP_NAME",
            "PLAN_KEY",
            "PROPERTIES"
            ]

        properties_key = [
            "KEY",
            "NAME"
            ]

        for i in component_key:
            if not yaml_util_obj.keyExist(yaml_obj, i):
                print(yaml.dump(yaml_obj))
                print("\nMissing key: " + i + "\n")
                sys.exit(1)

            if i == 'PROPERTIES':
                for i in properties_key:
                    if not yaml_util_obj.keyExist(yaml_obj['PROPERTIES'], i):
                        print(yaml.dump(yaml_obj))
                        print("\nMissing COMPONENT.PROPERTIES key: " + i + "\n")
                        sys.exit(1)       

        self.validate_reusable_key(yaml_obj, yaml_util_obj)

    ### ----------------------- validate_pipeline ------------------------------
    def validate_pipeline(self, yaml_obj, yaml_util_obj):
        '''Validate Pipeline key words'''    
        pipeline = [
            "CG_APP_NAME",
            "PLAN_KEY"
            ]

        if self.debug_flag:
            print('\nDEBUG: validating PIPELINE')

        for i in pipeline:
            if not yaml_util_obj.keyExist(yaml_obj, i):
                print(yaml.dump(yaml_obj))
                print("\nMissing key: " + i + "\n")
                sys.exit(1)
                
        self.validate_reusable_key(yaml_obj, yaml_util_obj)
              
    ### ----------------------------- length_checker ---------------------------
    def length_checker(self, yaml_obj):
        '''It is a recursive method to do the real work for lenth_check'''
       
        if isinstance(yaml_obj, dict):
            for i in yaml_obj:
                if len(i) > 256:
                    print("ERROR: length is > 256, " + i)
                    sys.exit(1)
                self.length_checker(yaml_obj[i])
        elif isinstance(yaml_obj, list):
            for i in yaml_obj:
                self.length_checker(i)    
        elif isinstance(yaml_obj, str):
            if len(yaml_obj) > 256:
                print("ERROR: length is > 256, " + yaml_obj)
                sys.exit(1)
        else:
            print("ERROR: unknown type: " + str(type(yaml_obj)))
            sys.exit(1)
            

    ### ------------------------------ length_check ----------------------------
    def length_check(self, yaml_obj):
        '''Ensure all keys/values lengths are < 256 bytes'''
        
        for i in yaml_obj:
            self.length_checker(yaml_obj[i])

    ### ------------------------------- validate -----------------------------------
    def validate(self, yaml_obj, yaml_util_obj):

        self.validate_main_keys(yaml_obj, yaml_util_obj)
        
        self.validate_global_properties(yaml_obj['GLOBAL_PROPERTIES'], yaml_util_obj)

        cnt = 0
        for i in yaml_obj["COMPONENTS"]:
            if self.debug_flag:
                print('\nDEBUG: checking components array[' + str(cnt) + ']')
            self.validate_component(i, yaml_util_obj)
            cnt += 1

        self.validate_pipeline(yaml_obj['PIPELINE'], yaml_util_obj)
        self.length_check(yaml_obj)
        
        return True

### --------------------------------- Testing ----------------------------------
def testing(yamlFile, yaml_util_obj, debug_flag):
    yaml_obj = yaml_util_obj.yaml_loader(yamlFile)
    checker_obj = specsValidator(__file__, debug_flag)
    checker_obj.validate(yaml_obj, yaml_util_obj)

def main(argv, debug_flag=False):
    print("Running " + __file__ + " main()")
    if len(argv)  < 2:
        print("\nERROR: missing input YAML file name\n")
        sys.exit(1)

    y_util = YamlUtil('from ' + __file__, debug_flag)
    if debug_flag:
        print("\nDEBUG: validating file = " + argv[1] + '\n')
    testing(argv[1], y_util, debug_flag)


if __name__ == "__main__":
    main(sys.argv, True)

