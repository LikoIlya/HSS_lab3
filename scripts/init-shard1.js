rs.initiate(
   {
      _id: "rs-shard-1",
      version: 1,
      members: [
         { _id: 0, host : "shard1-1:27017" },
         { _id: 1, host : "shard1-2:27017" },
		 { _id: 2, host : "shard1-3:27017" },
      ]
   }
)