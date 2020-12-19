'''A YAML utility module zaheer'''
#!/usr/bin/env python

import yaml
import sys

class YamlUtil:
    def __init__(self, name, debug_flag = False):
        self.name = name
        self.debug_flag = debug_flag

    def set_debug(self, debug_flag):
        self.debug_flag = debug_flag
    def get_debug(self, debug_flag):
        return self.debug_flag

    # ----------------------------------- yamlLoader ---------------------------
    # load yaml file into dict and return exception if encounters any errors
    def yaml_loader(self, yaml_filename):
        '''yaml loader'''
        with open(yaml_filename, 'r') as stream:
            try:
                # The FullLoader parameter handles the conversion from YAML
                # scalar values to Python the dictionary format
                yamlObj = yaml.load(stream, Loader=yaml.FullLoader)

            except yaml.YAMLError as exc: # <class 'yaml.parser.ParserError'>
                return exc


        return yamlObj

    # --------------------------------- yaml_count_key -------------------------
    # count number of keys
    def yaml_count_key(self, yaml_data, key):
        count = 0
        if isinstance(yaml_data, dict):
            for k, val in yaml_data.iteritems():
                if k == s:
                    count += 1

                count += yaml_count(val, s)
        elif isinstance(yaml_data, list):
            for l in yaml_data:
                count += yaml_count(l, s)
        return count

    # ----------------------------------- keyExist -----------------------------
    # does key exist?
    def keyExist(self, yamlObj, key):
        '''Does the key exist in this YAML object, yamlObj?'''
        rc = key in yamlObj
        if self.debug_flag:
            if rc:
                print('DEBUG: key = ' + key + ' existed')
            else:
                print('DEBUG: key = ' + key + ' is missing')
        return rc

    # ---------------------------------- pretty_xml ----------------------------
    # def pretty_xml(self, fname):
        # '''print the nicely formatted XML file'''
        # assert fname is not None
        # bs = BeautifulSoup(open(fname), 'xml')
        #pretty_soup = soup_prettify2(bs, desired_indent=4)
        #print(pretty_soup)

    # ----------------------------- dump_yaml_obj ------------------------------
    def dump_yaml_obj(self, yam_obj):
       '''Dump a YAML object'''
       print(yaml.dump( out, default_flow_style=False, default_style='    ' ))

    # ----------------------------- dump_yaml_file -----------------------------
    def dump_yaml_file(self, filename):
        '''Dump the whole YAML file out'''
        with open(filename, 'r') as stream:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            out = yaml.load(stream, Loader=yaml.FullLoader)
            #print(out)
            print(yaml.dump( out, default_flow_style=False, default_style='' ))
            components0 = out['COMPONENTS'][0]
            print(components0)
            
            components0properties=components0['PROPERTIES']
            print("\nKEY="+components0properties['KEY'])
            
    ### ------------------------------ reuse_key -------------------------------
    def reuse_key(self, key_name, yaml_obj, key_defined, yaml_util_obj):
        '''
            If key defined in yaml object, then use.
            Otherwise, check the previsouly defined key
        '''
        rc = key_defined

        if not yaml_util_obj.keyExist(yaml_obj, key_name): ### if it does not exist
            if len(key_defined) > 0: ### it is ok, uses previous defined one 
                if self.debug_flag:
                    print('DEBUG: use previous defined ' + key_name + ' = ' + key_defined)
            else:
                print(yaml.dump(yaml_obj))
                print("\nMissing key: " + key_name + "\n")
                sys.exit(1)
        else: ### user defined it, then  use it
            rc = yaml_obj[key_name]   

        return rc

# ---------------------------------- testing -------------------------------
def testing(filename):

    with open(filename, 'r') as stream:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        out = yaml.load(stream, Loader=yaml.FullLoader)
        components = out['COMPONENTS']
        # print(type(components)) # list
        # print(len(components))
        # print(type(components[0])) # dict
        # print(components[0]['CG_APP_NAME'])

        print(type(out['PIPELINE'])) # dict
        print(out['PIPELINE'])
        print(type(out['PIPELINE']['CG_APP_NAME'])) # str
        print(out['PIPELINE']['CG_APP_NAME'])

def main(argv):
    print("Running " + __file__ + " main()")
    if len(argv)  < 2:
        print("\nERROR: missing input YAML file name\n")
        sys.exit(1)

    yaml_fname = argv[1]

    yutil = YamlUtil(__file__)
    #yutil.pretty_xml(yaml_fname)
    yaml_obj = yutil.yaml_loader(yaml_fname)
    yutil.dump_yaml_file(yaml_fname)
    testing(yaml_fname)


if __name__ == "__main__":
    main(sys.argv)
