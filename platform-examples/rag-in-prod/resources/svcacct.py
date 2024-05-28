import pulumi
import pulumi_gcp as gcp
import pulumi_random as random


class svcAcct:

    def __init__(self, display, project):
        self.display = display
        self.project = project
        self.acctid = random.RandomString("random",
            length=10,
            special=True,
            override_special="/@£$")


    def createSA(self):
        account_resource = gcp.serviceaccount.Account("accountResource",
            account_id=self.acctid,
            create_ignore_already_exists=False,
            description="string",
            disabled=False,
            display_name=self.display,
            project=self.project)
        
        return account_resource