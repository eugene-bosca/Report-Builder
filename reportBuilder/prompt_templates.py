PR_PROMPT_TEMPLATE = """
Act like a software developer who is working on a project for a client who does not have any developer knowledge and wants an update on the progress of his website.

Here are the titles, descriptions, and what type of change occured in the pull requests:

{pr_data}

Based on the pull requests' title, description and what type of change occured, please provide a summary that highlights the following:

1. Objective/Goal: What is the purpose or objective of this pull request? What problem is it addressing or feature is it adding?

2. Changes Made: What specific changes have been made in this pull request? Is it introducing new functionality, fixing a bug, or improving existing code/documentation?

3. Implementation Details: Are there any notable implementation details worth mentioning? For example, did the pull request involve major architectural changes, performance optimizations, or the addition of new dependencies?

4. Testing: How has this code been tested? Has it undergone unit tests, integration tests, or manual testing? Are there any specific testing methodologies or tools worth noting?

5. Dependencies/References: Are there any external dependencies or references involved in this pull request? For instance, does it rely on a particular library, API, or documentation?

The summary should be divided into bullet points for each pull request.
"""

GLOSSARY_PROMPT_TEMPLATE = """
Extract the uncommon terms from the following response and put them in a list with their definitions:

{description}
"""
