PR_JSON = """
    {{
        search(
            first: 100,
            query: "repo:{repo} is:pr is:merged merged:{since}..{until} sort:updated-asc",
            type: ISSUE,
        ) 
        {{
            issueCount, #total number of pull requests
            nodes {{
                ... on PullRequest {{
                    title #title of each pull request
                    bodyHTML #body of each pull request in HTML format
                    createdAt #date and time the pull request was created
                    mergedAt #date and time the pull request was merged
                    
                    files(first: 2) {{
                        nodes {{
                            path #path of each file changed in the pull request
                            additions #number of lines added in the pull request
                            deletions #number of lines deleted in the pull request
                            changeType #type of change (ADDITION, DELETION, or MODIFICATION)
                        }}
                    }}
                    author {{
                        login #username of the author of the pull request
                        ... on User {{
                            id
                            name
                        }}
                    }}
                }}
            }}
        }}
    }}
    """