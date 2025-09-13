# AWS S3

AWS S3 is an **object storage service** that allows you to store a virtually unlimited amount of data in the cloud.  
You can store objects of any type in S3, e.g., binaries, files, images, videos, etc.

---

## Key Characteristics

- **Durable & Resilient**  
  Data is automatically replicated across multiple Availability Zones, ensuring high durability even if one node or zone goes down.

- **Highly Available & Globally Accessible**  
  S3 provides endpoints in multiple regions, allowing low-latency access to your data from anywhere.

- **Cost-Effective**  
  You pay only for the storage you use, making S3 cheaper than maintaining your own hardware, especially for ephemeral or large-scale data.

---

## Important Concepts (Interview Prep 🚀)

- **Is S3 global or region-based?**  
  - S3 is a **global service**, but **buckets are created in a single region** where the data physically resides.  
  - When you upload data, it is stored in the chosen region unless you enable replication.  

- **Bucket Naming and Global Uniqueness**  
  - **Bucket names are globally unique across *all* AWS accounts.**  
  - Example: if you create a bucket called `my-company-data`, no one else (not even another AWS account) can create a bucket with that name anywhere.  
  - This is because each bucket has a **globally unique DNS name**, like:  
    ```
    https://my-company-data.s3.amazonaws.com
    ```
  - 🔑 **Analogy:** Think of S3 bucket names like **Gmail usernames** — once `alice@gmail.com` exists, no one else can register it, even if they’re in a different country.  

- **Buckets in AWS Organizations / Sub-Accounts**  
  - Even if your company has many accounts under one AWS Organization, the **bucket namespace is still global**.  
  - If the “root” account or one sub-account creates `my-shared-bucket`, that name is taken globally.  
  - Other sub-accounts in your org cannot create a new bucket with the same name in another region.  
  - What they *can* do is **access or be granted permissions** to that same bucket (so it may appear in multiple accounts’ consoles).  

- **Why does it look like a bucket exists in multiple regions?**  
  - An S3 bucket **exists in exactly one AWS region** (chosen at creation).  
  - You may see the same bucket when switching regions in the console because:  
    - AWS consoles sometimes list **all accessible buckets**, regardless of their region.  
    - If you have cross-region replication set up, you’ll see **different buckets with different names** (one per region), but they’re logically linked.  
  - ⚠️ **Important:** If you open the bucket from a region other than its home region, you might see the bucket name but **not the objects inside it**, since the data physically resides only in the home region.  

- **Can you create the same bucket in different regions?**  
  - **No.** Bucket names are global, so once a name is taken, it’s unavailable in all regions.  
  - To keep data in multiple regions, you either:  
    - Use **S3 Cross-Region Replication (CRR)**, or  
    - Manually create separate buckets with **unique names** (e.g., `my-company-data-us-east-1`, `my-company-data-eu-west-1`) **and upload/sync the data yourself**.  

---

## Cross-Region Replication (CRR)

- **What it is:**  
  Cross-Region Replication automatically copies objects from a source bucket in one region to a destination bucket in another region.  

- **How it works:**  
  - You configure replication rules (source → destination).  
  - Every new object (and some metadata changes) in the source bucket are automatically replicated to the destination.  
  - Replication is **one-way** unless you set up rules in both directions.  

- **Requirements:**  
  - The source and destination buckets must have **different names**.  
  - Proper **IAM roles and policies** must be in place so S3 can replicate objects.  

- **Use Cases:**  
  - **Disaster recovery** (copy data across regions).  
  - **Compliance** (store data in multiple geographies).  
  - **Latency optimization** (keep data closer to users).  

---

## Why S3 Can Be Cheaper Than On-Prem Storage

At first glance, buying your own storage hardware may seem cheaper, but at large scale S3 is often more cost-effective because:

- **No upfront capital expense** — no need to buy disks, servers, or racks.  
- **Elastic scaling** — you only pay for what you use; no wasted capacity.  
- **Built-in durability** — AWS replicates across Availability Zones without extra cost; on-prem you’d need multiple data centers.  
- **Lower operational costs** — no power, cooling, hardware refreshes, or staff overhead.  
- **Lifecycle management** — S3 can auto-move older data to cheaper tiers (Infrequent Access, Glacier, Deep Archive).  
- **Economies of scale** — AWS buys hardware at massive scale and passes savings to customers.  

👉 **Interview TL;DR:**  
S3 is cheaper at scale because you avoid CapEx, reduce OpEx, get built-in replication, and can tier data automatically.  

---

## Example

Check out the implementation in [`s3.py`](./s3.py).
