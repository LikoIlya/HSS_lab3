rs.initiate(
   {
      _id: "rs-shard-3",
      version: 1,
      members: [
         { _id: 0, host : "shard3-1:27017" },
         { _id: 1, host : "shard3-2:27017" },
		 { _id: 2, host : "shard3-3:27017" },
      ]
   }
)