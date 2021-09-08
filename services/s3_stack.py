import json

from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    core
)

class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, id: str) -> None:
        super().__init__(scope)

        # https://stackoverflow.com/questions/61021252/aws-cdk-s3-bucket-creation-error-bucket-name-already-exisits

        bucket = s3.Bucket(self, "s3bucket", bucket_name = id)

        # policy_s3 = {"Version": "2012-10-17",
        #             "Statement": [
        #                 {
        #                     "Effect": "Allow",
        #                     "Action": [
        #                         "s3:PutObject",
        #                         "s3:DeleteObject",
        #                         "s3:PutObjectTagging"
        #                     ],
        #                     "Resource": [
        #                         "arn:aws:s3:::teste-dms/*"
        #                     ]
        #                 },
        #                 {
        #                     "Effect": "Allow",
        #                     "Action": [
        #                         "s3:ListBucket"
        #                     ],
        #                     "Resource": [
        #                         "arn:aws:s3:::teste-dms"]
        #                 }
        #             ]
        #         }

        # dms_role_s3 = iam.Role(
        #     self, 'dms-s3-role',
        #     role_name='dms-s3-role',
        #     assumed_by=iam.ServicePrincipal('dms.amazonaws.com'))

        # dms_role_s3.attach_inline_policy(iam.Policy(self, "policy_s3_dms", document=iam.PolicyDocument.from_json(policy_s3)))