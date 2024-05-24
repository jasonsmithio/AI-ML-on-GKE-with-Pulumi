import pulumi
import pulumi_gcp as gcp


class CloudSQL:

    def __init__(self, instance, dbname, region, tier, version='POSTGRES_15'):
        self.instance = instance
        self.dbname = dbname
        self.region = region
        self.tier = tier
        self.version = version


    def pginstance(self):

        newinstance = gcp.sql.DatabaseInstance("instance",
            name=self.name,
            region=self.region,
            database_version=self.version,
            settings=gcp.sql.DatabaseInstanceSettingsArgs(
                tier=self.tier,
            ),
            deletion_protection=True)
        
        return newinstance
        

    def pgname(self):    
        database_deletion_policy = gcp.sql.Database("database_deletion_policy",
            name=self.dbname,
            instance=self.dbinstance.name,
            deletion_policy="ABANDON")