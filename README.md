
## SBQS 2023

# Mock Objects in Software Testing: An Analysis of Usage in Open-Source Projects

## Abstract
Dependencies in software are essential for efficiently structuring and modularizing the code, enabling software components to perform specific tasks, interact, and reuse functionalities. Furthermore, many applications also rely on external components, such as APIs and external services, which can difficult the creation of a testing environment. To overcome these challenges, developers can use mocks to simulate these dependencies,  which becomes particularly useful when dealing with slow or hard-to-create dependencies, such as those requiring network access. Despite the use of mocks in software testing, there are few academic studies to understand the use of this technique. The main objective of this paper is to understand how mocks are used in automated tests
in open-source projects, in addition to quantifying the use of support tools and assessing their impact on test creation. We discovered that Mockito, PHPUnit, Jest, and Mock tools are widely employed for Java, PHP, JavaScript, and Python programs, respectively. We also observed that the presence of mocks is consistent and follows the number of test files in each project. We noted that the external dependencies to the project were the most frequently simulated. However, we found no significant correlation between the number of mocks in the project and code coverage.

## Additional information
This anonymous repository contains generator scripts for the analysis of research questions.

## Install deps
```
pip install -r requirements.txt --user
```

## Using

Alterar a variável ```PROG_LANG``` ao executar o script.

create_final_list.py
cloner.py
count_test_files.py
test_tool_by_descriptor.py
search_mock_use.py

dep_origins.py