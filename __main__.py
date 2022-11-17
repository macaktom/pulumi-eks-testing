import json
import pulumi
from pulumi_aws import ec2, eks, iam

#Playing around with Pulumi - testing AWS EKS creation - only for testing purposes!!!
vpc = ec2.Vpc(
    'vpc-prod',
    cidr_block='10.0.0.0/16',
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        'Name': 'eks-prod-vpc',
    }
)

subnet = ec2.Subnet(
        "subnet1-prod",
        vpc_id = vpc.id,
        cidr_block = "10.0.1.0/24",
        tags={
        'Name': 'eks-prod-subnet',
    }
)


test_role = iam.Role("testRole",
    assume_role_policy=json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Sid": "",
            "Principal": {
                "Service": "ec2.amazonaws.com",
            },
        }],
    }),
    tags={
        "tag-key": "tag-value",
    })


eks_cluster = eks.Cluster(
    'eks-cluster-prod',
    vpc_config = eks.ClusterVpcConfigArgs(
        subnet_ids=[subnet.id],
        public_access_cidrs = ['0.0.0.0/0'],
    ),
    role_arn = test_role.arn,
    tags={
        'Name': 'eks-prod-cluster',
    }
)

pulumi.export('cluster-name', eks_cluster.name)
pulumi.export("endpoint", eks_cluster.endpoint)