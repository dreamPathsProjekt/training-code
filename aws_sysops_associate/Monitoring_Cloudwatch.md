# Monitoring & Reporting

## Host Level Metrics

- CPU
- Network
- Disk
- Status Check

> **Important!:** RAM utilization & disk usage is a **custom_metric**

- EC2 monitoring **default**: 5 min intervals, **enable detailed monitoring:** 1 minute intervals (minimum granularity)
- By default __cloudwatch log data__ is stored indefinitely
- You can retrieve data from terminated EC2 or ELB instances after termination.
- Cloudwatch can be used on premise also. Download & install SSM agent & Cloudwatch agent.

## Monitoring Custom Metrics

> us-east-1 (N.Virginia) is the region where new services begin, but has the most downtime.

- Role creation for EC2 to talk to CloudWatch, Roles->EC2->CloudwatchFullAccess
- Attach role at instance creation

If you associated an IAM role (instance profile) with your instance, verify that it grants permissions to perform the following operations:

- cloudwatch:PutMetricData
- cloudwatch:GetMetricStatistics
- cloudwatch:ListMetrics
- ec2:DescribeTags

[Install scripts for various distros](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html)

[Cloudwatch Agent instead of scripts](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)

## Monitoring EBS

### EBS Types

- General purpose SSD `gp2` max 10000 IOPS
- Provisioned IOPS SSD `io1` > 10000 IOPS / 160 Mib/s (databases etc) max 20000 IOPS
- Throughput optimized HDD `st1`
- Cold HDD `sc1`

### Burst gp2 with I/O credits

- 100Gb volume: 3 IOPS/Gb = 300 IOPS
- Burst to 3000 IOPS = 3000 - 300 = 2700 IOPS burst
- Burst is maxed to 3000 IOPS -> only way is to increase volume size up to 10000 IOPS
- When you are not going above provisioned IO level you earn I/O credits

### Pre-warming EBS Volumes

- New EBS volumes receive maximum performance
- EBS restored from snapshot must be initialized - takes time, increase in I/O latency in first time access.
- __Initialization:__ Reading the entire volume once, before use in production to avoid latency hit. [EBS Initialize](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-initialize.html)

### EBS Cloudwatch Metrics

#### Important Metrics

- __VolumeReadOps, VolumeWriteOps:__ Total number of IOPS in a specified period in time.
- __VolumeQueueLength:__ Number of read & write ops **waiting** to be completed in specified period in time. Desired ~= 0

[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-volume-status.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-volume-status.html)

#### Status Checks

- `ok`: enabled - normal as expected
- `warning`: enabled - degraded performance, severely degraded
- `impaired`: enabled/disabled - stalled, not available
- `insufficient-data`: enabled/insufficient data - insufficient data

### Modifying EBS Volumes

- Increase size
- Change type
- io1 volume adjust IOPS perf.

All the above without detaching

## Monitoring ELB

### LB Types

- ALB
- NLB (Network) Layer-4 High network throughput
- CLB (Classic)

### Ways to monitor ELB

- CloudWatch Metrics
- Access Logs
- Request Tracing (ALB only)
- CloudTrail Logs

Cloudwatch vs CloudTrail

- CloudWatch monitors performance
- CloudTrail monitors API calls in AWS (e.g. ELB, user, EC2 creations/deletion events) => auditing

### ELB Access Logs

> Access Logs can store data where the EC2 instance has been deleted. Useful to trace 5XX requests to instances that are not there, terminated or unable to log requests.

### Request Tracing

> Track HTTP requests from clients to targets to other AWS services. __Only available for ALB.__ ALB adds or updates `X-Amzn-Trace-Id` header before sending request to the target.

### CloudTrail

> Use CloudTrail to capture calls made to the ELB AWS API and store them in S3.

## Monitoring ElastiCache

### Important metrics

- CPU Utilization
- Swap Usage
- Evictions
- Concurrent connections

### CPU Utilization

__Memcached:__

- Multithreaded
- Can handle cpu loads up to `90%`. If `>90%` __add more nodes__ to the cluster.

__Redis:__

- Not multithreaded. To determine the point in which to scale , `90 / number of cores`
- Example `cache.m1.xlarge` has 4 cores so `90 / 4 = 22.5%` => 22.5% threshold for scaling.

### Swap Usage

Typically swap file (or paging file) size = RAM size

__Memcached:__

- Should be ~= 0 most of the time. Never exceed 50mb. If > 50mb => increase `memcached_connections_overhead`
- `memcached_connections_overhead` defines amount of memory to be reserved for memcached connections & other misc. overhead

__Redis:__

- No `SwapUsage` metric instead use `reserved-memory`

### Evictions

> An eviction occurs when a new cache key (item) is added and an old one must be removed due to lack of free space.

__Memcached:__

- No recommended setting. Choose threshold based on application.
- Either __scale up:__ increase memory of existing nodes
- Or __scale out:__ add more __nodes__ to the cluster.

__Redis:__

- No recommended setting. Choose threshold based on application.
- Only __scale out:__ add more __read replicas__

### Concurrent connections

__Memcached & Redis:__

- No recommended setting. Choose threshold based on application.
- If sustained & high spike of Concurrent connections:
    1. Large traffic spike or
    2. Application is not releasing connections as it should.
- __Exam tip:__ Remeber to create/set __alarm__ on concurrent connections threshold.

## Metrics from multiple regions & custom dashboards

> Dashboards are international, but data sources depend on region you are at the moment.

## Billing Alarms

My Billing Dashboard -> Enable Billing Alerts -> Manage Billing Alerts -> Takes you to Cloudwatch -> Billing

## AWS Organizations

> Allows to manage multiple AWS Accounts.

- Centrally manage policies across multiple aws accounts.
- Control access to AWS resources
- Automate AWS Account creation and Management
- Consolidate billing across multiple AWS Accounts

### Central Management

- Create groups of accounts & attach policies across accounts.

### Control Access

- Create Service Control Policies (SCP) that centrally allow/deny Service usage. E.g. deny usage of DynamoDB for HR group across all AWS accounts.
- Even if IAM allows it, SCP will override it.

### Automate Account Creation

- Use AWS Organizations API to automate and create accounts programatically & add new account to a group.
- Policies attached to the group are automatically applied to new accounts.

### Consolidated Billing

- Setup a single payment method for all AWS Accounts in organization
- See combined view of charges from all accounts
- Take advantage of pricing benefits from aggregate usage such as volume discounts for EC2 & S3.

### Organize accounts

- Account groups are called organizational units.
- Policies are attached to organizational units.
- You need to enable SCP on Organize Accounts to attach policies.

## Tagging & Resource Groups

### Tags

- Key-value pairs attached to AWS Resources.
- Metadata
- Tags can be inherited (Autoscaling, EBeanstalk & CloudFormation can create other resources)
- Tags are case sensitive

### Resource Groups

Make it easy to group resources filtered by tags.

Contain information:

- Region
- Name
- HealthCheck

Specific Information:

- For EC2 - Public & Private IP addresses
- For ELB - Port configurations (listeners)

### Resource group types

- Classic Resource Group (Global). Resource Groups menu -> Create a classic group
- AWS Systems Managers (Per Region, execute commands for Resource Group). Resource Groups Menu -> Create a group. You can also attach tags to an ASM resource group (they will be applied to the group itself not resources).

### AWS Systems Manager

- Insights (Compliance etc.)
- Execute Automation (Actions)

## EC2 Pricing Models

### On Demand Instances

- Fixed rate by the hour (or by the second)
- Low cost & flexibility, no up-front payment / long-term commitment.
- Applications with short term, spiky or unpredictable workloads that cannot be interrupted.
- Applications being developed or tested on AWS for the first time.

### Reserved Instances

- Applications with steady state / predictable usage.
- Application that require reserved capacity.
- Up-front payments to reduce total costs.
- Contract 1yr or 3yrs.
- Standard RIs (Reserved Instances) Up to 75% off on-demand.
- **Maximum discount** - 75% 3yr term - all up-front.
- **Convertible RIs** - Up to 54% discount off on-demand - capability to change attributes of RI as long as the exchange results in creation of RI with equal or greater value.
- **Scheduled RIs** available to launch within the time window you reserve. Allows to match capacity requirements for a schedule that occurs only a fraction of the day/week/month e.g. seasonal or daily traffic spikes.

### Spot Instances

- Applications that have flexible start & end times.
- Applications that are only feasible at very low compute prices.
- Users with urgent computing needs for large amounts of additional capacity.
- Bidding model with spot price vs bidding price.
- Workloads suitable to shut down suddenly.

### Dedicated Hosts

- Useful for regulatory requirements that may not support multi-tenant virtualization (e.g. banking applications)
- Underlying physical hardware dedicated to you.
- Great for licensing which does not support multi-tenancy or cloud deployments. (e.g. Oracle deployments)
- Can be purchased On-Demand (hourly)
- Can be purchased as a Reservation for 70% off the On-Demand price.

## AWS Config

[https://aws.amazon.com/config/faq/](https://aws.amazon.com/config/faq/)

> AWS Config provides an inventory of your AWS resources and a history of configuration changes to these resources & configuration change notifications. You can use AWS Config to define rules that evaluate these configurations for compliance.
> Recording all the time what goes on in an AWS Environment.

Enables

- Compliance auditing
- Security analysis
- Resource tracking

Provides

- Configuration snapshots & logs config changes of AWS Resources
- Automated compliance checking

Components

- Config Dashboard
- Config Rules: Managed or Custom
- Resources
- Settings

> Has to be deployed on each individual region (unlike cloudtrail)

### Config Event Routing

- Events are stored in AWS Config S3 Bucket
- Event target: sent to a Lambda Function with Standard (40+) or Custom Rules.
- If Rule is broken Config triggers an SNS Notification

### Terminology

- Configuration **Items** - Point in time attributes of resource (e.g. sg has ports 22, 443 open)
- Configuration **Snapshots** - Collection of config items (every 3hrs, 6hrs etc.)
- Configuration **Stream** - Stream of changed config items (events)
- Configuration **History** - Collection of config items for a resource over time (e.g what the sg looked like 2 weeks ago)
- Configuration **Recorder** - The configuration of AWS Config that stores and records config items.

### Recorder Setup

- Logs config for account per region
- Stores in S3
- Notifies SNS

### What we can see

- Resource Type
- Resource ID
- Compliance
- Timeline
- - Configuration details
- - Relationships
- - Changes
- - Cloudtrail Events

### Compliance Checks

- Trigger
- - Periodic or
- - Configuration Snapshot Delivery (filterable)
- Managed Rules
- - About 40
- - Basic but fundamental

## Health Dashboards

### Service Health Dasboard

Shows health of AWS Service as a whole per region. [status.aws.amazon.com](https://status.aws.amazon.com/)

### Personal Health Dasboard

Alerts and guidance when AWS experience events that may impact you. Shown in console.
