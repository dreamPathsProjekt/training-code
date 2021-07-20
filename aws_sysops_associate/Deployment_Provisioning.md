# Deployment & Provisioning

## Deploying an EC2 instance

### Spot instance details

- When price is between current and maximum price, instance is live. When price exceeds maximum price, instances are reclaimed.
- __Persistent request:__ Ensures that your request will be submitted every time your Spot Instance is terminated. Choose start & end date for request.
- Interruption behavior: __Terminate__, __stop__ or __hibernate__. Stop loses ram content, terminate loses everything, hibernate keeps a ram snapshot.
- __Launch group__: All instances start & stop at the same time.

### Placement Groups

- Benefit from greater redundancy (multiple azs) or higher networking throughput (lower latency on same az), by grouping `EC2` instances
- Name for `PG` must be __unique__ within a single __AWS Account__
- Only certain types of instances can be launched in `PGs` - Compute Optimized, GPU, Memory Optimized, Storage Optimized
- You can't merge `PGs`
- You can't move an __existing instance__ in a `PG` -> You can create an `AMI` from the existing instance & then launch a __new instance__ from the `AMI` into the `PG`

- Clustered
- Spread
- Partitioned

__New feature:__ [Capacity Reservation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-capacity-reservations.html)

#### Clustered

- Logically group a set of instances in the same single __Availability Zone__
- Recommended for applications that need __low network latency, high network throughput or both__
- If availability zone goes down, you lose all instances.
- Only certain instances can be launched in a Clustered PG
- AWS recommends __homegenous__ instances - __Same EC2 Instance types__ - within a Clustered PG

#### Spread

- You can have Spread PG inside different __Availability Zones__ within __one Region__
- Instances placed on __distinct underlying hardware__
- Recommended for applications that have a small number of __Critical__ instances that should be kept separate for __better isolation__
- __Failure__ is handled much better than normal `EC2` placement.

#### Partitioned

- Similar to Spread `PG` but on segment level - partitions.
- You can have Partitioned PG inside different __Availability Zones__ within __one Region__
- When using __Partitioned PG__ Amazon `EC2` divides each group into __logical segments - partitions__
- It is ensured that each partition has its own set of __racks__, with each rack having it's own __separate network__ and __power source__
- No two partitions within a `PG` share the __same racks__
- Useful for __multiple EC2__ instance __groups__ with isolation with each other __group__ - e.g. `Cassandra`, `HDFS`, `HBase` etc.

### Cloudwatch monitoring

- __Default__ (no charge): 5 minute intervals
- __Detailed monitoring:__ (additional charges): 1 minute intervals
- There is option to create custom metrics with more granularity ( < 1 min )

### Tenancy

- __Shared:__ other customers on same hardware
- __Dedicated:__ dedicated hardware
- __Dedicated host__

### T2/T3 unlimited

> Burst beyond capacity for spiky loads, for as long as needed.

## EC2 Launch Issues

Common reasons for EC2 __launch__ failure:

### InstanceLimitExceededError

- You have reached the limit on number of instances you can launch in a region.
- AWS sets default limit - 20 / region. You can request increase
- You can request limit increase on a per region basis.

### InsufficientInstanceCapacity

- AWS does not have enough available on-demand capacity to serve your request.
- Error local to the requested availability zone.

Options to resolve:

- Wait a few minutes & try again
- Request fewer instances
- Select different instance type
- Try purchasing reserved instances.
- Submit new request without specifying availability zone.

## EBS Volumes & IOPS

- Can be used to create a filesystem, run an OS, run a DB etc.
- SSD backed storage - operating systems, dbs & I/O intensive use cases.

### Variants of SSD

- __gp2 General Purpose__ - boot volumes
- __io1 Provisioned IOPS__ - I/O intensive, NoSQL/Relational dbs, latency sensitive workloads.

### IOPS

- IOPS capability is dependent on size of volume
- gp2 volumes: minimum 100 IOPS. 3 IOPS/GB up to a maximum of 10,000 IOPS
- io1 volumes: 50 IOPS/GB up to a max of 32,000 IOPS

__Hitting the IOPS limit of your volume:__

gp2 volume

- You will start to get your I/O requests queuing
- Depending on your app's sensitivity to IOPS & latency, your app becomes slow.

Approaches to IOPS gp2 limit:

- For gp2 you can increase size of volume, but if volume is 3,333 GB or more you will have reached the 10,000 IOPS limit.
- Need more than 10,000 IOPS change storage type to io1

## Bastion host

- A bastion host is a host located in your Public Subnet (A subnet that has a route out to the internet via an internet gateway - igw)
- Allows you to connect to EC2 instances using SSH or RDP (Windows).
- You can login to bastion host from local & then use bastion host (jumphost or jumpbox) to ssh / rdp to Private subnet of EC2 instances.
- Allows to safely access, administer EC2 instances without exposing them to the internet.

## ELB 101

- Application LB: Layer 7 - Content based routing
- Network LB: Layer 4 (Transport) - Fast performance, expensive
- Classic LB: Both Layer 4, 7 - Not recommended

### Application LB

- Best suited for HTTP|HTTPS traffic. Layer 7 are application aware.
- Advanced request routing, send specified requests to specific web servers.

### Network LB

- Best suited to lb tcp traffic where extreme performance is required.
- Capable of handling millions of requests / sec with ultra-low latency.

### Classic LB

- Legacy ELB
- You can traffic HTTP|HTTPS and use Layer-7 specific features like X-Forwarded & sticky sessions.
- Can also use Layer-4 LB for applications tha rely on TCP protocol.

### Pre-Warming ELBs

Sudden increases in traffic known beforehand. ELB may become overloaded and unable to handle all requests.

> In order to avoid overloading, you can contact AWS and request to __pre-warm__ your ELB. Pre-warming configures ELB to expected capacity, based on the traffic you expect.

AWS will need to know:

1. Start and end dates
2. Expected request rate per second
3. Total size of a typical request

### ELB & static IP addresses

- __ALB__ scale automatically to adapt to workload
- This has the effect of changing the IP address which clients connect to as new ALB are brought into service.
- __NLB__ solve this by creating __static IP__ in each subnet you enable. This keeps firewall rules simple - clients only access single ip per subnet.
- You don't have to choose, you can place an ALB behind an NLB.

## ELB Error Messages

### LB Errors 4XX 5XX

- Classic & ALB: default successful request response code is __200__
- __4XX__ indicate something has gone wrong on client side
- __5XX__ server side error

### Client Side Errors

- __400__ bad/malformed request - e.g. header is malformed
- __401__ unauthorized - user access denied
- __403__ forbidden - request is blocked by WAF access control list
- __460__ client closed connection before lb could respond. Client timeout period too short.
- __463__ LB received an __X-Forwarded-For__ request header with > 30 ip addresses, similar to malformed request. X-Forwarded-For: identify originating request.

### Server Side Errors

- __500__ Internal Server Error - e.g. error on the LB or backend application
- __502__ Bad Gateway - e.g. application server closed the connection or sent back malformed response
- __503__ Service Unavailable - no registered targets
- __504__ Gateway Timeout - e.g. application not responding - problem with app, database or web server.
- __561__ Unauthorized - received error code from ID provider (e.g. LDAP) when trying to authenticate user.

## ELB CloudWatch Metrics

- ELB publish metrics to CloudWatch for themselves & for backend instances. By default every 1 min.
- Helps to verify that system is performing as expected.
- You can create CloudWatch Alarm to perform action e.g. send an email when a metric reaches a pre-defined limit or range.

### Overall health

- __BackendConnectionErrors__ - number of unsuccessful connection to backend instances
- __HealthyHostCount__ - number of healthy instances as registered targets
- __UnHealthyHostCount__ - number of unhealthy instances
- __HTTPCode_Backend_2XX,3XX,4XX,5XX__

### Performance Metrics

- __Latency__ - number of seconds taken for registered instance to connect / respond
- __RequestCount__ - number of requests completed / connections made during specified interval (1 or 5 mins)
- __SurgeQueueLength__ - number of pending requests, max queue size is 1024, additional requests will be rejected. __Classic LB only__ to investigate slow performance of web servers.
- __SpilloverCount__ - number of requests rejected because the surge queue is full. __Classic LB only__

## AWS Systems Manager 101

- __AWS Systems Manager - SSM__ gives you visibility and control over your entire AWS Infrastructure.
- Integrates with CloudWatch
- Includes __Run Command__ which automates operational tasks across resources - e.g. security patching, package installs.
- Organize your inventory, group resources together by application or environment - including __on-premises__ systems.

### Run command

- Allows to run pre-defined commands on one or more EC2 instances.
- Stop, restart, resize, terminate instances.
- Attach/Detach EBS Volumes.
- Create snapshots, backup DynamoDB tables.
- Apply patches/updates
- Run an Ansible playbook
- Run a bash script

### Create IAM for SSM

[https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-configuring-access-role.html](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-configuring-access-role.html)

IAM -> Roles -> Create Role -> AWS Service::EC2 -> __EC2RoleForSSM__ -> Attach to EC2 instances

### Systems Manager Components

- Automation
- Run Command
- Patch Manager
- Maintenance Windows
- State Manager - config management
- Activations - manage on-premises systems
- Documents - automation / commands defined
- Parameter Store - config data / secrets / passwords
