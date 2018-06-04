'''
Use the variables below to overwrite application default values.
Please DO NOT modify the same variables from elsewhere in the application.
This file is originally git-ignored but you should always keep this file 
away from distributions if it contains user-customized values.

Description:
# When you use Encors as a service for a group of users, and want to limit
this service to allow requests from only a few origins (i.e., domain), add
the hostnames to the list. e.g.: yourhostname.com, yourcompany.com
# Leave this list empty to allow requests from all origins.
'''
ALLOWED_ORIGINS = []