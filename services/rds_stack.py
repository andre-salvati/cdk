from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_iam as iam

class RdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

    # https://blog.codecentric.de/en/2019/11/aws-cdk-part-3-how-to-create-an-rds-instance/
    
    # def __init__(self, scope: core.Construct, id: str, vpc, asg_security_groups, **kwargs) -> None:
    #     super().__init__(scope, id, **kwargs)

        # Ceate Aurora Cluster with 2 instances with CDK High Level API
        # Secrets Manager auto generate and keep the password, don't put password in cdk code directly
        # db_Aurora_cluster = rds.DatabaseCluster(self, "MyAurora",
        #                                         default_database_name="MyAurora",
        #                                         engine=rds.DatabaseClusterEngine.arora_mysql(
        #                                             version=rds.AuroraMysqlEngineVersion.VER_5_7_12
        #                                         )
        #                                         instance_props=rds.InstanceProps(
        #                                             vpc=vpc,
        #                                             vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.ISOLATED),
        #                                             instance_type=ec2.InstanceType(instance_type_identifier="t2.small")
        #                                         ),
        #                                         instances=2,
        #                                         parameter_group=rds.ClusterParameterGroup.from_parameter_group_name(
        #                                             self, "para-group-aurora",
        #                                             parameter_group_name="default.aurora-mysql5.7"
        #                                         ),
        #                                         )
        # for asg_sg in asg_security_groups:
        #     db_Aurora_cluster.connections.allow_default_port_from(asg_sg, "EC2 Autoscaling Group access Aurora")

        # Alternatively, create MySQL RDS with CDK High Level API
        # db_mysql_easy = rds.DatabaseInstance(self, "MySQL_DB_easy",
        #                                      engine=rds.DatabaseInstanceEngine.mysql(
        #                                          version=rds.MysqlEngineVersion.VER_5_7_30
        #                                      ),
        #                                      instance_type=ec2.InstanceType.of(
        #                                          ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.SMALL),
        #                                      vpc=vpc,
        #                                      multi_az=True,
        #                                      allocated_storage=100,
        #                                      storage_type=rds.StorageType.GP2,
        #                                      cloudwatch_logs_exports=["audit", "error", "general", "slowquery"],
        #                                      deletion_protection=False,
        #                                      delete_automated_backups=False,
        #                                      backup_retention=core.Duration.days(7),
        #                                      parameter_group=rds.ParameterGroup.from_parameter_group_name(
        #                                          self, "para-group-mysql",
        #                                          parameter_group_name="default.mysql5.7"
        #                                      )
        #                                      )
        # for asg_sg in asg_security_groups:
        #     db_mysql_easy.connections.allow_default_port_from(asg_sg, "EC2 Autoscaling Group access MySQL")

        sg_rds = ec2.SecurityGroup(self, id="sg_rds",
            vpc=vpc.get_vpc,
            security_group_name="sg_rds"
        )

        sg_rds.add_ingress_rule(
            peer=ec2.Peer.ipv4("10.0.0.0/16"),
            #connection=ec2.Port.tcp(3306)
            connection=ec2.Port.tcp(1433)
        )

        bucket = s3.Bucket(self, "s3bucket", bucket_name = "sc-sql-backup-restore")

        policy_s3 = {
                "Version": "2012-10-17",
                "Statement":
                [
                    {
                    "Effect": "Allow",
                    "Action":
                        [
                            "s3:ListBucket",
                            "s3:GetBucketLocation"
                        ],
                    "Resource": "arn:aws:s3:::sc-sql-backup-restore"
                    },
                    {
                    "Effect": "Allow",
                    "Action":
                        [
                            "s3:GetObject",
                            "s3:PutObject",
                            "s3:ListMultipartUploadParts",
                            "s3:AbortMultipartUpload"
                        ],
                    "Resource": "arn:aws:s3:::sc-sql-backup-restore/*"
                    }
                ]
                }
        
        rds_role_s3 = iam.Role(
            self, 'rds-s3-role',
            role_name='rds-s3-role',
            assumed_by=iam.ServicePrincipal('rds.amazonaws.com'))

        rds_role_s3.attach_inline_policy(iam.Policy(self, "policy_s3", document=iam.PolicyDocument.from_json(policy_s3)))
        
        opt_group = rds.OptionGroup(self, id = "teste",
            engine = rds.DatabaseInstanceEngine.sql_server_ex(version=rds.SqlServerEngineVersion.VER_14),
            configurations = [{
                "name": 'SQLSERVER_BACKUP_RESTORE',
                "settings": { 'IAM_ROLE_ARN': rds_role_s3.role_arn}
            }])


        self.db = rds.DatabaseInstance(self, "rds",
            #database_name="dbSource",
            #engine=rds.DatabaseInstanceEngine.mysql(version=rds.MysqlEngineVersion.VER_8_0_16),
            engine=rds.DatabaseInstanceEngine.sql_server_ex(version=rds.SqlServerEngineVersion.VER_14),
            credentials = rds.Credentials.from_password(username="adminuser", 
                                                        password=core.SecretValue("Admin12345")),
            vpc=vpc.get_vpc,
            #port=3306,
            #credentials=rds.Credentials.from_generated_secret("dms-rds-password"),
            instance_type= ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.SMALL),
            removal_policy=core.RemovalPolicy.DESTROY,
            deletion_protection=False,
            option_group=opt_group,
            vpc_subnets=ec2.SubnetSelection(subnet_type = ec2.SubnetType.PUBLIC),
            
            security_groups=[sg_rds])

    @property
    def get_endpoint_address(self):
        return self.db.db_instance_endpoint_address

