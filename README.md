This is code for dashboard regarding planes
It is has 3 components:
1. a database containing the information
2. an API which pulls data from the database
3. a website which displays the data pulled from the database by the api

To do list and to figure out breakdown:

0. linting - git actions working just fix the code with the lines and what not
    1. flask 8 
    2. using flask 8 update new_thoughts with bit from main 
    3. this then in theory should work perfectly to check the code 
1. unit testing 
    1. figure out how to unit test with pandas
        1. https://www.youtube.com/watch?v=ovvU41ve1FQ
        2. https://stackoverflow.com/questions/41852686/how-do-you-unit-test-python-dataframes
        3. https://penandpants.com/2014/10/07/testing-with-numpy-and-pandas/
        4. Think I'm going to need a fitxtrue then with some mock stuff 
        5. can fixutre and pull headers or something from a csv  bassically create test data 
    2. update code structure so testinng can be done effectively 
    3. figure out test for backend guessing it's some sort of mock 
        1. https://fastapi.tiangolo.com/tutorial/testing/#extended-testing-file
        2. https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#override-a-dependency
    4. firgure out unit test for database and models despite having no functions or stuff to test but they do have stuff 
    5. guessing unit tests should be ran pre docker build as test indiovudal bits 
1.5 docker build/docker compose
2. intergration testing
    1. figure out what to use for unit testing  -can do intergration through pytest as just mutiple functions togther 
    2. figure out unit tests were going to run 
    3. figure out how to do that with github actions 
3. system testing
    1. figure out what things can do system testing
    2. hmm think this is called something else need to check  
4. Other CI/CD stuff to think about:
    1. Do we need to test docker containers 
    2. Do I need distater recovery options
    3. How do I test secuirty of docker containers 
    4. do I need to do something else
5. deploy to aws 
    1. post to repo
    2. then do docker compose in repo 
    3. find out how to ping adddress to web 
