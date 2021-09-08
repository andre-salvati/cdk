#!/usr/bin/env python3

from aws_cdk import core

from services.vpc_stack import VpcStack
from services.rds_stack import RdsStack
from services.dms_stack import DmsStack
from services.redshift_stack import RedshiftStack

app = core.App()

vpc_stack = VpcStack(app, "poc-sc-vpc")

rds_stack = RdsStack(app, "poc-sc-rds", vpc=vpc_stack)
#rds_stack = None

redshift_stack = RedshiftStack(app, "poc-sc-redshift", vpc=vpc_stack)
#redshift_stack = None

#dms_stack = DmsStackSC(app, "poc-sc-dms", vpc=vpc_stack, db=rds_stack, redshift=redshift_stack)

app.synth()