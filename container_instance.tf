
## Availability domains
data "oci_identity_availability_domain" "ad" {
  compartment_id = var.tenancy_ocid
  ad_number      = 1
}


resource oci_container_instances_container_instance starter_container_instance {
  availability_domain = data.oci_identity_availability_domain.ad.name
  compartment_id      = var.compartment_ocid
  container_restart_policy = "ALWAYS"
  containers {
    display_name = "wordpress"
    image_url = "wordpress"
    is_resource_principal_disabled = "false"
    environment_variables = {
      "WORDPRESS_DB_HOST" = "127.0.0.1",
      "WORDPRESS_DB_USER" = "wordpress",
      "WORDPRESS_DB_PASSWORD" = "wordpress",
      "WORDPRESS_DB_NAME" = "wordpress"
    }    
  }
  containers {
    display_name = "mySQL"
    image_url = "mysql:8.0.21"
    is_resource_principal_disabled = "false"
    environment_variables = {
      "MYSQL_ROOT_PASSWORD" = "wordpressonmysql",
      "MYSQL_DATABASE" = "wordpress",
      "MYSQL_USER" = "wordpress",
      "MYSQL_PASSWORD" = "wordpress"
    }   
    }    

    
  display_name = "Wordpress"
  graceful_shutdown_timeout_in_seconds = "0"
  shape                                = var.shape
  shape_config {
    memory_in_gbs = var.instance_shape_config_memory_in_gbs
    ocpus         = var.instance_ocpus
  }

state = "ACTIVE"
  vnics {
    display_name           = "${var.prefix}-ci"
    hostname_label         = "${var.prefix}-ci"
    is_public_ip_assigned  = "true"
    skip_source_dest_check = "true"
    subnet_id              = data.oci_core_subnet.starter_subnet.id
  }


    
  }  
  

data "oci_container_instances_container_instance" "wordpress" {
    #Required
    container_instance_id = oci_container_instances_container_instance.starter_container_instance.id
}

data "oci_core_vnic" "test_vnic" {
    #Required
    vnic_id = data.oci_container_instances_container_instance.wordpress.vnics[0].vnic_id
}

output "ip_endpoint" {
    value       = "Endpoint is ${data.oci_core_vnic.test_vnic.public_ip_address}"
}
