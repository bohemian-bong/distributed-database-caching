1) Basic Structure
- What we are making? 
A cache server, which caches database queries and provides faster access to its output. 
It is independent from the database as its main motive is to be transparent to the user's database. 
User can selectively send queries to this cache server without the need to create connection between the database and cache server.
It should handle data inconsistency between cached queries and database updated values.
Lastly, it should be distributed by some means (sharding/replication).

- How much it is done?
The cache server has two different API calls made.
A postQuery API which can be used by the user server to post certain queries along with its output.
A getQuery API which can be used by the user server to get output of certain queries.
The postQuery API sets a timestamp for each query when it is last updated.
If a query is accessed the last timestamp should not exceed a standard expiration time. This is how a kind of LRU is implemented.

2)  Query Normalization
We need a process to normalize each query sending by the user.
Normalization will include two logically same queries getting mapped to a single query.
Addition to that, normalization should also fetch the fields which are getting affected/viewed by the query.

2) Query Storing
Each normalized query will be mapped to its output.
Fields will be mapped to a set of queries which it can create an affect.
Also along with that there should be a timestamp.

2) Handling Database Updates
We are proceeding with a Change Data Capture (CDC) approach.
Each update query should pass through the cache server, and check if the field affected
has any queries mapped to it or not. If it is, then we should either invalidate that record
or ask server to re-run this queries and give their updated output in free time.

3) Cache Expiration Policy
Currently its a timestamp based approach but does not remove entry automatically.
Approaches like LFU and LRU needs to be tested.

4) Distributed
Last thing is to make the cache server and its cache distributed.
- Sharding
    a) Consistent Hashing - The query is hashed, and consistent hashing directs it to the appropriate cache node.
    b) Region-Based Partitioning 
- Replication
    a) Master-Slave Replication - A master node handles write operations, and slave nodes handles read operations.
    b) Peer-to-Peer Replication - All nodes are equal (no master), and data is replicated across them.

