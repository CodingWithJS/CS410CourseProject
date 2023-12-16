# CS410CourseProject

To Run the project in local

For Backend (after navigating to /backend folder)
1. Run pip install -r requirements.txt
2. After all the packages are installed run python app.py
3. This should start the backend server on port 5000

For frontend
1. Navigate to frontend/student-review-feedback folder
2. Run npm install to install dependencies
3. Run npm start
4. The react app should come up on the default port 3000
5. Navifgate to this url http://localhost:3000/ and proceed with the steps mentioned in demo

Frontend is also deployed to cloud hosting platform netlify and you can check it from here as well:https://student-course-review-feedback.netlify.app/ 

There was issue deploying the backend code to hosting platform due to many hosting platforms having a maximum size limit of 500MB while the setup of backend code requires more than 4 GB due to its dependencies like pytorch and tensorflow

Work done
Mahesh - Basic react and backend setup and initial code using Bert Sentiment Analysis
Jeremy - CSV upload, Text Summarization and UI enhancements

Please Note:
- CSV only supports UTF 8 characters
- Also the demo has been added as a Demo.mp4 in the root folder