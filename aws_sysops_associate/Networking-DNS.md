# Networking - DNS

## DNS 101

- IPV4: 32 bit addresses: `byte.byte.byte.byte`
- IPV6: 128 bit addresses

- `.com`, `.eu`: __Top Level Domain Name__
- `.co.uk`: co is __Second Level Domain Name__
- `IANA` controls top level domain names in `root zone db`
- To ensure domain name uniqueness, there are `domain registrars`: GoDaddy, Cloudflare, Amazon etc.
- All registrars are registered with `InterNIC`

> __nslookup:__ When you run an nslookup, your are querying your local nameserver to look up a DNS record for a domain. If the nameserver you are using does not have the particular record stored locally or in its cache, it will reach out to its "forwarder" server. A forwarder server is another nameserver that your local nameserver has configured as an outbound resource for DNS resolution, such as Google's DNS server 8.8.8.8. That forwarder server should then respond to your local nameserver with the requested DNS record.
If the forwarder does not have that record in its cache, the query continues up the chain of servers in the Internet looking for the record, ultimately ending at the requested domain's nameserver, which can be seen when you run a whois check against the domain.

### SOA Start Of Authority Record

- Stores info about the name of the server that supplied the data for the zone
- Administrator of the zone
- Current version of the data file.
- Default number of seconds for ttl file on resource records.

> TTL is the amount of time it takes for a newly created record or changes to a record, to propagate to the whole Internet.

### NS Records

- Name Server Records are used by top level domain servers to direct traffic to the content DNS Server which contains the authoritative DNS records.

e.g.

```Shell
acloud.guru.com -> .com resolution = 'acloud.guru.com. 172800 IN NS ns.awsdns.com' -> Route53 -> SOA Record
DNS             ->                 = NS Record         TTL          NS server
```

### Types of Records

- `SOA` [Start Of Authority Record](#soa-start-of-authority-record)
- `A` Record is fundamental type of DNS Record. Stands for Address. Is used to translate Domain Name to IP address.
- `CNAME` Record is `Canonical Name`. Resolve one domain name to another.
- `Alias` Record is used to map resource record sets in your `hosted zone` to ELB, Cloudfront distros or S3 buckets. Unique to `Route53`. Similar to CNAME records.
- A CNAME record cannot be used for naked domain names (zone apex) (e.g. `intelligems.eu`), only subdomains (`www.intelligems.eu`, `ci.intelligems.eu`). Zone Apex must be either an A record or an Alias.
- `MX` mail-server record.
- `PTR` Reverse lookups to find out domain name owner.

### AWS Tips

- ELBs do not have pre-defined IPv4 addresses. You resolve to them using DNS.
- Understand difference between Alias and CNAME.
- Choice, always choose Alias over a CNAME.
- Alias records save time, any change to an IPv4 address of e.g. an ELB is reflected in Route53 Alias record automatically.

## Route53

- `Hosted Zones`: can be public or private, each hosted zone is a single domain name.
- Multiple `Record Sets` in a hosted zone.
- Default `RS` in each created `HZ`: `NS` Record & `SOA` record.
- On NS record -> Multiple top level domain dns records (.com, .co.uk etc.) for HA.
- `TTL` in **seconds**

## Routing Policies

- Simple
- Weighted
- Latency
- Failover
- Geolocation
- Multivalue Answer

### Route to targets on multiple Regions Lab

- Lab setting: 4 EC2 instances - 2 web servers on N.Virginia, 1 Sydney, 1 SaoPaolo
- Targets == Resources: ELB, EC2, S3, Cloufront etc.

### Simple Routing Policy

- You can have only **one** record with multiple values: ip addresses (A Record) or dns names (CNAME, Alias). If you specify multiple values in a record, Route53 returns all values to the user with **random order**
- If you try to create another record set on the **same** (e.g. the zone apex) domain name, with **simple routing**, you will be not allowed.

### Weighted Routing Policy

- Requests are routed on percentage (20% - 80%). Useful for `A/B` or `Blue/Green` deployment scenarios.
- `Weight`: 0 - 100
- You can create multiple record sets on the same name (e.g. apex) until their weights add up to 100.

### Latency Routing Policy

- Route traffic based on the lowest latency for your end-user. (i.e. which region will give them a faster response)
- You have to create a record set for **each region** that holds target-resources (e.g. EC2 or ELB) where you host your service. Route53 auto selects the lowest latency record set.

### Failover Routing Policy

- Active/Passive setup. Main hosted in one region and back-up hosted in another region in case of failure.
- Route53 will monitor the health of your primary using `healthchecks`
- Healthchecks can monitor:
- - Endpoint - IP or DomainName (useful for ELB)
- - Status of other healthchecks (**calculated** healthcheck)
- - Cloudwatch Alarm
- Healthcheck `Host Name` is the origin name the health check operates, passes the name in the `Host header`
- You can create `SNS Alarm` for Healthcheck
- `Failover Record Type`: `Primary` or `Secondary`
- Failover routing is **not instant**. Some downtime may happen, between healthcheck failure to new DNS routing propagation.
- **Warning:** EC2 instances without `Elastic Ip` or `ELB` in front, when restarted have **different public ip** addresses.

### Geolocation Routing Policy

- Lets you choose where your traffic will be sent, based on the geo location of the users, from which the DNS queries originate.
- Example: All european users routed to specific instances that run a version of your app tailored to european customers and/or translated, prices in Euros etc.
- **Recommended:** To create a **default** record set, for all other regions.

### Multivalue Answer Routing Policy

- When you want to approximately randomly route to **multiple resource**s, e.g. web servers, you can create a multivalue answer record **for each resource** and optionally associate a **Route53 healthcheck** with each record.
- Example use case: HTTP Web server with a **12** instances to handle high traffic. No server can handle all traffic on it's own.
- Route53 responds to DNS queries for up to **8 healthy** instances.
- Route53 gives **different answers** to different DNS resolvers.

[Multivalue vs simple policies](https://aws.amazon.com/premiumsupport/knowledge-center/multivalue-versus-simple-policies/)

### Geoproximity Routing Policy (NEW)

[Geoproximity Routing (Traffic Flow Only)](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-geoproximity)

### AWS Routing Tips

- You can nest record sets with `aliases`. Example: 2 weighted record sets with 3 nested latency record sets, each with it's own weight.
- Avoid nesting **too deep**, as resolution latency accumulates for each extra level.

