import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_gcp as gcp


def not_implemented(msg):
    raise NotImplementedError(msg)

def single_or_none(elements):
    if len(elements) != 1:
        raise Exception("single_or_none expected input list to have a single element")
    return elements[0]


class Taints(TypedDict, total=False):
    effect: Input[str]
    key: Input[str]
    value: Input[Any]

class NodePoolsArgs(TypedDict, total=False):
    accelerator: Input[str]
    acceleratorCount: Input[float]
    autoscaling: Input[Dict[str, Any]]
    clusterName: Input[str]
    machineReservationCount: Input[float]
    machineType: Input[str]
    nodePoolName: Input[str]
    projectId: Input[str]
    region: Input[str]
    reservationName: Input[str]
    resourceType: Input[str]
    taints: Input[list(Taints)]

class NodePools(pulumi.ComponentResource):
    def __init__(self, name: str, args: NodePoolsArgs, opts:Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:NodePools", name, args, opts)

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
        node_pool = gcp.container.NodePool(f"{name}-node-pool",
            cluster=args["clusterName"],
            location=args["region"],
            name=not_implemented("format(\"%s-%s\",var.cluster_name,var.node_pool_name)"),
            project=args["projectId"],
            autoscaling=gcp.container.NodePoolAutoscalingArgs(
                location_policy=args["autoscaling"]["location_policy"],
                total_max_node_count=args["autoscaling"]["total_max_node_count"],
                total_min_node_count=args["autoscaling"]["total_min_node_count"],
            ),
            network_config=gcp.container.NodePoolNetworkConfigArgs(
                enable_private_nodes=True,
            ),
            node_config=gcp.container.NodePoolNodeConfigArgs(
                reservation_affinity=single_or_none([{
                    "consumeReservationType": "SPECIFIC_RESERVATION",
                    "key": "compute.googleapis.com/reservation-name",
                    "values": [args["reservationName"]],
                } for entry in [{"key": k, "value": v} for k, v in [1] if args["reservationName"] != "" else []]]),
                taints=[gcp.container.NodePoolNodeConfigTaintArgs(
                    effect=entry["value"]["effect"],
                    key=entry["value"]["key"],
                    value=entry["value"]["value"],
                ) for entry in [{"key": k, "value": v} for k, v in args["taints"]]],
                machine_type=args["machineType"],
                oauth_scopes=["https://www.googleapis.com/auth/cloud-platform"],
                labels={
                    "resource-type": args["resourceType"],
                },
                gcfs_config=gcp.container.NodePoolNodeConfigGcfsConfigArgs(
                    enabled=True,
                ),
                guest_accelerators=[gcp.container.NodePoolNodeConfigGuestAcceleratorArgs(
                    count=args["acceleratorCount"],
                    type=args["accelerator"],
                )],
                shielded_instance_config=gcp.container.NodePoolNodeConfigShieldedInstanceConfigArgs(
                    enable_integrity_monitoring=True,
                    enable_secure_boot=True,
                ),
            ),
            opts=pulumi.ResourceOptions(parent=self))

        self.register_outputs()
