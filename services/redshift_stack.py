from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_redshift as redshift

class RedshiftStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, config, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
                
        sg_redshift = ec2.SecurityGroup(self, id="sg_redshift",
                vpc=vpc.get_vpc,
                security_group_name="sg_redshift"
        )

        # TODO para acessar pelo DBeaver
        # colocar meu ip no sg inbound!!!!
        # colocar a URL na conexão do DBeaver
        
        sg_redshift.add_ingress_rule(
            peer=ec2.Peer.ipv4("10.0.0.0/16"),
            connection=ec2.Port.tcp(5439)
        )
            
        subnet_group = redshift.CfnClusterSubnetGroup(self, "redshift subnet group",
            subnet_ids=vpc.get_vpc_public_subnet_ids,
            description="Redshift Subnet Group"
        )
        
        self.instance = redshift.CfnCluster(self, "redshiftCluster",
            cluster_type="single-node",
            db_name="comments_cluster",
            master_username=config['default']['redshift_user'],
            master_user_password=config['default']['redshift_pass'],
            #master_user_password=comments_cluster_secret.secret_value.to_string(),
            #iam_roles=[_rs_cluster_role.role_arn],
            node_type="dc2.large",
            cluster_subnet_group_name= subnet_group.ref,
            vpc_security_group_ids=[sg_redshift.security_group_id])
        
    @property
    def get_endpoint_address(self):
        return self.instance.attr_endpoint_address
