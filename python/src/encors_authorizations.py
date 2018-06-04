''''
Use the variables below to overwrite application default values.
Please DO NOT modify the same variables from elsewhere in the application.
This file is originally git-ignored but you should always keep this file 
away from distributions if it contains user-customized values.

Description:
# When you use Encors as a service for a group of users, and want to limit
this service to allow requests which provide with any of authorizations 
in the list below in their headers in POST method.
# Leave this list empty to disable authorization. i.e., service works 
without the authorization header.
'''
AUTHORIZATIONS = []