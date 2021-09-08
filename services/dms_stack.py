from aws_cdk import core
import aws_cdk.aws_ec2 as ec2

import json
from aws_cdk import (
    aws_dms as dms,
    aws_iam as iam,
    #aws_secretsmanager as secretsmanager,
)

class DmsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, db, redshift, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # https://stackoverflow.com/questions/58542334/aws-dms-database-migration-service-system-error-messagethe-iam-role-arnawsi
        # https://stackoverflow.com/questions/63616384/creating-an-aws-dms-task-using-aws-cdk
        # https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.VPC.html

        dms_role = iam.Role(self, 'dms-vpc-role', 
            role_name='dms-vpc-role',
            assumed_by=iam.ServicePrincipal('dms.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSVPCManagementRole')]
        )        
            # managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSVPCManagementRole'),
            #                   iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSCloudWatchLogsRole'),
            #                   iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSRedshiftS3Role')]

        subnet_group = dms.CfnReplicationSubnetGroup(self, 'dms-sg',
            replication_subnet_group_description = "subnet group para DMS",
            replication_subnet_group_identifier= 'sc-dms-subnetgroup',
            subnet_ids=vpc.get_vpc_private_subnet_ids)

        subnet_group.node.add_dependency(dms_role)

        instance = dms.CfnReplicationInstance(self, "dms-instance",
            #publicly_accessible = False,
            replication_subnet_group_identifier="sc-dms-subnetgroup",
            replication_instance_class="dms.t2.small")

        instance.add_depends_on(subnet_group)

        if db != None:

            source = dms.CfnEndpoint(self, "source",
                endpoint_identifier= "sc-dms-source",
                endpoint_type= "source",
                engine_name= "sqlserver",
                server_name= db.get_endpoint_address,
                #port= 3306, # mysql
                port= 1433, # sqlserver
                database_name= "master",
                username= "adminuser",
                #password=secret.secret_value)
                password="Admin12345")

        if redshift != None:

            dms_access_role = iam.Role(self, 'dms-access-for-endpoint',
                role_name='dms-access-for-endpoint',
                assumed_by=iam.ServicePrincipal('dms.amazonaws.com'),
                managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonDMSRedshiftS3Role')]
            )
            
            target = dms.CfnEndpoint(self, "target",
                endpoint_identifier= "sc-dms-target",
                endpoint_type= "target",
                engine_name= "redshift",
                server_name= redshift.get_endpoint_address,
                port= 5439,
                database_name= "comments_cluster",
                username= "dwh_user",
                password="Teste12345")

        if db != None and redshift != None:

            # https://stackoverflow.com/questions/63616384/creating-an-aws-dms-task-using-aws-cdk

            dms.CfnReplicationTask(self, "task",
                replication_instance_arn= instance.ref,
                migration_type= "full-load",
                source_endpoint_arn= source.ref,
                target_endpoint_arn= target.ref,
                table_mappings=json.dumps({
                "rules": [{
                    "rule-type": "selection",
                    "rule-id": "1",
                        "rule-name": "1",
                    "object-locator": {
                        "schema-name": "%",
                        "table-name": "%"
                    },
                    "rule-action": "include"
                }]})
            )
