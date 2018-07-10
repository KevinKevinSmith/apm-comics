# APM Comics Install Guide
Welcome to the APM Comics install guide. Follow these directions to build your own Serverless Web Application on AWS, leveraging S3, DynamoDB, Lambda, and API Gateway. For each section, there are both Interactive and Programatic steps (if appropriate). You may choose to follow either, but DO NOT complete both sets of steps.

## Create Dynamo DB Database
### Interactive Steps
1. Navigate to the [DynamoDB Console](https://console.aws.amazon.com/dynamodb/home?region=us-east-1)
2. Select `Create Table`
3. For the "Table Name" enter `apm-comics-prod`
4. For the "Partition Key", enter `itemtype` and select `string` as the data type
5. Check the box for "Add sort key" and enter `itemid` and select `string` as the data type
6. Uncheck the box labeled "Use default settings"
7. Uncheck the boxes labeled "Read Capacity" and "Write Capacity" under the "Auto Scaling" heading. Once unchecked, the "Read capacity units" and "Write capacity units" become un-grayed, and you can enter values unto these boxes.
8. Enter a value of `2` into the "Read Capacity" and "Write Capacity" boxes
9. Check "Enable Encryption"
10. Click "Create"
### Programatic Steps
1. Launch a terminal window in the `/dynamo` folder of the repo
2. Run the following command:<br/>
    `aws dynamodb create-table --table-name "apm-comics-prod" --cli-input-json file://schema.json` 
    
## Create S3 Bucket
### Interactive Steps
1. Navigate to [S3 Console](https://s3.console.aws.amazon.com/s3/home?region=us-east-1)
2. Select "Create Bucket"
3. On Page 1 "Name and region", enter a unique bucket name (e.g. `apm-comics-web-flast` where you replace `flast` with the first letter of your first name and your last name)
4. Click "Next"
5. On Page 2 "Set properties", click on "Default Encryption" and select `AES-256` and click "Save"
6. Click "Next"
7. On Page 3 "Set permissions", under the heading "Manage public permissions", select the drop down "Grant public read access to this bucket"
8. Click "Next"
9. Confirm the properties, and click "Create Bucket"
10. When you are returned to the S3 Console, click on the bucket which you just created
11. Select the "Properties" tab
12. Click on "Static website hosting"
13. Click on the "Use this bucket to host a website" radio button
14. In the "Index document" textbox, enter `index.html`
15. Click Save
16. Launch a terminal window
17. Run the following command to copy the contents of the APM Comics Website to your S3 Bucket:<br/>`aws s3 sync s3://apm-comics-web/web s3://YOUR_BUCKET_HERE --region US-EAST-1 --acl bucket-owner-full-control --acl public-read`<br/>replacing `YOUR_BUCKET_HERE` with the name of the bucket you created in Step 3
18. Attempt to visit `http://YOUR_BUCKET_HERE.s3-website-us-east-1.amazonaws.com` replacing `YOUR_BUCKET_HERE` with the name of the bucket you created in Step 3 and ensure that the page loads. There might not be much there, as the DynamoDB page is not properly set up (yet)

### Programatic Steps
1. Launch terminal window
2. `aws s3api create-bucket --bucket YOUR_BUCKET_HERE --region us-east-1 --create-bucket-configuration LocationConstraint=us-east-1`<br/> replacing `YOUR_BUCKET_HERE` with a unique bucket name (e.g. `apm-comics-web-flast` where you replace `flast` with the first letter of your first name and your last name)
3. `aws s3 sync s3://apm-comics-web/web s3://YOUR_BUCKET_HERE --region US-EAST-1 --acl bucket-owner-full-control --acl public-read`<br/>replacing `YOUR_BUCKET_HERE` with the name of the bucket you created in Step 2
4. `aws s3 website s3://YOUR_BUCKET_HERE/ --index-document index.html --error-document error.html`<br/>replacing `YOUR_BUCKET_HERE` with the name of the bucket you created in Step 2
    
## Setup IAM Roles
### Interactive Steps
1. Navigate to [IAM](https://console.aws.amazon.com/iam/home?region=us-east-1#/home)
2. Select "Policies" from the left sidebar
3. Click "Create Policy"
4. In the new window, select the "JSON" tab and copy directly from the `apm_dynamo.json` file under the `iam` folder of the root directory of the repo
5. Click "Review Policy"
6. Name the policy `apm-comics-dynamo` and in the description, you can mention that `This policy will be used to control the access to the DynamoDB table for the apm-comics project`, or something of the like.
7. Click "Create Policy"
8. When you return back to the "Policies" page, you will see a message that "apm-comics-dynamo has been created".
9. Click "Create Policy" again
10. In the window, select the "JSON" tab and copy directly from the `apm_s3.json` file under the `iam` folder of the root directory of the repo.<br/>**NOTE: You must change the name of the bucket on line 41 of the JSON to match the name of the bucket you created in the previous section! You can replace `YOUR_BUCKET_NAME_HERE` with your bucket name.**
11. Name the policy `apm-comics-s3` and in the description, you can mention that `This policy will be used to control the access to the S3 Bucket for the apm-comics project`, or something of the like.
12. Click "Create Policy"
13. Select "Roles" from the left sidebar
14. Click "Create Role"
15. Select `AWS Service` under "Select type of trusted entity" and `Lambda` under "Choose the service that will use this role"
16. Click "Next: Permissions"
17. In the "Search" box, enter `apm-comics-dynamo`. When the result appears, select the checkbox
18. In the "Search" box, enter `apm-comics-s3`. When the result appears, select the checkbox
19. Select "Next: Review"
20. In the "Role name" textbox, enter `apm-comics-role`
21. Click "Create role"


### Programatic Steps
1. Launch terminal window in the `/iam` folder
2. `aws iam create-policy --policy-name apm-comics-dynamo --policy-document https://s3.amazonaws.com/apm-comics-web/iam/apm_dynamo.json`
3. `aws iam create-policy --policy-name apm-comics-s3 --policy-document https://s3.amazonaws.com/apm-comics-web/iam/apm_s3.json`
4. Navigate to [IAM Roles](https://console.aws.amazon.com/iam/home?region=us-east-1#/roles)
5. Start following the Interactive Steps at Step 13

## Setup Lambda Functions
## Interactive Steps
1. Navigate to [Lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#)
2. Select "Create Function"
3. Click on the "Author from Scrach" box, and enter `apm-comics-getAllItems` in the "Name" textbox
4. Select `Python 3.6` in the "Runtime" textbox
5. Select `apm-comics-role` from the dropdown under "Existing Role"
6. Click "Create function"
7. Scroll down to "Function code" and paste the contents of the `lambda\getAllItems.py` file into the program editor window
8. Select "Save" and check that the save completes successfully
9. Select "Functions" from the navigation menu at the top of the webpage
10. Repeat steps 2-9 for each file in the `lambda\` folder in the repo, except `importData.py`, replacing following the pattern of `apm-comics-fileName` for the "Name" of the function in step 3

## Setup API Gateway
### Interactive Steps
1. Navigate to [API Gateway](https://console.aws.amazon.com/apigateway/home?region=us-east-1)
2. Click "Create API"
3. Select "New API"
4. Enter `apm-comics-api` into the "API name" textbox
5. Click "Create API"
6. Click on the root `/` resource, and select "Actions" -> "Create Resource"
7. In "Resource Name" and "Resource Path" enter `getCart` (Case Sensitive)
8. Check "Enable API Gateway CORS"
9. Click "Create Resource"
10. Click on `/getCart`
11. Select "Actions" -> "Create Method"
12. In the new drop down that appears, select `POST` and click the check mark
13. Click on `POST` under `/getCart`
14. Select `Lambda Function` under "Integration Type" and in the "Lambda Function" textbox, enter "apm-comics-getAllItems", which should be auto predicted
15. Click "Save"
16. You will be promoted with a box to "Add Permission to Lambda Function". Click "OK"
17. Click on `/getCart`
18. Select "Actions" -> "Enable COORS"
19. Click "Enable CORS and replace existing CORS headers"
20. Click "Yes, replace existing values" when prompted to Confirm method changes
21. Repeat steps 6-16 using the values in the following table

|Resource Name|Method|Lambda Function|  
|-------|-------|-------|  
|getCustomer|POST|apm-comics-getCustomer|
|getItem|POST|apm-comics-getItem| 
|getItems|GET|apm-comics-getAllItems| 
|getSession|POST|apm-comics-getSession|  

22. Click on the root `/` resource, and select "Actions" -> "Deploy API"
23. Select `[New Stage]` from the dropdown for "Deployment stage"
24. Enter `prod` as the "Stage name"
25. Click "Deploy"
26. Note the "Invoke URL" which is presented to you
27. Open the [S3 Console](https://s3.console.aws.amazon.com/s3/home?region=us-east-1)
28. Select the `apm-comics-web-flast` bucket you created earlier
29. Navigate to the "js" folder and click on the "script.js" file
30. Click the "download" button
31. Open the downloaded `script.js` file in your favorite text editor
32. Edit the first line to change `apm-comics-web` to the bucket name you created earlier
33. Edit the second line to change the apiURL to the URL created in step 26
34. Save the file
35. Click your browser's back button
36. Click the "Upload" button" and select the `script.js` file you just modified
37. Click "Next"
38. On the "Set permissions" page, under the heading "Manage public permissions", select the drop down "Grant public read access to this bucket"
39. Click "Upload"

## Import Data
### Interactive Steps
1. Navigate to [Lambda](https://console.aws.amazon.com/lambda/home?region=us-east-1#)
2. Select "Create Function"
3. Enter `apm-comics-importData` in the "Name" textbox
4. Select `Python 3.6` in the "Runtime" textbox
5. Select `apm-comics-role` from the dropdown under "Existing Role"
6. Click "Create function"
7. Scroll down to "Function code" and paste the contents of the `lambda\importData.py` file into the program editor window
8. Edit line 26 and change the bucket name to the one created earlier in the S3 section
9. Select "Save" and check that the save completes successfully
10. In the dropdown next to the test button, select "Configure Test Events"
11. In the "Event name" textbox, enter `run`
12. In the code box below, clear it all out, and enter an empty JSON `{ }`
13. Click "Create"
14. Scroll down to "Basic Settings" and set the timeout to `15 sec` 
15. Click "Test"
16. Wait for a `null` return value from the function. A null return indicates that all of your data has been imported!

## Complete
Congratulations! If you now visit `http://YOUR_BUCKET_NAME.s3-website-us-east-1.amazonaws.com`, you should see a functioning Serverless AWS Application!
