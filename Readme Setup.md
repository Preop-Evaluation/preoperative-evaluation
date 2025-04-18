For testing, some users have been created in App/controllers/init.py, these are their credentials:
Anesthesiologist: email: mikesmith@mail.com 
		  password: password
Doctor: email: janedoe@mail.com
	password: password
Patient: email: johndoe@mail.com
	 password: password
Admin: email: admin@mail.com
       password: admin123

You may need to type /init at the end of the URL if any internal server errors appear at authentication. 
See Trello for link to live website. 

NOTES: 
Render blocks outgoing ports for the mail server used. Railway was chosen as the hosting website.
The application was set up using Gmail's email ports and protocols. To use another email service provider "App/default_config.py" must be edited with the relevant information for the other provider. 
The Application is set up to use "preopassessmentteam@gmail.com" as the sender of the emails. To use another Gmail, the mail_username and mail_password fields in App/default_config.py must be changed. NB, you must first create an "app password" for the gmail account. 

CREATING AN APP PASSWORD: 
Navigate to account settings, then security, and search for "app passwords" using the search bar on the top. Once there, you will be prompted to enter your password, and then you can create an app password once you enter a name. This will be the password to put into the mail_password variable. 
NOTE: 2FA must be enabled to generate, and do not share this password. 

In a real world use case, the mail_username and mail_password fields would be removed from App/default_config.py and placed into the Environment Variables for the website. A new Gmail account was set up purely for testing and demonstration purposes. 


ENVIRONMENT VARIABLES: 

ENV
PRODUCTION


JWT_ACCESS_TOKEN_EXPIRES
7


MAIL_SERVER
smtp.gmail.com


MAIL_USERNAME
preopassessmentteam@gmail.com


MAIL_PASSWORD
rxzd fvjr nlmy xrbv


SECRET_KEY
SECRET_KEY


SQLALCHEMY_DATABASE_URI
sqlite:///temp-database.db






