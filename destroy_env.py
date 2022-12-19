
import os
import subprocess
import getpass
import sys


"""
This function will check if the .oci config in the default location and if not prompt for the locatio of the
file.
"""
def check_oci_config():
        user = getpass.getuser()
        path = "/Users/" + user + "/.oci/config"
        path1 = "/home/" + user + "/.oci/config"
        config_status = os.path.exists(path)
        config_status1 = os.path.exists(path1)
        if config_status == True:
            config_file = "/Users/" + user + "/.oci/config"
           
        elif config_status1 == True:
            config_file = "/home/" + user + "/.oci/config"
        else:
            config_file_exist = False
            while config_file_exist == False:
                inp = input('what is the location of oci config file: ')
                config_status = os.path.exists(inp)
                if config_status == True:
                    config_file = inp
                    config_file_exist = True
        return config_file


"""
This function will check verify if all paramters are in the .oci config
"""

def verify_config(config_file):
    print(config_file)
    config_paramaters = ['user', 'fingerprint', 'key_file', 'tenancy', 'region']
    for parameter in config_paramaters:
        if parameter not in config_file:
            print("{} not in config file".format(parameter))
            valid_config = False
    if valid_config == False:
        exit()


"""
This function will check read all the parameter in oci config
"""
def read_config(config_file):
    tf_dict = {}
    verify_config_file =[]
    with open(config_file) as f:
        for line in f:
            if "[DEFAULT]" not in line:
                tf_string = line.strip()
                tf_variable = tf_string.split('=') 
                verify_config_file.append(tf_variable[0])
                tf_dict[tf_variable[0]] = tf_variable[1]
    return tf_dict
   

"""
This function will export all paramaters in oci config as TF_VAR varaiables
"""

def get_compartment_id():
    compartment_id = input('enter the compartment_id for deploying the container instance: ')
    return(compartment_id)



def export_tf_var(tf_dict):
    compartment_id = get_compartment_id()
    os.environ["TF_VAR_compartment_ocid"] = compartment_id
    os.environ["TF_VAR_user_ocid"] = tf_dict["user"]
    os.environ["TF_VAR_fingerprint"] = tf_dict["fingerprint"]
    os.environ["TF_VAR_tenancy_ocid"] = tf_dict["tenancy"]
    os.environ["TF_VAR_region"] = tf_dict["region"]
    os.environ["TF_VAR_private_key_path"] = tf_dict["key_file"]



"""
This function will run the terraform
"""

def run_terrafom():
    process = subprocess.Popen(["terraform", "destroy", "-auto-approve"],stdout=subprocess.PIPE, bufsize=1)
    for line in iter(process.stdout.readline, b''):
        print(line.rstrip())
    process.stdout.close()
    process.wait()



def main():
    config_file = check_oci_config()
    tf_dict = read_config(config_file)
    export_tf_var(tf_dict)
    run_terrafom()




if __name__ == "__main__":
    main()