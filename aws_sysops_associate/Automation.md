# Automation

## CloudFormation

- CloudFormation interprets the template and makes tha appropriate API Calls to create resources defined.
- YAML or JSON

### Benefits

- Infrastructure is provisioned consistently, allowing fewer mistakes / human error.
- Less time & effort than configuring manually.
- Version control & peer review templates.
- Free to use - only charge resources you create.
- Can be used to Manage updates & dependencies between different resources.
- Can be used to rollback & delete entire stack.

### Cloudformation Template

- YAML / JSON describes the endstate of infrastructure you are provisioning or changing.
- Upload to CloudFormation using S3.
- CloudFormation service reads the template and makes API calls on your behalf.
- Resulting resources: **Stack**

### Template Anatomy

- **Parameters:** input custom values
- **Conditions:** e.g. provision resources based on environment
- **Resources:** mandatory - AWS resources to be provisioned
- **Mappings:** create custom mappings e.g. Region:AMI
- **Transforms:** reference code stored in S3, e.g. template snippets, lambda code
- **Outputs:** output values

### Example template

```YAML
AWSTemplateFormatVersion: "2010-09-09"
# Optional start
Description: "Example template to create EC2 instance"
Metadata:
  Instances:
    Description: "Web Server Instance"

# input values from user when launching stack
Parameters:
  EnvType: # param name
    Description: "Environment Type"
    Type: String
    AllowedValues:
      - prod
      - test

Conditions:
  CreateProdResources: !Equals [ !Ref EnvType,prod] # if EnvType equals prod then CreateProdResources

# Optional end

Mappings: # e.g. set user defined values based on region
  RegionMap:
    eu-west-1:
      "ami": "ami-0bdb1d6c15a40392c"
    mapping02:
      key02:
        Name: value02

Trasform: # include snippets of code outside main template, e.g. lambda function, or template snippets
  Name: 'AWS::Include'
  Parameters:
    Location: 's3://S3BucketName/MyFileName.yaml'

Resources: # AWS Resources you are deploying
  EC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      KeyName:
      DisableApiTermination:
      ImageId: ami-0bdb1d6c15a40392c
      InstanceType: t2.micro
      Monitoring: true
      SecurityGroupIds:
        - sg-id
      Userdata: !Base64 |
        #!/bin/bash -ex
        # put your script here
      Tags:
        - Key: Environment
          Value: production
        - Key: Name
          Value: m1.prod

Outputs: # outputs the instance id of the instance "EC2Instance" created above.
  InstanceID:
    Description: Instance ID
    Value: !Ref EC2Instance
```

[Template Snippets to create reusable components to be included](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/CHAP_TemplateQuickRef.html)

- `Resources` is the only mandatory part of the template.
- __Warnings__ EC2 KeyPairs have to be created outside CF. There is no key pair resource in CF.
- Use `Rollback on failure` in `Advanced options` to let CloudFormation to delete any services if an error with the template occurs.
- Uploading a template automatically creates an S3 bucket. Deleting the stack does not delete the S3 bucket.

### CloudFormation Troubleshooting

[https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html)

## Elastic Beanstalk

- Upload code and AWS handles deployment, capacity provisioning, loadbalancing, auto-scaling & application health.
- Full control of underlying AWS Resources. You only pay for resources required to store & run your app (EC2, S3 etc.)
- Fastest & simplest way to deploy apps on AWS.
- Automatically scales up & down.
- You can select optimal EC2 instance type
- Choice: Either retain full admin control over AWS resources or Elastic Beanstalk does it on your behalf.
- Managed platform updates: automatically apply updates to OS, Java, PHP etc.
- Monitor & manage application health via dashboard.
- Integrated with CloudWatch for metrics & X-Ray for performance data.
- Deploys & scales web apps including web server (tomcat, nginx etc.)

## OpsWorks

- OpsWorks service allows to automate server configuration using Puppet / Chef.
- Using managed instances of either Puppet or Chef.
- Enables configuration management for your OS and applications.
- Automate server config using code. Works with existing Chef / Puppet code.
- Chef / Puppet support both Windows / Linux.
