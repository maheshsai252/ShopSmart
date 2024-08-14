## Project Overview
ShopSmart is designed to revolutionize your shopping experience by offering product suggestions tailored to your unique preferences, including interests, gender, and other personal factors. Imagine simply entering a prompt and instantly receiving a curated list of products that feel as if they were handpicked just for you. ShopSmart not only brings these products to your fingertips but also provides concise summaries and detailed descriptions to help you understand the key features of each item.

What sets ShopSmart apart is its user-friendly wishlist page, where you can save all your favorite finds. Additionally, our integrated chatbot is always ready to offer advice on which products might best suit your needs. The platform is designed to evolve with you, offering personalized recommendations that adapt as your interests change, ensuring that you always have access to the most relevant and appealing products.

## Project Resources

[![Demo Video](https://img.shields.io/badge/-Demo%20Video-red?style=for-the-badge)](https://www.youtube.com/watch?v=WFkK3tz0280)
[![Application](https://img.shields.io/badge/-Application-yellow?style=for-the-badge)]()

[![User Manual](https://img.shields.io/badge/-User%20Manual-green?style=for-the-badge)](https://docs.google.com/document/d/15pDnNdHlmCXaaEcZROz4v-op_vVbvMunByE-UpY5CHo/edit?usp=sharing)


## Tech Stack
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-4B8BBE?style=for-the-badge&logo=python&logoColor=yellow)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-00A7E1?style=for-the-badge&logo=apache-airflow&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-6558F5?style=for-the-badge&logo=pinecone&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-purple?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-0db7ed?style=for-the-badge&logo=docker&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon_S3-F7CA18?style=for-the-badge&logo=amazon-s3&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2D9CDB?style=for-the-badge&logo=pydantic&logoColor=white)

### Run the application

Clone the project repository:
https://github.com/maheshsai252/ShopSmart.git

Navigate to the project directory:

cd ShopSmart

Create a .env file and add the following environment variables:
```
SNOWFLAKE_USER=xxxx
SNOWFLAKE_PASSWORD=xxxx
SNOWFLAKE_ACCOUNT=xxxx
SNOWFLAKE_WAREHOUSE=xxxx
SNOWFLAKE_SCHEMA=xxxx
SNOWFLAKE_ROLE=xxxx
SNOWFLAKE_DATABASE=xxxx
sasl_username=xxxx
sasl_password=xxxx
bootstrap_servers=xxxx
AWS_ACCESS_KEY_ID = xxxx
AWS_SECRET_ACCESS_KEY = xxxx
pinecone_key = xxxx
openai_key = xxxx
gemini_key=xxxx
JWT_SECRET=xxxx
```

Run Docker compose build for initializing and running the containers for Airflow and Web App.

```
cd Web-Service

docker-compose build
```

Run Docker compose for initializing and running the containers for Airflow, Frontend and Backend.

```
docker-compose up
```

Now the application is up and running. Now navigate to below link to check the application in the web browser.

0.0.0.0:8501

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
