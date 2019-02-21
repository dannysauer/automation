variable "auth_url" {}
variable "domain_name" {}
variable "region_name" {}
variable "project_name" {}
variable "user_name" {}
variable "password" {}
variable "image_name" {}
variable "internal_net" {}
variable "external_net" {}
variable "admin_size" {}
variable "master_size" {}
variable "mons" {}
variable "worker_size" {}
variable "osds" {}
variable "regcode_SLES" {}
variable "regcode_SES" {}
variable "identifier" {}
variable "volumeSize" {}

provider "openstack" {
  domain_name = "${var.domain_name}"
  tenant_name = "${var.project_name}"
  user_name   = "${var.user_name}"
  password    = "${var.password}"
  auth_url    = "${var.auth_url}"
  insecure    = "true"
}

data "template_file" "admin" {
  template = "${file("admin.tpl")}"

  vars {
    regcode_SLES    = "${var.regcode_SLES}"
    regcode_SES    = "${var.regcode_SES}"
  }
}

data "template_file" "mon" {
  template = "${file("mon.tpl")}"

  vars {
    regcode_SLES    = "${var.regcode_SLES}"
    regcode_SES    = "${var.regcode_SES}"
    saltmaster = "${openstack_compute_instance_v2.admin.name}"
  }
}

data "template_file" "osd" {
  template = "${file("osd.tpl")}"

  vars {
    regcode_SLES    = "${var.regcode_SLES}"
    regcode_SES    = "${var.regcode_SES}"
    saltmaster = "${openstack_compute_instance_v2.admin.name}"
  }
}

resource "openstack_compute_keypair_v2" "keypair" {
  name       = "ses-ssh-${var.identifier}"
  region     = "${var.region_name}"
  public_key = "${file("ssh/id_ses.pub")}"
}

resource "openstack_compute_secgroup_v2" "secgroup_base" {
  name        = "ses-base-${var.identifier}"
  region      = "${var.region_name}"
  description = "Basic security group for ses"

  rule {
    from_port   = -1
    to_port     = -1
    ip_protocol = "icmp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 2379
    to_port     = 2379
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_secgroup_v2" "secgroup_admin" {
  name        = "ses-admin-${var.identifier}"
  region      = "${var.region_name}"
  description = "ses security group for admin"

  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 443
    to_port     = 443
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 4505
    to_port     = 4506
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 389
    to_port     = 389
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 6780
    to_port     = 7500
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_secgroup_v2" "secgroup_mon" {
  name        = "ses-mon-${var.identifier}"
  region      = "${var.region_name}"
  description = "ses security group for mons"

  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 2380
    to_port     = 2380
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 6443
    to_port     = 6444
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 8285
    to_port     = 8285
    ip_protocol = "udp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 30000
    to_port     = 32768
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 30000
    to_port     = 32768
    ip_protocol = "udp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 6780
    to_port     = 7500
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_secgroup_v2" "secgroup_osd" {
  name        = "ses-osd-${var.identifier}"
  region      = "${var.region_name}"
  description = "ses security group for osds"

  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 443
    to_port     = 443
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 8080
    to_port     = 8080
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 8081
    to_port     = 8081
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 2380
    to_port     = 2380
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 10250
    to_port     = 10250
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 8285
    to_port     = 8285
    ip_protocol = "udp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 30000
    to_port     = 32768
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 30000
    to_port     = 32768
    ip_protocol = "udp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 6780
    to_port     = 7500
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }
}

resource "openstack_compute_instance_v2" "admin" {
  name       = "ses-admin"
  region     = "${var.region_name}"
  image_name = "${var.image_name}"

  connection {
    private_key = "${file("ssh/id_ses.pub")}"
  }

  flavor_name = "${var.admin_size}"
  key_pair    = "ses-ssh-${var.identifier}"

  network {
    name = "${var.internal_net}"
  }

  security_groups = [
    "${openstack_compute_secgroup_v2.secgroup_base.name}",
    "${openstack_compute_secgroup_v2.secgroup_admin.name}",
  ]

  user_data = "${data.template_file.admin.rendered}"
}

resource "null_resource" "deepsea" {
  connection {
    user        = "sles"
    type        = "ssh"
    host        = "${openstack_compute_floatingip_associate_v2.admin_ext_ip.floating_ip}"
    private_key = "${file("ssh/id_ses")}"
  }

  provisioner "file" {
    source      = "deepsea.sh"
    destination = "/tmp/deepsea.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo -u root chmod +x /tmp/deepsea.sh",
      "sudo -u root /tmp/deepsea.sh",
    ]
  }

  depends_on = ["openstack_compute_instance_v2.admin", "openstack_compute_instance_v2.osd",
    "openstack_compute_instance_v2.mon",
    "openstack_compute_volume_attach_v2.salt-minion-attach",
  ]
}

data "external" "cephsecret" {
  program    = ["bash", "cephsecret.sh", "${openstack_networking_floatingip_v2.admin_ext.address}"]
  depends_on = ["null_resource.deepsea"]
}

resource "openstack_networking_floatingip_v2" "admin_ext" {
  pool = "${var.external_net}"
}

resource "openstack_compute_floatingip_associate_v2" "admin_ext_ip" {
  floating_ip = "${openstack_networking_floatingip_v2.admin_ext.address}"
  instance_id = "${openstack_compute_instance_v2.admin.id}"
}

resource "openstack_compute_instance_v2" "mon" {
  count      = "${var.mons}"
  name       = "ses-mon${count.index}"
  region     = "${var.region_name}"
  image_name = "${var.image_name}"

  connection {
    private_key = "${file("ssh/id_ses.pub")}"
  }

  flavor_name = "${var.master_size}"
  key_pair    = "ses-ssh-${var.identifier}"

  network {
    name = "${var.internal_net}"
  }

  security_groups = [
    "${openstack_compute_secgroup_v2.secgroup_base.name}",
    "${openstack_compute_secgroup_v2.secgroup_mon.name}",
  ]

  user_data = "${data.template_file.mon.rendered}"
}

resource "openstack_networking_floatingip_v2" "mon_ext" {
  count = "${var.mons}"
  pool  = "${var.external_net}"
}

resource "openstack_compute_floatingip_associate_v2" "mon_ext_ip" {
  count       = "${var.mons}"
  floating_ip = "${element(openstack_networking_floatingip_v2.mon_ext.*.address, count.index)}"
  instance_id = "${element(openstack_compute_instance_v2.mon.*.id, count.index)}"
}

resource "openstack_blockstorage_volume_v2" "osd-blk" {
  count = "${var.osds}"
  size  = "${var.volumeSize}"
  name  = "osd-blk${count.index}"
}

resource "openstack_compute_volume_attach_v2" "salt-minion-attach" {
  count       = "${var.osds}"
  instance_id = "${element(openstack_compute_instance_v2.osd.*.id, count.index)}"
  volume_id   = "${element(openstack_blockstorage_volume_v2.osd-blk.*.id, count.index)}"
}

resource "openstack_compute_instance_v2" "osd" {
  count      = "${var.osds}"
  name       = "ses-osd${count.index}"
  region     = "${var.region_name}"
  image_name = "${var.image_name}"

  connection {
    private_key = "${file("ssh/id_ses.pub")}"
  }

  flavor_name = "${var.worker_size}"
  key_pair    = "ses-ssh-${var.identifier}"

  network {
    name = "${var.internal_net}"
  }

  security_groups = [
    "${openstack_compute_secgroup_v2.secgroup_base.name}",
    "${openstack_compute_secgroup_v2.secgroup_osd.name}",
  ]

  user_data = "${data.template_file.osd.rendered}"
}

output "external_ip_admin" {
  value = "${openstack_networking_floatingip_v2.admin_ext.address}"
}

output "internal_ip_admin" {
  value = ["${openstack_compute_instance_v2.admin.access_ip_v4}"]
}

output "internal_ip_mons" {
  value = ["${openstack_compute_instance_v2.mon.*.access_ip_v4}"]
}

output "external_ip_mons" {
  value = ["${openstack_networking_floatingip_v2.mon_ext.*.address}"]
}

output "internal_ip_osds" {
  value = ["${openstack_compute_instance_v2.osd.*.access_ip_v4}"]
}

output "k8s_StorageClass_internal_ip" {
  value = ["\nkind: StorageClass\napiVersion: storage.k8s.io/v1\nmetadata:\n  name: persistent\nprovisioner: kubernetes.io/rbd\nparameters:\n  monitors: ${openstack_compute_instance_v2.mon.0.access_ip_v4}:6789,${openstack_compute_instance_v2.mon.1.access_ip_v4}:6789,${openstack_compute_instance_v2.mon.2.access_ip_v4}:6789\n  adminId: admin\n  adminSecretName: ceph-secret-admin\n  adminSecretNamespace: default\n  pool: k8s\n  userId: admin\n  userSecretName: ceph-secret-admin"]
}

output "ceph_secret" {
  value = ["\napiVersion: v1\nkind: Secret\nmetadata:\n  name: ceph-secret-admin\n  namespace: default\ndata:\n  key: ${lookup(data.external.cephsecret.result, "secret")}\ntype: kubernetes.io/rbd"]
}
