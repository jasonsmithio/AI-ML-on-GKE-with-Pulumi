import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_gcp as gcp

class ClusterArgs(TypedDict, total=False):
    clusterName: Input[str]
    env: Input[str]
    initialNodeCount: Input[float]
    machineType: Input[str]
    masterAuthNetworksIpcidr: Input[str]
    network: Input[str]
    projectId: Input[str]
    region: Input[str]
    removeDefaultNodePool: Input[bool]
    subnet: Input[str]
    zone: Input[str]

class Cluster(pulumi.ComponentResource):
    def __init__(self, name: str, args: ClusterArgs, opts:Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Cluster", name, args, opts)

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
        default = gcp.organizations.get_client_config_output()

        project = gcp.organizations.get_project_output(project_id=args["projectId"])

        mlp = gcp.container.Cluster(f"{name}-mlp",
            deletion_protection=False,
            enable_shielded_nodes=True,
            initial_node_count=args["initialNodeCount"],
            location=args["region"],
            name=args["clusterName"],
            network=args["network"],
            node_locations=[
                f"{args["region"]}-a",
                f"{args["region"]}-b",
                f"{args["region"]}-c",
            ],
            project=args["projectId"],
            remove_default_node_pool=args["removeDefaultNodePool"],
            subnetwork=args["subnet"],
            addons_config=gcp.container.ClusterAddonsConfigArgs(
                gcp_filestore_csi_driver_config=gcp.container.ClusterAddonsConfigGcpFilestoreCsiDriverConfigArgs(
                    enabled=True,
                ),
                gcs_fuse_csi_driver_config=gcp.container.ClusterAddonsConfigGcsFuseCsiDriverConfigArgs(
                    enabled=True,
                ),
                gce_persistent_disk_csi_driver_config=gcp.container.ClusterAddonsConfigGcePersistentDiskCsiDriverConfigArgs(
                    enabled=True,
                ),
            ),
            cluster_autoscaling=gcp.container.ClusterClusterAutoscalingArgs(
                autoscaling_profile="OPTIMIZE_UTILIZATION",
                enabled=True,
                auto_provisioning_defaults=gcp.container.ClusterClusterAutoscalingAutoProvisioningDefaultsArgs(
                    oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
                    management=gcp.container.ClusterClusterAutoscalingAutoProvisioningDefaultsManagementArgs(
                        auto_repair=True,
                        auto_upgrade=True,
                    ),
                    shielded_instance_config=gcp.container.ClusterClusterAutoscalingAutoProvisioningDefaultsShieldedInstanceConfigArgs(
                        enable_integrity_monitoring=True,
                        enable_secure_boot=True,
                    ),
                    upgrade_settings=gcp.container.ClusterClusterAutoscalingAutoProvisioningDefaultsUpgradeSettingsArgs(
                        max_surge=0,
                        max_unavailable=1,
                        strategy="SURGE",
                    ),
                ),
                resource_limits=[
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="cpu",
                        minimum=4,
                        maximum=600,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="memory",
                        minimum=16,
                        maximum=2400,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-a100-80gb",
                        maximum=30,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-l4",
                        maximum=30,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-tesla-t4",
                        maximum=300,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-tesla-a100",
                        maximum=50,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-tesla-k80",
                        maximum=30,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-tesla-p4",
                        maximum=30,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-tesla-p100",
                        maximum=30,
                    ),
                    gcp.container.ClusterClusterAutoscalingResourceLimitArgs(
                        resource_type="nvidia-tesla-v100",
                        maximum=30,
                    ),
                ],
            ),
            logging_config=gcp.container.ClusterLoggingConfigArgs(
                enable_components=[
                    "APISERVER",
                    "CONTROLLER_MANAGER",
                    "SCHEDULER",
                    "SYSTEM_COMPONENTS",
                    "WORKLOADS",
                ],
            ),
            ip_allocation_policy=gcp.container.ClusterIpAllocationPolicyArgs(),
            master_authorized_networks_config=gcp.container.ClusterMasterAuthorizedNetworksConfigArgs(
                cidr_blocks=[gcp.container.ClusterMasterAuthorizedNetworksConfigCidrBlockArgs(
                    cidr_block=args["masterAuthNetworksIpcidr"],
                    display_name="vpc-cidr",
                )],
            ),
            monitoring_config=gcp.container.ClusterMonitoringConfigArgs(
                enable_components=[
                    "APISERVER",
                    "CONTROLLER_MANAGER",
                    "DAEMONSET",
                    "DEPLOYMENT",
                    "HPA",
                    "POD",
                    "SCHEDULER",
                    "STATEFULSET",
                    "STORAGE",
                    "SYSTEM_COMPONENTS",
                ],
                managed_prometheus=gcp.container.ClusterMonitoringConfigManagedPrometheusArgs(
                    enabled=True,
                ),
            ),
            node_config=gcp.container.ClusterNodeConfigArgs(
                machine_type=args["machineType"],
                shielded_instance_config=gcp.container.ClusterNodeConfigShieldedInstanceConfigArgs(
                    enable_integrity_monitoring=True,
                    enable_secure_boot=True,
                ),
            ),
            node_pool_defaults=gcp.container.ClusterNodePoolDefaultsArgs(
                node_config_defaults=gcp.container.ClusterNodePoolDefaultsNodeConfigDefaultsArgs(
                    gcfs_config=gcp.container.ClusterNodePoolDefaultsNodeConfigDefaultsGcfsConfigArgs(
                        enabled=True,
                    ),
                ),
            ),
            private_cluster_config=gcp.container.ClusterPrivateClusterConfigArgs(
                enable_private_nodes=True,
                enable_private_endpoint=True,
                master_ipv4_cidr_block="172.16.0.32/28",
            ),
            release_channel=gcp.container.ClusterReleaseChannelArgs(
                channel="STABLE",
            ),
            workload_identity_config=gcp.container.ClusterWorkloadIdentityConfigArgs(
                workload_pool=f"{args["projectId"]}.svc.id.goog",
            ),
            opts=pulumi.ResourceOptions(parent=self))

        self.clusterId = mlp.id
        self.clusterLocation = mlp.location
        self.clusterName = mlp.name
        self.env = args["env"]
        self.gkeProjectId = args["projectId"]
        self.register_outputs({
            'clusterId': mlp.id, 
            'clusterLocation': mlp.location, 
            'clusterName': mlp.name, 
            'env': args["env"], 
            'gkeProjectId': args["projectId"]
        })