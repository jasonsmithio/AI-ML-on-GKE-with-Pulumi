import pulumi
from cloud_nat import CloudNat
from cluster import Cluster
from network import Network
from node_pools import NodePools
from vm_reservations import VmReservations
import pulumi_command as command
import pulumi_gcp as gcp
import pulumi_github as github
import pulumi_null as null
import pulumi_std as std


def not_implemented(msg):
    raise NotImplementedError(msg)

config = pulumi.Config()
# Name of the GKE cluster
cluster_name = config.get("clusterName")
if cluster_name is None:
    cluster_name = "gke-ml"
# Version of Config Management to enable
config_management_version = config.get("configManagementVersion")
if config_management_version is None:
    config_management_version = "1.17.1"
# Name of the GitHub repo that will be synced to the cluster with Config sync.
configsync_repo_name = config.get("configsyncRepoName")
if configsync_repo_name is None:
    configsync_repo_name = "config-sync-repo"
# Name of the environment
environment_name = config.get("environmentName")
if environment_name is None:
    environment_name = "dev"
# The GCP project where the resources will be created
environment_project_id = config.require("environmentProjectId")
# List of environments
env = config.get_object("env")
if env is None:
    env = ["dev"]
# GitHub user email.
github_email = config.require("githubEmail")
# GitHub org.
github_org = config.require("githubOrg")
# GitHub token. It is a token with write permissions as it will create a repo in the GitHub org.
github_token = config.require("githubToken")
# GitHub user name.
github_user = config.require("githubUser")
# Name of the namespace to demo.
namespace = config.get("namespace")
if namespace is None:
    namespace = "ml-team"
# VPC network where GKE cluster will be created
network_name = config.get("networkName")
if network_name is None:
    network_name = "ml-vpc"
# Taints to be applied to the on-demand node pool.
ondemand_taints = config.get_object("ondemandTaints")
if ondemand_taints is None:
    ondemand_taints = [{
        "effect": "NO_SCHEDULE",
        "key": "ondemand",
        "value": True,
    }]
# Taints to be applied to the reserved node pool.
reserved_taints = config.get_object("reservedTaints")
if reserved_taints is None:
    reserved_taints = [{
        "effect": "NO_SCHEDULE",
        "key": "reserved",
        "value": True,
    }]
# VPC routing mode.
routing_mode = config.get("routingMode")
if routing_mode is None:
    routing_mode = "GLOBAL"
# Create git-cred in config-management-system namespace.
secret_for_rootsync = config.get_float("secretForRootsync")
if secret_for_rootsync is None:
    secret_for_rootsync = 1
# Taints to be applied to the spot node pool.
spot_taints = config.get_object("spotTaints")
if spot_taints is None:
    spot_taints = [{
        "effect": "NO_SCHEDULE",
        "key": "spot",
        "value": True,
    }]
# Description of the first subnet.
subnet01_description = config.get("subnet01Description")
if subnet01_description is None:
    subnet01_description = "subnet 01"
# CIDR of the first subnet.
subnet01_ip = config.get("subnet01Ip")
if subnet01_ip is None:
    subnet01_ip = "10.40.0.0/22"
# Name of the first subnet in the VPC network.
subnet01_name = config.get("subnet01Name")
if subnet01_name is None:
    subnet01_name = "ml-vpc-subnet-01"
# Region of the first subnet.
subnet01_region = config.get("subnet01Region")
if subnet01_region is None:
    subnet01_region = "us-central1"
# Description of the second subnet.
subnet02_description = config.get("subnet02Description")
if subnet02_description is None:
    subnet02_description = "subnet 02"
# CIDR of the second subnet.
subnet02_ip = config.get("subnet02Ip")
if subnet02_ip is None:
    subnet02_ip = "10.12.0.0/22"
# Name of the second subnet in the VPC network.
subnet02_name = config.get("subnet02Name")
if subnet02_name is None:
    subnet02_name = "gke-vpc-subnet-02"
# Region of the second subnet.
subnet02_region = config.get("subnet02Region")
if subnet02_region is None:
    subnet02_region = "us-west2"
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Project
##########################################################################
environment = gcp.organizations.get_project_output(project_id=environment_project_id)
containerfilesystem_googleapis_com = gcp.projects.Service("containerfilesystem_googleapis_com",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="containerfilesystem.googleapis.com")
serviceusage_googleapis_com = gcp.projects.Service("serviceusage_googleapis_com",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="serviceusage.googleapis.com")
project_services_cr = gcp.projects.Service("project_services-cr",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="cloudresourcemanager.googleapis.com")
project_services_an = gcp.projects.Service("project_services-an",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="anthos.googleapis.com")
project_services_anc = gcp.projects.Service("project_services-anc",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="anthosconfigmanagement.googleapis.com")
project_services_con = gcp.projects.Service("project_services-con",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="container.googleapis.com")
project_services_com = gcp.projects.Service("project_services-com",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="compute.googleapis.com")
project_services_gkecon = gcp.projects.Service("project_services-gkecon",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="gkeconnect.googleapis.com")
project_services_gkeh = gcp.projects.Service("project_services-gkeh",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="gkehub.googleapis.com")
project_services_iam = gcp.projects.Service("project_services-iam",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="iam.googleapis.com")
project_services_gate = gcp.projects.Service("project_services-gate",
    disable_dependent_services=False,
    disable_on_destroy=False,
    project=environment.project_id,
    service="connectgateway.googleapis.com")
#
# Networking
##########################################################################
create_vpc = Network("create-vpc", {
    'networkName': not_implemented("format(\"%s-%s\",var.network_name,var.environment_name)"), 
    'projectId': environment.project_id, 
    'routingMode': routing_mode, 
    'subnet01Ip': subnet01_ip, 
    'subnet01Name': not_implemented("format(\"%s-%s\",var.subnet_01_name,var.environment_name)"), 
    'subnet01Region': subnet01_region, 
    'subnet02Ip': subnet02_ip, 
    'subnet02Name': not_implemented("format(\"%s-%s\",var.subnet_02_name,var.environment_name)"), 
    'subnet02Region': subnet02_region})
cloud_nat = CloudNat("cloud-nat", {
    'createRouter': True, 
    'name': not_implemented("format(\"%s-%s\",\"nat-for-acm\",var.environment_name)"), 
    'network': create_vpc.vpc, 
    'projectId': environment.project_id, 
    'region': std.split_output(separator="/",
        text=create_vpc["subnet-1"]).apply(lambda invoke: invoke.result[3]), 
    'router': not_implemented("format(\"%s-%s\",\"router-for-acm\",var.environment_name)")})
#
# GKE
##########################################################################
configmanagement_acm_feature = gcp.gkehub.Feature("configmanagement_acm_feature",
    location="global",
    name="configmanagement",
    project=environment.project_id,
    opts=pulumi.ResourceOptions(depends_on=[
            project_services_gkeh,
            project_services_anc,
            project_services_an,
            project_services_com,
            project_services_gkecon,
        ]))
gke = Cluster("gke", {
    'clusterName': not_implemented("format(\"%s-%s\",var.cluster_name,var.environment_name)"), 
    'env': environment_name, 
    'initialNodeCount': 1, 
    'machineType': "n2-standard-8", 
    'masterAuthNetworksIpcidr': subnet01_ip, 
    'network': create_vpc.vpc, 
    'projectId': environment.project_id, 
    'region': subnet01_region, 
    'removeDefaultNodePool': False, 
    'subnet': create_vpc["subnet-1"], 
    'zone': f"{subnet01_region}-a"})
reservation = VmReservations("reservation", {
    'clusterName': gke.cluster_name, 
    'projectId': environment.project_id, 
    'zone': f"{subnet01_region}-a"})
node_pool_reserved = NodePools("nodePool-reserved", {
    'clusterName': gke.cluster_name, 
    'nodePoolName': "reservation", 
    'projectId': environment.project_id, 
    'region': subnet01_region, 
    'reservationName': reservation.reservation_name, 
    'resourceType': "reservation", 
    'taints': reserved_taints})
node_pool_ondemand = NodePools("nodePool-ondemand", {
    'clusterName': gke.cluster_name, 
    'nodePoolName': "ondemand", 
    'projectId': environment.project_id, 
    'region': subnet01_region, 
    'resourceType': "ondemand", 
    'taints': ondemand_taints})
node_pool_spot = NodePools("nodePool-spot", {
    'clusterName': gke.cluster_name, 
    'nodePoolName': "spot", 
    'projectId': environment.project_id, 
    'region': subnet01_region, 
    'resourceType': "spot", 
    'taints': spot_taints})
membership = gcp.gkehub.Membership("membership",
    membership_id=gke.cluster_name,
    project=environment.project_id,
    endpoint=gcp.gkehub.MembershipEndpointArgs(
        gke_cluster=gcp.gkehub.MembershipEndpointGkeClusterArgs(
            resource_link=gke.cluster_id.apply(lambda cluster_id: f"//container.googleapis.com/{cluster_id}"),
        ),
    ),
    opts=pulumi.ResourceOptions(depends_on=[
            configmanagement_acm_feature,
            project_services_gkeh,
            project_services_gkecon,
        ]))
#
# Git Repository
##########################################################################
# data "github_organization" "default" {
#   name = var.github_org
# }
acm_repo = github.Repository("acm_repo",
    allow_merge_commit=True,
    allow_rebase_merge=True,
    allow_squash_merge=True,
    auto_init=True,
    delete_branch_on_merge=False,
    description="Repo for Config Sync",
    has_issues=False,
    has_projects=False,
    has_wiki=False,
    name=configsync_repo_name,
    visibility="private",
    vulnerability_alerts=True)
environment_branch = github.Branch("environment",
    branch=environment_name,
    repository=acm_repo.name)
feature_member = gcp.gkehub.FeatureMembership("feature_member",
    feature="configmanagement",
    location="global",
    membership=membership.membership_id,
    project=environment.project_id,
    configmanagement=gcp.gkehub.FeatureMembershipConfigmanagementArgs(
        version=config_management_version,
        config_sync=gcp.gkehub.FeatureMembershipConfigmanagementConfigSyncArgs(
            source_format="unstructured",
            git=gcp.gkehub.FeatureMembershipConfigmanagementConfigSyncGitArgs(
                policy_dir="manifests/clusters",
                secret_type="token",
                sync_branch=environment_branch.branch,
                sync_repo=acm_repo.http_clone_url,
            ),
        ),
        policy_controller=gcp.gkehub.FeatureMembershipConfigmanagementPolicyControllerArgs(
            enabled=True,
            referential_rules_enabled=True,
            template_library_installed=True,
        ),
    ),
    opts=pulumi.ResourceOptions(depends_on=[
            project_services_gkecon,
            project_services_gkeh,
            project_services_an,
            project_services_anc,
        ]))
environment_branch_default = github.BranchDefault("environment",
    branch=environment_branch.branch,
    repository=acm_repo.name)
environment_branch_protection_v3 = github.BranchProtectionV3("environment",
    repository=acm_repo.name,
    branch=environment_branch.branch,
    required_pull_request_reviews=github.BranchProtectionV3RequiredPullRequestReviewsArgs(
        require_code_owner_reviews=True,
        required_approving_review_count=1,
    ),
    restrictions=github.BranchProtectionV3RestrictionsArgs())
#
# Scripts
##########################################################################
create_cluster_yamls = null.Resource("create_cluster_yamls", triggers={
    "md5_files": _arg2_.result,
    "md5_script": _arg3_.result,
},
opts=pulumi.ResourceOptions(depends_on=[feature_member]))
create_cluster_yamls_provisioner0 = command.local.Command("createClusterYamlsProvisioner0",
    create=pulumi.Output.all(acm_repo.full_name, gke.cluster_name).apply(lambda full_name, cluster_name: f"{not_implemented('path.module')}/scripts/create_cluster_yamls.sh {github_org} {full_name} {github_user} {github_email} {environment_name} {cluster_name}"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[create_cluster_yamls]))
create_git_cred_cms = null.Resource("create_git_cred_cms", triggers={
    "md5_credentials": std.md5_output(input=std.join_output(separator="",
        input=[
            github_user,
            github_token,
        ]).apply(lambda invoke: invoke.result)).apply(lambda invoke: invoke.result),
    "md5_script": std.filemd5_output(input=f"{not_implemented('path.module')}/scripts/create_git_cred.sh").apply(lambda invoke: invoke.result),
},
opts=pulumi.ResourceOptions(depends_on=[
        feature_member,
        gke,
        node_pool_reserved,
        node_pool_ondemand,
        node_pool_spot,
        cloud_nat,
    ]))
create_git_cred_cms_provisioner0 = command.local.Command("createGitCredCmsProvisioner0",
    create=pulumi.Output.all(gke.cluster_name, environment).apply(lambda cluster_name, environment: f"{not_implemented('path.module')}/scripts/create_git_cred.sh {cluster_name} {environment.project_id} {github_user} config-management-system"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[create_git_cred_cms]))
install_kuberay_operator = null.Resource("install_kuberay_operator", triggers={
    "md5_files": _arg2_.result,
    "md5_script": _arg3_.result,
},
opts=pulumi.ResourceOptions(depends_on=[
        feature_member,
        create_git_cred_cms,
    ]))
install_kuberay_operator_provisioner0 = command.local.Command("installKuberayOperatorProvisioner0",
    create=acm_repo.full_name.apply(lambda full_name: f"{not_implemented('path.module')}/scripts/install_kuberay_operator.sh {full_name} {github_email} {github_org} {github_user}"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[install_kuberay_operator]))
namespace_default_kubernetes_service_account = "default"
namespace_default = gcp.serviceaccount.Account("namespace_default",
    account_id=f"wi-{namespace}-{namespace_default_kubernetes_service_account}",
    display_name=f"{namespace}/{namespace_default_kubernetes_service_account} workload identity service account",
    project=environment.project_id)
namespace_default_iam_workload_identity_user = gcp.serviceaccount.IAMMember("namespace_default_iam_workload_identity_user",
    member=environment.apply(lambda environment: f"serviceAccount:{environment.project_id}.svc.id.goog[{namespace}/{namespace_default_kubernetes_service_account}]"),
    role="roles/iam.workloadIdentityUser",
    service_account_id=namespace_default.id,
    opts=pulumi.ResourceOptions(depends_on=[gke]))
create_namespace = null.Resource("create_namespace", triggers={
    "md5_files": _arg2_.result,
    "md5_script": _arg3_.result,
},
opts=pulumi.ResourceOptions(depends_on=[
        feature_member,
        install_kuberay_operator,
    ]))
create_namespace_provisioner0 = command.local.Command("createNamespaceProvisioner0",
    create=acm_repo.full_name.apply(lambda full_name: f"{not_implemented('path.module')}/scripts/create_namespace.sh {full_name} {github_email} {github_org} {github_user} {namespace} {environment_name}"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[create_namespace]))
create_git_cred_ns = null.Resource("create_git_cred_ns", triggers={
    "md5_credentials": std.md5_output(input=std.join_output(separator="",
        input=[
            github_user,
            github_token,
        ]).apply(lambda invoke: invoke.result)).apply(lambda invoke: invoke.result),
    "md5_script": std.filemd5_output(input=f"{not_implemented('path.module')}/scripts/create_git_cred.sh").apply(lambda invoke: invoke.result),
},
opts=pulumi.ResourceOptions(depends_on=[
        feature_member,
        create_namespace,
    ]))
create_git_cred_ns_provisioner0 = command.local.Command("createGitCredNsProvisioner0",
    create=pulumi.Output.all(gke.cluster_name, gke.gke_project_id).apply(lambda cluster_name, gke_project_id: f"{not_implemented('path.module')}/scripts/create_git_cred.sh {cluster_name} {gke_project_id} {github_user} {namespace}"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[create_git_cred_ns]))
ray_head_kubernetes_service_account = "ray-head"
ray_worker_kubernetes_service_account = "ray-worker"
namespace_ray_head = gcp.serviceaccount.Account("namespace_ray_head",
    account_id=f"wi-{namespace}-{ray_head_kubernetes_service_account}",
    display_name=f"{namespace}/{ray_head_kubernetes_service_account} workload identity service account",
    project=environment.project_id)
namespace_ray_head_iam_workload_identity_user = gcp.serviceaccount.IAMMember("namespace_ray_head_iam_workload_identity_user",
    member=environment.apply(lambda environment: f"serviceAccount:{environment.project_id}.svc.id.goog[{namespace}/{ray_head_kubernetes_service_account}]"),
    role="roles/iam.workloadIdentityUser",
    service_account_id=namespace_ray_head.id,
    opts=pulumi.ResourceOptions(depends_on=[gke]))
namespace_ray_worker = gcp.serviceaccount.Account("namespace_ray_worker",
    account_id=f"wi-{namespace}-{ray_worker_kubernetes_service_account}",
    display_name=f"{namespace}/{ray_worker_kubernetes_service_account} workload identity service account",
    project=environment.project_id)
namespace_ray_worker_iam_workload_identity_user = gcp.serviceaccount.IAMMember("namespace_ray_worker_iam_workload_identity_user",
    member=environment.apply(lambda environment: f"serviceAccount:{environment.project_id}.svc.id.goog[{namespace}/{ray_worker_kubernetes_service_account}]"),
    role="roles/iam.workloadIdentityUser",
    service_account_id=namespace_ray_worker.id,
    opts=pulumi.ResourceOptions(depends_on=[gke]))
install_ray_cluster = null.Resource("install_ray_cluster", triggers={
    "md5_files": _arg2_.result,
    "md5_script": _arg3_.result,
},
opts=pulumi.ResourceOptions(depends_on=[
        feature_member,
        create_git_cred_ns,
    ]))
install_ray_cluster_provisioner0 = command.local.Command("installRayClusterProvisioner0",
    create=pulumi.Output.all(acm_repo.full_name, namespace_ray_head.email, namespace_ray_worker.email).apply(lambda full_name, namespaceRayHeadEmail, namespaceRayWorkerEmail: f"{not_implemented('path.module')}/scripts/install_ray_cluster.sh {full_name} {github_email} {github_org} {github_user} {namespace} {namespace_ray_head_email} {ray_head_kubernetes_service_account} {namespace_ray_worker_email} {ray_worker_kubernetes_service_account}"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[install_ray_cluster]))
manage_ray_ns = null.Resource("manage_ray_ns", triggers={
    "md5_script": std.filemd5_output(input=f"{not_implemented('path.module')}/scripts/manage_ray_ns.sh").apply(lambda invoke: invoke.result),
},
opts=pulumi.ResourceOptions(depends_on=[
        feature_member,
        create_git_cred_ns,
        install_ray_cluster,
    ]))
manage_ray_ns_provisioner0 = command.local.Command("manageRayNsProvisioner0",
    create=acm_repo.full_name.apply(lambda full_name: f"{not_implemented('path.module')}/scripts/manage_ray_ns.sh {full_name} {github_email} {github_org} {github_user} {namespace}"),
    environment={
        "GIT_TOKEN": github_token,
    },
    opts=pulumi.ResourceOptions(depends_on=[manage_ray_ns]))
