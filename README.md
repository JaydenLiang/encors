# Encors
CORS (Cross-Origin Resource Sharing) Proxy

### version: 1.0.0

## what it is and what it does?
A lightweight proxy service to bypass the so-called  "no 'Access-Control-Allow-Origin' header is present on the requested resource" issues when you try to load a resource using XHR(XMLHttpRequest) such as AJAX in JavaScript.

It currently offers you a proxy server run in a python3 environment, and will ideally offer you more choices in environments such as nodeJS, in the future :).

You can deploy it as a SaaS for your organization, or run it on-demand.

## how it works?
It grabs whatever resource you request and wrap it with an appropriate  'Access-Control-Allow-Origin' header and sends it back to you as the response to your request.

## limitation?
Yes! It only works for resources which don't originally have this header. For resources that already have such access control, Encors can't help. A full list of  limitations will be discussed in the **Limitations in Encors** section.

# Installation

## Install with source code
It's highly recommended that you create a python3 [virtual environment](https://docs.python.org/3/tutorial/venv.html) to run this service. However, make sure you are in a python3 environment then the following installation will have no difference in a virtual environment or real environment.
> 1. Download it from GitHub repository: [jaydenliang/encors](https://github.com/JaydenLiang/encors/) or clone it from your CLI:

>   `git clone https://github.com/JaydenLiang/encors.git`

> 2. Install dependencies:

>  `pip install -r encors/python/requirements.txt`

>3. Install a Python WSGI Http server. It's up to your choice but I use [Gunicorn](http://gunicorn.org/) as an example:

>  `pip install gunicorn`

>4. Set Encors up and running:

>  `gunicorn --chdir encors/python/src/encors:app`

>You will see an http server is up and listening to incoming requests on http://localhost:8000

> More advanced configurations for the http server please see documentation of your own server choice.

## Install with Docker repository

This section of installation requires a [Docker](https://www.docker.com/) environment instead of a Python3 environment on your device so please prepare a Docker environment before following the instructions.

> 1. Pull the latest Encors for Python image from docker repository:

>  `docker pull encors/encors-py`

> 2. Run it as a daemon container binding local port 8000 to port 8000 of the container:

>  `docker run -d -p 8000:8000 encors-py`

>  Then Encors is ready on: **http://localhost:8000/**

>  Or you can bind the service to any other local port if 8000 has been used.

# Usage

## Request a resource
You can either install and run it locally, in your organization network, or you can use the free Encors service from http://encors.me/. To load a resource from: https://jsonplaceholder.typicode.com/users, you can do it:

> 1. using your own Encors service:

>   `http://localhost:8000/?src=https://jsonplaceholder.typicode.com/users`

> 2. using the free Encors service from http://encors.me/:

>   `http://encors.me/?src=https://jsonplaceholder.typicode.com/users`

## Parameters

All parameters available in GET method must be sent via url query in GET method; those in POST method must be sent via request header in POST method.

### *src*

>The URI of resource to request. Available in GET, POST methods.

> Accepted values: any valid URI.

### *format*

>To specify the content type of response. Available in GET, POST methods.

> Accepted values:

> 1. text
> 2. json

### *authentication*

> To use one or any authentication token to allow for a limit number of users to request from your service. Available in POST method.

> Note: authentication tokens can be defined in cors_authentications.py

## Service configuration

You can configure your Encors service to meet your own needs:

> 1. To limit the size of resource been requested able to get through your Encors service:

>  Modify the value of *CONTENT\_SIZE\_LIMIT\_IN\_BYTE* variable in encors\_conf.py

>    `CONTENT_SIZE_LIMIT_IN_BYTE = 2048000`

>  Value is count in byte.

> 2. To limit your service to accept requests (via GET method) from a list of pre-defined origins (aka: domain names) only:

>   Add an origin to encors\_allowed\_origins.py

>  `ALLOWED_ORIGINS = ['pjliang.com', 'github.com']`

> 3. To limit your service to accept requests (via POST method) from those who know an authentication token only:

>  Add a token to encors\_authentications.py, for example:

>  `AUTHENTICATIONS = ['UnGZw9rFOVPqkVTimaAQE8T7WE3aJBdt', '4QZGYBZASwoey29uh5bffO8PsjxP5QYC']`

>  Then, let them know a token, and voilà! They can now use a token to send a request from your Encors service via POST method.

## Limitations in Encors (current version)

1. allowed\_origins only match the entire hostname, but do not accept wildcard.

2. content size limit will be applied globally across the entire service regardless allowed\_origins or authentication tokens, GET or POST method.

3. Service in https is not tested. Don't expect it to work in https, please.

4. It only works for resources which don't originally have an 'Access-Control-Allow-Origin' header. For those already have such access control, Encors can't help.

## License, Terms & Conditions
Please refer to the LICENSE file in this project.

##Third-Party Library Disclosures 
Please refer to the NOTICE file in this project.

## Resources
For more information about CORS, please refer to:

* https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
* https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
* https://enable-cors.org/
