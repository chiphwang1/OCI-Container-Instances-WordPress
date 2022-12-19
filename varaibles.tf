variable tenancy_ocid {
}
variable compartment_ocid {
     
}

variable "region" {
 
}

variable "fingerprint" {
 
}

variable "private_key_path" {
  
}

variable "user_ocid" {
   
} 



# Prefix
variable prefix { default = "wordpress" }



# Compute Instance size
variable "shape" { default = "CI.Standard.E3.Flex"}
variable "instance_ocpus" { default = 1 }
variable "instance_shape_config_memory_in_gbs" { default = 8 }




