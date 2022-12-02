# waste-classification

### This project is built with:
✔️  Keras

✔️  Django

✔️  Postgres

✔️  AWS S3

✔️  AWS RDS

✔️  Heroku

### Features:
✔️  Image classification into 12 categories

✔️  Based on a user's geolocation , API provides disposal instructions and a list of local recycling/donation centers for the predicted label if it's recyclable/reusable

❕  Note: Free tier Heroku dyno will sleep after 30 minutes of inactivity which might affect the server response time interval

### ➖ API is available at: [https://waste-classification-demo.herokuapp.com/predict/](https://waste-classification-demo.herokuapp.com/predict/)
(no longer working after heroku removed their free tier 😕)

### ➖ Request body: 
        
        ➕ file    :    ?image
        ➕ long    :    ?longitude
        ➕ lat     :    ?latitude
