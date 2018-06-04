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

## Use the Encors service
You can either install and run the Encors service locally or in your organization network.

In addition, you can use the free Encors service from http://encors.me/.

## Request a resource
There are two ways to pass the requested URI to the Encors servcie you chose:

> * Passing it as the parameter to the end of the service url, via a **GET** method. For examples:

>   1. using your own Encors service:

>   `http://localhost:8000/http://www.pjliang.com/json/fake-users.json`

>   2. using the free Encors service from http://encors.me/:

>   `http://encors.me/http://www.pjliang.com/json/fake-users.json`

> 2. Passing it as an 'encors-target' key-value pair parameter in header, via a **POST** method. For example:

>  * set a key-value pair with  **encors-target** as key, and  **http://www.pjliang.com/json/fake-users.json** as value.


## Acceptable Parameter(s)

Here is a set of acceptable header parameters to use. Only the **encors-target** parameter is acceptable through url via **GET** method. Any other must be provided in request header. Detailed examples will be given below.

### *encors-target*

>The resource to request. Accept values:

> * a valid URI

> Note: If provided through the request url via **GET** method, the key is omitted. If provided in both url and header, value in header will be accepted.

> Examples:

> `http://encors.me/http://www.pjliang.com/json/fake-users.json`

> `(in request header) encors-target=http://www.pjliang.com/json/fake-users.json`

### *encors-jsonp*

> If you intend to get a response with the JSONP method support. It will try to return the resource in a JSONP way. See [JSONP in W3School](https://www.w3schools.com/js/js_json_jsonp.asp).

> Accepted values:

> * **jsonp** ( yes. use the string literal 'jsonp' as a value)

> Note: Only a resource with a content-type: **application/json** will be passed with JSON Paddings. Other resource types will skip this and return in its original content-type.

> Example:

> `(in request header) encors-jsonp=jsonp`

## Service configuration

You can configure your Encors service to meet your own needs:

> 1. To limit the size of resource been passed through your Encors service:

>  Modify the value of *CONTENT\_SIZE\_LIMIT\_IN\_BYTE* variable in encors\_conf.py

>    `CONTENT_SIZE_LIMIT_IN_BYTE = 2048000`

>   Content size is measured in byte.

> 2. To control to your service to only accept requests (via GET or POST method) from a list of recognized origins (aka: domain names):

>   Add an origin to encors\_allowed\_origins.py

>  `ALLOWED_ORIGINS = ['pjliang.com', 'github.com']`

## Limitations in Encors (current version)

1. allowed\_origins only match the entire hostname, but do not accept wildcard.

2. content size limit will be applied globally across the entire service regardless allowed\_origins or authentication tokens, GET or POST method.

3. Service in https is not tested yet.

4. It only works for resources which don't originally have an 'Access-Control-Allow-Origin' header. For those already have such access control, Encors can't help.

## License, Terms & Conditions
Please refer to the LICENSE file in this project.

##Third-Party Library Disclosures Notice 
Please refer to the NOTICE file in this project.

## Resources
For more information about CORS, please refer to:

* https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
* https://en.wikipedia.org/wiki/Cross-origin_resource_sharing
* https://enable-cors.org/
* https://www.w3schools.com/js/js_json_jsonp.asp
