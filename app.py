#!/usr/bin/env python3

from aws_cdk import core

from services.vpc_stack import VpcStack
from services.rds_stack import RdsStack
from services.dms_stack import DmsStack
from services.redshift_stack import RedshiftStack
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

prefix = config['default']['stack_prefix']

app = core.App()

vpc_stack = VpcStack(app, f"{prefix}-vpc")

rds_stack = RdsStack(app, f"{prefix}-rds", vpc_stack, config)
#rds_stack = None

redshift_stack = RedshiftStack(app, f"{prefix}-redshift", vpc_stack, config)
#redshift_stack = None

dms_stack = DmsStack(app, f"{prefix}-dms", vpc_stack, rds_stack, redshift_stack, config)

app.synth()