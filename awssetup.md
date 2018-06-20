
# AWS Setup Guide
## Register for an AWS Account
1. Go to the Amazon Web Services home page.
2. Choose Sign Up.
Note: If you've signed in to AWS recently, it might say Sign In to the Console.
3. Type the requested account information, and then choose Continue.
*Note: If Create a new AWS account isn't visible, first choose Sign in to a different account, and then choose Create a new AWS account. When creating a new account, be sure that you enter your account information correctly, especially your email address. If you enter your email address incorrectly, you might not be able to access your account or change your password in the future.*
4. Choose **Personal** or Professional.
5. Type the requested company or personal information.
6. Read the AWS Customer Agreement, and then check the box.
7. Choose Create Account and Continue.
*Note: After you receive an email to confirm that your account is created, you can sign in to your new account using the email address and password you supplied. However, you must continue with the activation process before you can use AWS services.*
8. Add a payment method
*On the Payment Information page, type the requested information associated with your payment method. If the address for your payment method is the same as the address you provided for your account, choose Secure Submit.*
9. Otherwise, choose Use a new address, type the billing address for your payment method, and then choose Secure Submit.
10. Verify your phone number
*On the Phone Verification page, type a phone number that you can use to accept incoming phone calls.
Enter the code displayed in the captcha.*
11. When you're ready to receive a call, choose Call me now. In a few moments, an automated system will call you.
12. Type the provided PIN on your phone's keypad. After the process is complete, choose Continue.
13. Choose an AWS Support plan
*On the Select a Support Plan page, choose one of the available Support plans. For a description of the available Support plans and their benefits, see AWS Support - Features. Basic Support is the best for the free account*

After you choose a Support plan, a confirmation page indicates that your account is being activated. Accounts are usually activated within a few minutes, but the process might take up to 24 hours.

***Note**: You can sign in to your AWS account during this time. The AWS home page might continue to display a button that shows "Complete Sign Up" during this time, even if you've completed all the steps in the sign-up process. When your account is fully activated, you'll receive a confirmation email. After you receive this email, you have full access to all AWS services.*

## Installing the CLI
### Windows
The AWS CLI is supported on Microsoft Windows XP or later. For Windows users, the MSI installation package offers a familiar and convenient way to install the AWS CLI without installing any other prerequisites.

When updates are released, you must repeat the installation process to get the latest version of the AWS CLI. If you prefer to update frequently, consider  [using pip](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#awscli-install-windows-pip)  for easier updates.


1.  Download the appropriate MSI installer.
	-   [Download the AWS CLI MSI installer for Windows (64-bit)](https://s3.amazonaws.com/aws-cli/AWSCLI64.msi)
	-   [Download the AWS CLI MSI installer for Windows (32-bit)](https://s3.amazonaws.com/aws-cli/AWSCLI32.msi)    
2.  Run the downloaded MSI installer.
3.  Follow the instructions that appear.
The CLI installs to  `C:\Program Files\Amazon\AWSCLI`  (64-bit) or  `C:\Program Files (x86)\Amazon\AWSCLI`  (32-bit) by default. To confirm the installation, use the  `aws --version`  command at a command prompt (open the START menu and search for "cmd" if you're not sure where the command prompt is installed).

Post install, run the following command and verify that the software is properly installed. If you receive an error that the command is not found, please visit [this AWS Support Page](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html#awscli-install-windows-path) to find directions on how to add the executable to your path
	```batch
	aws --version 
	> aws-cli/1.11.84 Python/3.6.2 Windows/7 botocore/1.5.47
	```
### Mac
0. Ensure that Python 2 version 2.6.5+ *or* Python 3 version 3.3+ is installed. You can verify this by running
	```bash
	python --version
	```
1. Download the [AWS CLI Bundled Installer](https://s3.amazonaws.com/aws-cli/awscli-bundle.zip) using the following command:
	```bash
	curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
	```
2. Unzip the package
	```bash
	unzip awscli-bunzle.zip
	```
3. Run the install executable
	```bash
	sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
	```
### Linux/Unix Install
Dude, you're already running linux. Just do a `pip install awscli --upgrade --user` and be on your merry way. Do you really need me to explain how pip works?
## Configuring the CLI
1. Navigate to https://console.aws.amazon.com/iam/home#/users to create a new user
2. Select "Add User" from the top
3. Name the user. You can name this `AWS CLI Laptop` for convenience
4. Click the checkbox next to `Programmatic Access`
5. Select the tab `Attach existing policies directly`
6. The first item should be called `Administrator Access`. If not, please search for it in the search box
7. Select the checkbox next to `Administrator Access`
8. Click `Next: Review`
9. Click `Create User`
10.  Copy the `Access key ID` and `Secret access key` to a notepad document, or click `Download .csv`. Do not navigate away from this page without copying these keys! Otherwise, they must be generated again
11. Navigate to the `.aws` directory inside of your home directory (Windows: `C:\Users\%username%\.aws`) (Mac: `~\.aws`)
12. Verify that a `credentials` and `config` file exist. (*Note: These files do not have file extensions. Do not add an extension*)
13. Open the `credentials` file and ensure that the contents are that of your `Access key ID` and `Secret access key`. Be sure there is an extra blank line at the end of the file. The file should be in this format:
```
[default]
aws_access_key_id = ABCDEFGHIJKLMNOPQRSTUVWZYZ
aws_secret_access_key = abc123abc123abc123abc123

```
14. Open the `config` file and ensure that the contents are as follows. Be sure there is an extra blank line at the end of the file.
```
[default]
region = us-east-1
output = json

```
15. Test that you are able to use the CLI by running the following command from a cmd/terminal window:
`aws ec2 describe-instances`. Check that you are not getting an authentication error.
## Install Issues
Please visit the following websites if you are having issues:
- [Windows](http://lmgtfy.com/?q=amazon+aws+cli+install+windows+troubleshooting)
- [Mac](http://lmgtfy.com/?q=amazon+aws+cli+install+mac+troubleshooting)