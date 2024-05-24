import pulumi
import pulumi_gcp as gcp

class gcStorage:

    def __init__(self, bucketname, location):
        self.bucketname = bucketname
        self.location = location

    def makebucket(self):
        newbucket = gcp.storage.Bucket("auto-expire",
            name=self.bucketname,
            location=self.location,
            lifecycle_rules=[
                gcp.storage.BucketLifecycleRuleArgs(
                    condition=gcp.storage.BucketLifecycleRuleConditionArg(
                        age=3,
                    ),
                    action=gcp.storage.BucketLifecycleRuleActionArgs(
                        type="Delete",
                    ),
                ),
                gcp.storage.BucketLifecycleRuleArgs(
                    condition=gcp.storage.BucketLifecycleRuleConditionArg(
                        age=1,
                    ),
                    action=gcp.storage.BucketLifecycleRuleActionArgs(
                        type="AbortIncompleteMultipartUpload",
                    ),
                 ),
            ])            

        return newbucket