## Required tools (to run through Docker):

Python, Docker, Postman. 

Make sure you have Python Flask package on your local computer.

Use command below to install Flask in the python environment.

pip install -U Flask



## Follow 3 steps to start docker container

### 1. Go to cmd and cd to your current directory.

### 2. Type

docker build -t score .

### 3. Type

docker run -p 11111:11111 --name score_container score

&nbsp;
##### If you want to delete/change container, use the command below and execute step 2 and 3

docker rm -f score_container

##### To start this container, use the command below

docker start score_container

##### To stop this container, use the command below

docker stop score_container



## Use postman or other API testing tools.

### 1. POST

Select raw under the Body and JSON as the data type
and type
http://your_ip:11111/receipts/process

paste in the JSON example, click 'send' and you will receive an id.

Example:
127.0.0.1:11111/receipts/process

    {
      "retailer": "Target",
      "purchaseDate": "2022-01-01",
      "purchaseTime": "13:01",
      "items": [
        {
          "shortDescription": "Mountain Dew 12PK",
          "price": "6.49"
        },{
          "shortDescription": "Emils Cheese Pizza",
          "price": "12.25"
        },{
          "shortDescription": "Knorr Creamy Chicken",
          "price": "1.26"
        },{
          "shortDescription": "Doritos Nacho Cheese",
          "price": "3.35"
        },{
          "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
          "price": "12.00"
        }
      ],
      "total": "35.35"
    }


### 2. GET

Type in 
http://you_ip:11111/receipts/{id}/points

with the id received in the previous step.

Example: 
127.0.0.1:11111/receipts/b80c3733-a02b-4d89-abc6-dcadb4581a8d/points



## Other files:

api.yml: formal definition of JSON data.

app.py: body of code.

Dockerfile: file to run on docker.

requirements.txt: required packages to be installed in python Docker image.

test_data.txt: edge cases to be tested.

unit_test.py: test s single case.

demo.mp4: demo video.
