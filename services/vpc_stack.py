from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class VpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        # self.vpc = ec2.Vpc(self, "VPC",
        #                    max_azs=2,
        #                    cidr="10.10.0.0/16",
        #                    # configuration will create 3 groups in 2 AZs = 6 subnets.
        #                    subnet_configuration=[ec2.SubnetConfiguration(
        #                        subnet_type=ec2.SubnetType.PUBLIC,
        #                        name="Public",
        #                        cidr_mask=24
        #                    ), ec2.SubnetConfiguration(
        #                        subnet_type=ec2.SubnetType.PRIVATE,
        #                        name="Private",
        #                        cidr_mask=24
        #                    ), ec2.SubnetConfiguration(
        #                        subnet_type=ec2.SubnetType.ISOLATED,
        #                        name="DB",
        #                        cidr_mask=24
        #                    )
        #                    ],
        #                    # nat_gateway_provider=ec2.NatProvider.gateway(),
        #                    nat_gateways=2,
        #                    )
        # # core.CfnOutput(self, "Output",
        # #                value=self.vpc.vpc_id)

        self.vpc = ec2.Vpc(self, "vpc")

    @property
    def get_vpc(self):
        return self.vpc

    @property
    def get_vpc_public_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PUBLIC
        ).subnet_ids

    @property
    def get_vpc_private_subnet_ids(self):
        return self.vpc.select_subnets(
            subnet_type=ec2.SubnetType.PRIVATE
        ).subnet_ids