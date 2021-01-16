"""
query { 
  repository(owner: "facebook", name: "react") { 
    createdAt,
    updatedAt,
    forkCount,
    forks(first: 10){
    	nodes{
        createdAt,
      },
    },
    stargazerCount,
    stargazers(first: 10){
      nodes{
        createdAt,
      },
    },
    primaryLanguage{
      name
    },
    languages(first: 5){
      totalCount,
      totalSize,
      edges{
        node {
          name,
        },
        size,
      },
    },
    
  }
}
"""
