# DynamoDB

DynamoDB is a serverless, fully managed, NoSQL Database

## Types of supported Data models

- Key-value store (Note: Each value is essentially a document)
- Document based

## Storage model

Data is stored in disk so latency would be higher than an in-memory store like redis or memcache

however it looks like they do offer an in-memory enhancement for DynamoDB, more info on that here -> https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html

## Important metrics (TODO: validate this data)
(Note: Following metrics have been validated

RPO
Read latency
Availability sla
write latency)

| Metric              | DynamoDB (Standard)                           | DynamoDB Accelerator (DAX)                                      |
|---------------------|-----------------------------------------------|------------------------------------------------------------------|
| RPO (Recovery Point Objective) | 0 (Within a region)                          | Ephemeral (If DAX fails, no data is lost because it's in DDB)  |
| RTO (Recovery Time Objective) | Seconds (Managed failover)                   | Minutes (Time to provision/warm a new cluster)                 |
| Read Latency        | Single-digit Milliseconds (1–10ms)           | Microseconds (< 1ms)                                           |
| Write Latency       | Low (~5–10ms)                                | Slightly Higher (Write-through overhead)                      |
| Consistency         | Strong (Optional) or Eventual                | Eventual (Query/Item cache)                                   |
| Availability SLA    | 99.99% (99.999% for Global)                  | 99.9% (Standard for DAX clusters)                             |
| Throughput          | Virtually Infinite (Auto-scaling)            | Limited by Node Instance Size                                 |

## Additional reading

Dynamo research paper which was the foundation of DynamoDB: https://cdn.amazon.science/ac/1d/eb50c4064c538c8ac440ce6a1d91/dynamo-amazons-highly-available-key-value-store.pdf