# Security & Compliance

## Compliance Frameworks

- `PCI-DSS` - International
- `ISO`- International
- `HIPAA` - Healthcare Organizations in US

### ISO 27001:2005/10/13

- Documented Information Security Management System
- AWS is ISO 27001 compliant as an organization

### FedRAMP

- Federal Risk and Authorization Management Program
- (US) Government-wide program to security assessment, authorization & continuous monitoring for cloud products & services.

### HIPAA

- Federal (US) Health Insurance Portability & Accountability Act of 1996
- Protect confidentiality & security of healthcare information
- Some Services within AWS may not be HIPAA compliant yet

### NIST

- National Institute of Standards & Technology - US Department of Commerce
- Set of industry standards & best practices

### PCI - DSS v3.2

- Payments Card Industry - Data Security Standard
- AWS Infrastructure is PCI compliant - apps & configuration is your responsibility to be compliant

### PCI -DSS v3.2 Requirements

#### Build and maintain a secure network & systems

- __Requirement 1.__ Install & maintain a firewall configuration to protect cardholder data - AWS SG & ACL
- __Requirement 2.__ Do not use vendor-supplied defaults for system passwords & other security parameters

#### Protect Cardholder Data

- __Requirement 3.__ Protect stored cardholder data - e.g. RDS encrypted at Rest
- __Requirement 4.__ Encrypt transmission of cardholder data across open, public networks - e.g. use SSL and use encryption in-transit

#### Maintain a Vulnerability Management Program

- __Requirement 5.__ Protect all systems against malware & regularly update anti-virus software or programs
- __Requirement 6.__ Develop & maintain secure systems & applications

#### Implement Strong Access Control Measures

- __Requirement 7.__ Restrict access to cardholder data by business need to know - e.g. sysadmins do not need to have access to cardholder data
- __Requirement 8.__ Identify and authenticate access to system components - Use IAM and MFA
- __Requirement 9.__ Restrict physical access to cardholder data - No printouts or restricted access to on-premise database server etc.

#### Regularly monitor & test networks

- __Requirement 10.__ Track and monitor all access to network resources & cardholder data - Usage of Cloudwatch, AWS Config, CloudTrail etc.
- __Requirement 11.__ Regularly test security systems and processes. - e.g. penetration testing

#### Maintain an Information Security Policy

- __Requirement 12.__ Maintain a policy that addresses information security for all personnel.

### Other frameworks

- `SAS70`
- `SOC1`
- `FISMA`
- `FIPS 140-2` - a US government security standard for cryptographic modules. Level 4 - Highest security. `CloudHSM` is Level 3.

## DDOS

[AWS DDOS Whitepaper](./DDoS_White_Paper.pdf)

### Distributed Denial of Service Attacks

- Site or application unavailable to end users, usually by flooding traffic.
- Multiple mechanisms to achieve this:
- - Large packet floods
- - Reflection techniques
- - Amplification techniques
- - Large botnets

#### Amplification/Reflection Attacks

- Multiple things as NTP, SSDP, DNS, Chargen, SNMP attacks, where an attacker may send a __third party server__ (such as NTP - Network Time Protocol server) a request using a __spoofed IP__ address.
- The server will send a response to the request, with a greater payload (usually 24X58 times larger) to the initial request to the __spoofed IP address__ (usually the target)
- Example request: packet of 64 bytes - response: up to 3456 bytes from NTP server.
- Attackers can co-ordinate and use multiple NTP servers per second to send legitimate NTP traffic to target.

#### NTP Amplification Example

- Hacker's IP: `190.1.2.3`
- Victim's IP: `245.1.2.3`
- NTP Server IP: `200.1.2.3`
- Spoofed Source: `245.1.2.3` same as victim - Destination: `200.1.2.3`

#### Application Attacks (Layer 7 Attacks)

- Flood of `GET` requests to WebServer
- `Slowloris` attack - Hold connection requests open to web server as long as possible (and as many open as possible to drain the connection pool). Adding periodically http requests and headers, without completing the requests.

### How to mitigate DDOS

- Minimize the Attack Surface Area - Prefer `ALBs` with `WAFs`, rather than webservers with DNS round-robin.
- Be ready to Scale to absorb the attack - `Auto-Scaling` groups (use both for Webservers & `WAFs`)
- Safeguard Exposed Resources
- Learn Normal Behaviour - expected traffic - `Cloudwatch`
- Create a Plan for Attacks

### AWS Shield

- __Free__ service that protects all AWS customers on `ELB`, `CloudFront` & `Route53`
- Protects against `SYN`/`UDP` Floods, Reflection attacks and other Layer 3/Layer 4 attacks.
- __Advanced__ provides enhanced protections for apps running on `ELB`, `CloudFront` & `Route53` against larger - more sophisticated attacks. Costs $3000/month. Dedicated team & cost mitigation.

#### AWS Shield Advanced

- Always-on, flow-based monitoring of network traffic & active application monitoring - near real-time notifications of DDOS attacks.
- DDOS Response Team (DRT) 24X7
- Protects you AWS Bill against higher fees due to `ELB`, `CloudFront` & `Route53` usage spikes during a DDOS attack
- Costs $3000/month

## AWS Marketplace - Security Products

- `https://aws.amazon.com/marketplace`
- Marketplace is region specific
- To perform penetration testing on AWS you have to submit the __AWS Vulnerability / Penetration Testing Request Form__, to request authorization for pen testing to originate from any AWS Resources.
- Permission is __required__ for all penetration tests, even for AWS Marketplace products.

## IAM Custom Policies - Roles - Lab

### Create Custom Policy

- IAM -> Policies -> Create Policy
- AWS icon means __AWS Managed Policy__
- `Service` - e.g. `S3`, `EC2` etc.
- `Actions` - `Access Level`
- - `List`
- - `Read`
- - `Tagging`
- - `Write`
- - `Permissions Managment`
- `Resources` - e.g. for `S3` you can choose specific `Bucket` or even specific `Object` of `Bucket`, or `job`
- `Request conditions` - for filtering requests e.g. `MFA` required, `SourceIP` of request, `aws:PrincipalArn`, `aws:RequestedRegion` etc.
- `Name` of policy is mandatory, `Description` optional

Example AWS Custom Policy for `S3` - `List`, `Read` - All Resources - __Customer Managed__

```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucketByTags",
                "s3:GetLifecycleConfiguration",
                "s3:GetBucketTagging",
                "s3:GetInventoryConfiguration",
                "s3:GetObjectVersionTagging",
                "s3:ListBucketVersions",
                "s3:GetBucketLogging",
                "s3:ListBucket",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketPolicy",
                "s3:GetObjectVersionTorrent",
                "s3:GetObjectAcl",
                "s3:GetEncryptionConfiguration",
                "s3:GetBucketRequestPayment",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectTagging",
                "s3:GetMetricsConfiguration",
                "s3:HeadBucket",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketPolicyStatus",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketWebsite",
                "s3:ListJobs",
                "s3:GetBucketVersioning",
                "s3:GetBucketAcl",
                "s3:GetBucketNotification",
                "s3:GetReplicationConfiguration",
                "s3:ListMultipartUploadParts",
                "s3:GetObject",
                "s3:GetObjectTorrent",
                "s3:GetAccountPublicAccessBlock",
                "s3:ListAllMyBuckets",
                "s3:DescribeJob",
                "s3:GetBucketCORS",
                "s3:GetAnalyticsConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetBucketLocation",
                "s3:GetObjectVersion"
            ],
            "Resource": "*"
        }
    ]
}
```

### Create Role

- IAM -> Policies -> Create Role
- `Choose Service to use the Role` e.g. `EC2`
- `Permissions` -> Choose Policy e.g. Customer managed policy
- `Role Name` is mandatory
- Created Role can be assigned to an `EC2` instance

### Attach Role to instance after creation

- In the past you could not attach a role to existing running `EC2` instance
- Connect with ssh to EC2 instance
- Test s3 list

```Bash
aws s3 ls

An error occurred (AccessDenied) when calling the ListBuckets operation: Access Denied
```

- Solution 1: setup aws credentials (key & secret key id) of user with `AdministratorAccess` permissions, inside EC2 instance, with `aws configure` -> __Security Risk__ if instance is compromised & __Safety Risk__ since admin credentials can perform actions on any AWS resource, so actions can be performed by mistake.
- Solution 2: `EC2` -> Actions -> Instance Settings -> Attach/Replace IAM Role. Changes to attached role or policy edits to already attached roles, may take some minimal time to propagate.

- Test list s3 buckets with solution 2:

```Bash
aws s3 ls
2019-06-21 19:59:54 ama.intelligems.eu
2019-05-09 14:18:51 aws-madinad
2019-04-22 12:39:02 car-company
2018-12-20 11:10:00 cf-templates-11kpcd2kcuozf-eu-west-1
2019-05-10 12:44:58 codepipeline-eu-west-1-505596239165
2019-07-17 14:45:21 drone-ci-storage
2018-11-13 11:33:20 elasticbeanstalk-us-east-1-685721039798
2019-06-03 21:59:34 event-page-contact-dev-serverlessdeploymentbucket-1gknkphu2l3fg
2019-06-07 20:44:13 event-page-contact-prod-serverlessdeploymentbucke-k0iaupbhk31x
2018-02-09 07:28:01 intelligems-data
2018-07-22 21:01:22 intelligems-sentry-filestore
2019-01-10 11:54:42 intelligems-wagtail
2019-02-17 02:09:45 kops-state-training-gyhsx9v7n
2019-01-14 10:12:29 neorion-website
2018-07-21 13:31:16 scopeml.com
2019-05-13 14:16:17 terraform-state-internal
2018-11-10 00:23:09 training-snitch
2018-07-21 13:34:09 www.scopeml.com


# Test list objects
aws s3 ls s3://intelligems-data
2018-11-13 11:44:55      84548 aws-technology-partner-badge.png


# Test s3 upload (write)
echo "Test upload" > test.txt
aws s3 cp ~/test.txt s3://drone-ci-storage
upload failed: ./test.txt to s3://drone-ci-storage/test.txt An error occurred (AccessDenied) when calling the PutObject operation: Access Denied

# If write (all) permissions are added to policy, ec2 instance can upload on any bucket on any region.
# Sometimes for the above to work you may need to add the --region= flag to the aws s3 cp command.

# Test other aws cli programmatic actions
aws ec2 describe-instances --region=eu-west-1

An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to perform this operation.
```

### Pass Role vs Assume Role

#### Pass Role

- [https://docs.aws.amazon.com/IAM/latest/APIReference/API_AddRoleToInstanceProfile.html](https://docs.aws.amazon.com/IAM/latest/APIReference/API_AddRoleToInstanceProfile.html)
- [https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html)
- Adds the specified IAM role to the specified instance profile. An instance profile can contain only one role, and this limit cannot be increased. You can remove the existing role and then add a different role to an instance profile. You must then wait for the change to appear across all of AWS because of eventual consistency. To force the change, you must disassociate the instance profile and then associate the instance profile, or you can stop your instance and then restart it.

> Note: The caller of this API must be granted the PassRole permission on the IAM role by a permissions policy.

#### Assume Role

- [https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#stsapi_comparison](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_request.html#stsapi_comparison)
- Returns a set of temporary security credentials that you can use to access AWS resources that you might not normally have access to. These temporary credentials consist of an access key ID, a secret access key, and a security token. Typically, you use AssumeRole within your account or for cross-account access. For a comparison of AssumeRole with other API operations that produce temporary credentials, see Requesting Temporary Security Credentials and Comparing the AWS STS API operations in the IAM User Guide.

> Important: You cannot use AWS account root user credentials to call AssumeRole. You must use credentials for an IAM user or an IAM role to call AssumeRole.

#### Configure Assume Role with AWS CLI

[https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html)

## AWS Access Keys Best Practices

- [https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html](https://docs.aws.amazon.com/general/latest/gr/aws-access-keys-best-practices.html)

## MFA & Reporting with IAM - Lab

### MFA on root AWS account

- Important to save or print screen the QR code, to be able to connect with multiple devices (in case a phone is lost)
- You can use Google Authenticator on device, to scan and use a device for MFA

### MFA on individual users accounts

- AWS SMS MFA: We are no longer accepting new participants for the SMS MFA preview.
- Console: User -> Security Credentials -> Assigned MFA Device -> Virtual MFA Device -> Scan QR Code -> Type two consecutive MFA codes -> Activate MFA Device
- CLI: Requirements: aws cli with full IAM Access

### Enable MFA device for user with AWS CLI

```Bash
# Use bootstrap method QRCode to create MFA device
aws iam create-virtual-mfa-device --virtual-mfa-device-name EC2-User --outfile /home/ec2-user/QRCode.png --bootstrap-method QRCodePNG
# Returns a serial number (User ARN) that needs to be copied on next command
{
    "VirtualMFADevice": {
        "SerialNumber": "arn:aws:iam::673164704829:mfa/EC2-User"
    }
}
# Backup QR Code, e.g. by copying to secure s3 bucket
aws s3 cp /home/ec2-user/QRCode.png s3://secure-bucket-name

# Scan QR Code with Google Authenticator, using device camera

# Activate MFA device
aws iam enable-mfa-device --user-name EC2-User --serial-number arn:aws:iam::"USERNUMBERHERE":mfa/EC2-User --authentication-code-1 "CODE1HERE" --authentication-code-2 "CODE2HERE"

# Example
aws iam enable-mfa-device --user-name EC2-User --serial-number arn:aws:iam::673164704829:mfa/EC2-User --authentication-code-1 434121 --authentication-code-2 827407

# Command is time-sensitive (because of auth codes expiration) to create a token
```

- [Enforce the use of MFA with AWS CLI by using STS Token Service](https://aws.amazon.com/premiumsupport/knowledge-center/authenticate-mfa-cli/)
- __Exam Tip__: `Credential Report` (.csv file) shows user status and whether they have enabled MFA on their accounts.

## Security Token Service (STS)

> Tip: `AD` is built on top of `LDAP` (Lightweight Directory Access Protocol), `Active Directory` is a product and a directory service. `LDAP` is an application layer protocol and an IETF standard. `Active Directory` supports and implements `LDAP`, therefore allowing RFC-compliant `LDAP` clients to talk to it and perform `LDAP` operations such as bind, search, etc.

- Grants users limited & temporary access to AWS resources.
- Sources of users:
- __Federation (typically AD)__
- - Uses Security Assertion Markup Language (SAML)
- - Temporary access based on the user's AD credentials. __Does not need to be user in IAM__
- - Single Sign-On (SSO) allows users to log in to AWS console __without assigning IAM credentials__. They can login using even their workstation credentials.
- __Federation with Mobile Apps__
- - Use Facebook/Amazon/Google or other OpenID providers to log-in.
- __Cross Account Access__
- - Users from one AWS Account access resources of another.

### Key Terms

- __Federation__ - Combine or join a list of users from one domain (such as IAM - Identity Access Management) with a list of users of another domain (such as AD, Facebook etc.)
- __Identity Broker__ - A service that allows you to take an identity from point A and join it (federate it) to point B
- __Identity Store__ - Services like Active Directory, Facebook, Google etc.
- __Identities__ - A user of a service (identity store)

### STS Scenario

- Company website on `EC2` web servers in your `VPC`
- Users of the site, login to the site which authenticates against the companies Active Directory ==> __on-premise__
- `VPC` is connected to __on-prem__ using a secure `IPSEC VPN`
- Once logged-in the user can only have access to their __own__ `S3` bucket

![STS Scenario](./sts_scenario.PNG)

- __Identity Broker__ in the above design, must be developed on your own. The __Identity Broker__ calls the `GetFederationToken` function using `IAM` credentials. The call must include an __IAM Policy__ & a __duration (1 to 36 hrs__, along with a __policy__ that specifies permissions to be granted to temporary credentials.
- Authentication must happen first against the AD on step `3`
- Steps `4`,`5` exchange __temporary STS Token__ and also authenticate against `IAM` on steps `8`,`9`
- `STS` confirms that the policy of the `IAM` user making the call to `GetFederationToken` gives __permission to create new tokens__ and returns 4 values: `Access Key`, `Secret Access Key`, a __Token__ & a __Duration__ (token duration to expiration).

## Security Logging

### Related Services

- `CloudTrail` - Records user activity & actions (AWS API calls)
- `CloudWatch Logs`
- `AWS Config` - Records state of configuration
- `VPC Flow Logs` - Network traffic across `VPC`

[Security at Scale: Logging in AWS Whitepaper](./AWS_Security_at_Scale_Logging_in_AWS_Whitepaper.pdf) not mandatory for exam, but useful for logging checklist. Developed using:

- PCI DSS v2.0
- FedRAMP
- ISO 27001:2005

### Control Access to Log Files

- Ways to Prevent unauthorized access
- - IAM users, groups, roles, policies
- - S3 bucket policies
- - MFA
- Ways to Ensure role-based access (not IAM roles but design based on __organizational roles__)
- - IAM users, groups, roles, policies
- - S3 bucket policies

### Alerts on Log File Creation & Misconfiguration

- Alerts when log files __created__ or __fail__
- - `CloudTrail` notifications
- - `AWS Config` rules
- Alerts are specific, but don't divulge details
- - `CloudTrail` `SNS` notifications, only point to Log File Location

### Manage Changes to AWS Resources and Log Files

- Log changes to system components
- - `AWS Config` rules - log configuration changes
- - `CloudTrail` - log API calls
- Controls in-place to prevent modifications to logs
- - `IAM` & `S3` controls and policies
- - `CloudTrail` log file validation (feature)
- - `CloudTrail` log file encryption (feature)

## AWS Hypervisors, Isolation & AWS Firewalls - SGs

__Hypervisor__ or __Virtual Machine Monitor (VMM)__ is software, firmware or hardware that creates and runs Virtual Machines.

- Computer on which hypervisor runs: __host__ machine
- Each virtual machine: __guest__ machine

### AWS Hypervisor

- `EC2` runs on the `Xen` hypervisors. However `C5` class instances are running on `KVM`
- [https://www.theregister.co.uk/2017/11/07/aws_writes_new_kvm_based_hypervisor_to_make_its_cloud_go_faster/](https://www.theregister.co.uk/2017/11/07/aws_writes_new_kvm_based_hypervisor_to_make_its_cloud_go_faster/)
- Also for `KVM` you may need [Enhanced Networking ENA](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking-ena.html)
- `Xen` hypervisors can either run guest OS as Paravirtualization - `PV` or Hardware Virtual Machine - `HVM`
- `HVM` guests are fully virtualized. VMs on top pf hypervisor are not aware that they are sharing processing time with other VMs.
- `PV` is a lighter form of virtualization. Used to be quicker.
- However this performance gap has closed, and Amazon recommend using `HVM` wherever possible.
- Windows `EC2` - only `HVM`
- Linux `EC2` - both `PV` & `HVM`

### PV

- __Paravirtualized guests__ rely on the hypervisor, to provide support for operations that normally require privileged access, the guest OS has no elevated access to the CPU.
- CPU provides 4 separate access modes: 0-3 called __rings__. Ring 0 is the most privileged while Ring 3 the least.
- __Host OS__ (`Xen` Hypervisor) executes at __Ring 0__
- __Guest OS__ executes at __Ring 1__, while applications on __Ring 3__, unlike most operating systems (Ring 0)

### Isolation Layers

1. Physical Interface - e.g. network device
2. Firewall runs on Hypervisor - Host OS
3. Different Customers' security groups on top of firewall
4. Virtual Interface - e.g. virtual network devices
5. Hypervisor
6. Different Customers' virtual space (guest OS)

![Isolation](./isolation.PNG)

### Hypervisor Access

- Admins with business needs to access the __management plane__, are required to use MFA to gain access to purpose built __administrative hosts__
- __Administrative hosts__ are specifically designed, built, configured and hardened to protect the management plane of the cloud.
- All access to the management plane is logged & audited.
- When an employee no longer has a business need to access, privileges and access modes to relevant systems can be revoked.

### Guest (EC2) Access

- Instances are completely controlled by the customer.
- Full root access or admin control over accounts, services & applications.
- AWS has no access rights to instances or guest OS
- Linux instances - `SSH`
- Windows instances - `RDP`

### Memory Scrubbing

- `EBS` automatically __resets every block of storage__ used by a customer, so that one customer's data are not unintentionally exposed to another.
- __Memory allocated to guests__ is automatically scrubbed (set to zero), by the hypervisor when it is __unallocated__ to a guest. The memory is not returned to the __pool of free memory for allocation__ until scrubbing is complete.

## EC2 Dedicated Istances vs Dedicated Hosts

### EC2 Dedicated Instances

- Are `EC2` instances that run in a `VPC` on __hardware that's dedicated to a single customer__
- Dedicated instances are __physically isolated__ at the host hardware level from instances that belong to __other AWS accounts.__
- Dedicated instances may share hardware with __other instances from the same AWS Account__ that are __not__ Dedicated Instances.
- `Launch Instance` -> `Tenancy`: Use `Dedicated` instead of `Shared`
- You can purchase `On-Demand` or `Reserved` (save up to 70%) or `Spot` (save up to 90%)

### EC2 Dedicated Hosts

- Similar to Dedicated Instances - __Dedicated Hosts__ run in a `VPC` on __hardware that's dedicated to a single customer__
- Difference: Dedicated Host gives you additional visibility and control over how instances are placed on a physical server & things like sockets, cores, host ID etc.
- You can consistently deploy your instances on the __same server__ over time.
- Enable you to use existing server-bound software (__licenses__) & address corporate __compliance__ & __regulatory__ requirements. Example Oracle & VMWare licenses require dedicated hosts.
- `EC2` -> `Instances` Menu -> `Dedicated Hosts` or
- `Launch Instance` -> `Tenancy`: Use `Dedicated Host`

![Dedicated Instances vs Hosts](./dedicated.PNG)

## AWS Systems Manager

- Practical Advice (not exam): Use as much of SSM in day to day ops - [https://docs.aws.amazon.com/systems-manager/index.html](https://docs.aws.amazon.com/systems-manager/index.html)

### SSM EC2 Run Command

- Allows you to manage a large number of `EC2` instances and on-premises systems.
- Automate common admin tasks and ad-hoc configuration changes e.g. app installs, security patches, updates, join new instances to a Windows domain without login to each etc.
- `SSM` or use `EC2` -> `Systems Manager` Menu __Deprecated: No Longer Applies__
- `EC2` instances to work with `SSM` need an `IAM` role.

#### Create IAM EC2 Role for SSM

- `IAM` -> Create Role -> `EC2` Use Case -> `EC2 Role for Systems Manager` -> `AmazonEC2RoleforSSM` Policy
- Attach Role to Instances you need managed

```JSON
// AmazonEC2RoleforSSM
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ssm:DescribeAssociation",
                "ssm:GetDeployablePatchSnapshotForInstance",
                "ssm:GetDocument",
                "ssm:DescribeDocument",
                "ssm:GetManifest",
                "ssm:GetParameters",
                "ssm:ListAssociations",
                "ssm:ListInstanceAssociations",
                "ssm:PutInventory",
                "ssm:PutComplianceItems",
                "ssm:PutConfigurePackageResult",
                "ssm:UpdateAssociationStatus",
                "ssm:UpdateInstanceAssociationStatus",
                "ssm:UpdateInstanceInformation"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ssmmessages:CreateControlChannel",
                "ssmmessages:CreateDataChannel",
                "ssmmessages:OpenControlChannel",
                "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2messages:AcknowledgeMessage",
                "ec2messages:DeleteMessage",
                "ec2messages:FailMessage",
                "ec2messages:GetEndpoint",
                "ec2messages:GetMessages",
                "ec2messages:SendReply"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:PutMetricData"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstanceStatus"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ds:CreateComputer",
                "ds:DescribeDirectories"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation",
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetEncryptionConfiguration",
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts",
                "s3:ListBucket",
                "s3:ListBucketMultipartUploads"
            ],
            "Resource": "*"
        }
    ]
}
```

#### Run Command against EC2

- `SSM` -> `Run Command` -> Command: pick one e.g. `AWS-ConfigureCloudwatch`-> Target: `Specify Tags`, `Resource Group` or `Manually select`
- You can enable `SNS` on `Run Command` to send e-mail or notification when complete.
- Log Output: either `S3`, `CloudWatch Log Group` or no output record (view only in `SSM` output).
- `AWS CLI` section builds the appropriate command to run from cli.

```Bash
aws ssm send-command --document-name "AWS-ConfigureCloudWatch" --document-version "1" --targets '[{"Key":"tag:SSM","Values":["Yes"]}]' --parameters '{"status":["Enabled"],"properties":[""]}' --timeout-seconds 600 --max-concurrency "50" --max-errors "0" --region eu-west-1
```

#### Run Command Exam Tips

- Commands can be applied to a group of instances based on instance `Tags` or using `Resource Groups`.
- `SSM` agent needs to be installed on __your managed instances: on-premises, some EC2 AMI flavours, Other hybrid cloud instances__ to use Run Command.
- Linux AMIs:
- - `SSM Agent` is installed, by default, on __Amazon Linux base AMIs dated 2017.09 and later__. `SSM Agent` is also installed, by default, on `Amazon Linux 2`, `Ubuntu Server 16.04`, and `Ubuntu Server 18.04 LTS` AMIs.
- - You must manually install `SSM Agent` on other versions of Linux, including non-base images like `Amazon ECS-Optimized` AMIs. [Linux SSM Agent Installation](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-manual-agent-install.html)
- Windows AMIs:
- - `SSM Agent` is installed by default on instances created from `Windows Server 2016` and `Windows Server 2019` Amazon Machine Images (AMIs), and on instances created from `Windows Server 2003-2012 R2` AMIs published in November 2016 or later.
- - Windows AMIs published __before November 2016__ use the `EC2Config` service to process requests and configure instances. [Windows SSM Agent Installation](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-install-win.html)
- Run command can be run to on-premises systems as well.
- Commands & Parameters are defined in a `Systems Manager Document` (JSON)
- Commands issued:
- - AWS CLI
- - AWS Console
- - AWS Tools for Windows Powershell
- - SSM API
- - Amazon SDKs (e.g. `boto3`)

### SSM Parameter Store

[SSM Parameter Store Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

- Pass sensitive values (or plaintext config values) to `EC2` instances. Names of parameters need to be unique.
- Can be used by a bunch of other AWS Services such as: `EC2 Run Command`, `EC2 State Manager`, `CloudFormation`, `Lambda` etc.
- You can view unencrypted value, only with the correct `IAM` permissions (access to `KMS` key)
- Use `IAM` Roles for secrets consumption e.g. `ECS` - [https://aws.amazon.com/blogs/compute/managing-secrets-for-amazon-ecs-applications-using-parameter-store-and-iam-roles-for-tasks/](https://aws.amazon.com/blogs/compute/managing-secrets-for-amazon-ecs-applications-using-parameter-store-and-iam-roles-for-tasks/)

#### Parameter Types

- `String` - Any string value.
- `StringList` - Separate strings using commas.
- `SecureString` - Encrypt sensitive data using the `KMS` keys for your account.

#### Parameter Tiers

- `Standard` - Limit of 10,000 parameters. Parameter value size up to 4 KB. __Parameter policies__ are __not__ available. No additional charge.
- `Advanced` - Can create more than 10,000 parameters. Parameter value size up to 8 KB. __Parameter policies__ are available. Charges apply.

## Secure S3 using Pre-Signed URLs - AWS Config Lab

### S3 Pre-Signed URLs

- Allows read access without object `ACLs` or `Policies`, for a period of time, using a temporary `Access Key` & Signature
- Done via AWS SDKs (`boto3`) or using the CLI

```Bash
# Create a bucket
aws s3 mb s3://testpresignedurls --region=eu-west-1 --profile=training

# Create test file & upload
echo "Hello World, using Pre-Signed URLs" > pre-signed-test.txt
 aws s3 cp pre-signed-test.txt s3://testpresignedurls
upload: ./pre-signed-test.txt to s3://testpresignedurls/pre-signed-test.txt

# Access Denied on file link, by default S3 denied all access to object

# Pre-sign S3 object (default expiration: 60 mins)
aws s3 presign s3://testpresignedurls/pre-signed-test.txt --expires-in 300
https://testpresignedurls.s3.amazonaws.com/pre-signed-test.txt?Expires=1566725023&AWSAccessKeyId=AKIAICUIHVJDK5VJZTMA&Signature=GMh84Be08KpPrC6fOipKQDJgWE8%3D

# Visiting the above link gives read access to the object for 300 seconds.
```

### AWS Config with S3 Lab

- `Management & Governance` -> `Config` -> `Rules` -> `Add Rule` -> Filter for `s3` Rules
- `s3-bucket-public-read-prohibited` - Checks if s3 buckets allow __public read__ (bucket level compliance)
- `s3-bucket-public-write-prohibited` - Checks if s3 buckets allow __public write__ (bucket level compliance)

## Inspector vs Trusted Advisor

### Amazon Inspector

- Is an __automated security assessment service__, that helps improve the security and compliance of applications on AWS
- Automated Assessment for __vulnerabilities__ & deviations from __best practices__
- Detailed list of security findings, sorted by __level of severity__
- Reviewed directly, or part of detailed security reports via `Amazon Inspector Console` or API.
- Under `Security, Identity & Compliance` (important to remember vs `Trusted Advisor`: `Management & Governance`)
- Monitor network, filesystem, process activity of targets.

### Inspector Severity Levels

- `High`
- `Medium`
- `Low`
- `Informational`

### Setup Inspector

- `Assessment Setup` - `Advanced Setup`
- `Define an assessment target` - e.g. __All__ instances in a region, or grouped by __Tags__
- Install `Inspector Agents` on `EC2` instances -  Automated: Install the Amazon Inspector Agent on all EC2 instances in this assessment target. __To use this option, make sure that your EC2 instances have the SSM Agent installed and an IAM role that allows Run Command__
- `Define Assessment template` - Choose `Rules Packages` - Duration: 1hr recommended for better results - Setup `Assessment Schedule` to run periodically or one-off.
- `Perform Asessment Run`
- Review `Findings` against `Rules` or download `Full Report` that also lists all __tested vulnerabilities/rules__.
- `Amazon Inspector` - `Assessment Templates` - can be used to create a __Master Template__ that includes scheduled runs & `SNS` notifications.

### Amazon Trusted Advisor

- An online resource (Dashboard) to help you reduce cost, increase performance and improve security, by optimizing AWS environment.
- Core checks & recommendations (Security, Service Limits)
- Full Trusted Advisor - `Business` & `Enterprise` Support Plans only.
- Advisor Topics:
- - `Cost Optimization` - `Business` - `Enterprise`
- - `Security` - `Basic` - `Developer`
- - `Performance` - `Business` - `Enterprise`
- - `Fault Tolerance` - `Business` - `Enterprise`
- - `Service Limits` - `Basic` - `Developer`
- Under `Management & Governance`
- For `Security` topics only useful for basic checks such as `MFA` on Root Account, `SG` Unrestricted Ports etc.

#### Upgrade Support Plan

> Upgrade your Support plan to unlock all Trusted Advisor recommendations!
You will have access to technical support from a cloud support engineer, with phone and chat support, support API, Identity and Access Management, Architecture support - use case guidance, and more.

[AWS Support Plans Comparison](https://console.aws.amazon.com/support/plans/home?#/)

## Shared Responsibility Model

- AWS manages security __of__ the cloud. Security __in__ the cloud is the responsibility of the customer.
- Customers choose security to implement to protect their own content, platform, applications, systems and networks, no different to an on-site datacenter.

### AWS Security Responsibilities

- Global Infrastructure
- Hardware, Software, Networking and data-center facilities (physical AZs)
- "Managed Services" - `S3`, `DynamoDB`, `RDS` etc.

### Customer Security Responsibilities

- Infrastructure as a Service (IaaS)
- Updates & Security Patches to the Guest OSes
- Configuration of the AWS provided Firewall (`SGs`, `NACLs`)

![Shared Responsibility Model](./Shared_Responsibility_Model_V2.59.jpg)

### Service Aware Model

- The model changes for different AWS Services
- Service Types
- - __Infrastructure__
- - __Container__
- - __Abstracted__

#### Infrastructure Services

- Compute Services: `EC2`, `EBS`, `VPC`, `Auto Scaling`
- Similar and compatible to on-prem solutions
- You control the OS (Guest) & any Identity access management system, that provides access to the __user layer of the virtualization stack__
- Example `EC2`, you are responsible for:
- - `AMIs`
- - OS
- - Applications
- - Data in transit
- - Data at rest
- - Data stores
- - Credentials (Private/Public keys, AWS keys)
- - Policies, Roles & Configurations (`IAM`)

#### Container Services

- Typically run on a separate `EC2` but you don't manage the OS ot the platform layer.
- AWS provides a "managed service" for these application `containers`
- You are responsible for setting up & managing network access controls, such as firewall rules (`SGs`, `NACLs`) & platform level identity and access management, separately from `IAM` (e.g. RDS database users, groups)
- You are not responsible e.g. for `RDS` database updates, `RDS` OS updates, `PHP` updates with `Elastic Beanstalk` etc.
- Container Services: `RDS`, `EMR`- `Elastic MapReduce` (Managed Spark - Hadoop), `Elastic Beanstalk`

#### Abstracted Services

- High-level storage, database and messaging services such as `S3`, `Glacier`, `DynamoDB`, `SQS`, `SES` etc.
- These services abstract the platform & management layer
- You access endpoints of these abstracted services using `AWS APIs` & AWS manages the underlying service components on which they reside.

## VPC - Security Groups Security Aspects

- Security Groups are __Stateful__ - When opening ports on `ingress` traffic, automatically `egress` traffic is allowed.
- Lock Down `CIDRs` or single IP addr (`/32`) of Bastion Hosts to private instances, do not allow all ingress through the bastion's security group rule (sg to sg), as other instances may reside on that `SG` and be able to connect (see the below image).

![SG to SG](./sg_to_sg.PNG)

- How to know who is provisioning instances in private/public subnets. When you have 1000s of accounts (e.g. big firms) accessing, you need more than `CloudTrail` logging API calls to `S3`.
- You can use `Athena` to query access logs.

![Athena-cloudTrail](./athena_cloudtrail.PNG)

## AWS Artifact

- Provides on-demand downloads, from a single source, of AWS Compliance & Security Documents - __Audit Artifacts__ such as:
- - AWS ISO certs
- - PCI reports
- - SOC reports
- You can submit the documents to your auditor or regulator to __demonstrate the compliance of infrastructure and services you use__

## Encryption Differences

How to encrypt, previously unencrypted services, at rest

### Services that provide Instant Encryption

- `S3`

### Services that provide Encryption needing Migration

- `RDS`
- `DynamoDB` - may change in the future
- `EFS`
- `EBS`

## AWS WAF

- `AWS WAF` is a web application firewall service that helps protect the websites and web apps that you deliver with Amazon CloudFront and ELB Application Load Balancers. Create __web access control lists__ (`Web ACLS`) that define which HTTP and HTTPS requests to allow, block, or count.
- Configure `AWS WAF` to recognize and block common web application security risks like SQL injection (`SQLi`) and cross-site scripting (`XSS`)
- [`AWS WAF` vs `SGs`](https://www.anujvarma.com/firewalls-versus-security-groupsaws/)

![AWS WAF](./waf.PNG)

## Failed Questions

1. Your Security Architect would like to perform Penetration Testing on your entire AWS environment. They would like to schedule this as soon as possible, how should you approach this?

- Penetration Testing is not supported at any time as it can be disruptive in a multi-tenant environment
- There is no need to perform Penetration Testing because AWS automatically runs regular tests on your behalf and provides any security recommendations in the Trusted Advisor console
- You need to request approval before you can perform Penetration Testing in AWS `SELECTED`
- You are free to perform Penetration Testing on your own environment any time you like
- This will depend on the service and the type of test you want to perform - some will require permission `CORRECT`

> __EXPLANATION__: Penetration Testing is __allowed__ with prior approval from AWS
