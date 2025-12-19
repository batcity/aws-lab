# Amazon API gateway:

Amazon API Gateway lets users create API endpoints - either REST APIs or web socket based

The primary clientele is people/firms who want to quickly spin up public or private API endpoints
probably serverless ones - and worry less about setting things up - the disadvantage is that this is
pricy if the traffic is huge and the users would be tied to AWS

**Note: ** Don't use these instead of tradional API gateways like kong, nginx and so on because
this would be way more expensive since it charges based on how many times the gateway is hit
and it also adds additoinal latency

