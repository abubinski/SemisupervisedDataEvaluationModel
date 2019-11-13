# Semi Supervised Data Evaluation Model

This sample is a prerequisite to using the Semisupervised Orchestration Framework (ML Professoar). Follow the steps below to deploy a Computer Vision or Custom Vision model to Azure with Azure Functions and return JSON image analysis results.  

The module can be configured to perform any of the vision analysis services by setting the appropriate environment variable. 

## Prerequesites 

In order to run this sample, you'll need to install the following software:
- VS Code <https://code.visualstudio.com/Download>
- Python (use version 3.6 because Azure Functions only supports that version and if your OS is 64 bit pick the 64 bit version or it can create path issues) <https://www.python.org/downloads/windows/>
- Node.js <https://nodejs.org/en/download/>
- Docker client <https://docs.docker.com/docker-for-windows/install/>

### Create a Custom Vision Account

Sign up for a free Microsoft Cognitive Services account <https://azure.microsoft.com/en-us/try/cognitive-services/>. Then log into the Cognitive Services custom model project management portal, it is separate from the Azure Portal, and set up your project.  The portal can be found here: <https://www.customvision.ai>

## Create Azure Resources via Azure Cloud Shell

Use the following set of commands in the Azure Cloud Shell to create the Azure resources necessary to run the model. 

SemisupervisedDataEvaluationModelEnvironmentConfiguration.ps1  (in this repo) and SemisupervisedOrchestrationFrameworkEnvironmentConfiguration (from the ML Professoar repo). 

### *Todd to add the SemisupervisedOrchestrationFrameworkEnvironmentConfiguration.ps1 file to this repo*

How to upload and run powershell scripts in Azure:
<https://www.ntweekly.com/2019/05/24/upload-and-run-powershell-script-from-azure-cloud-shell/>

If you have multiple subscriptions, use the following code snip to establish which subscription you'd like you use for your resource group and resources.

        az account set --subscription <name or id>

Start with uploading the evaluation ps1 file and then do the orchestration file

Create a separate resource group when you run the orchestration file

The http address is from the function

Resource Group Details xxxx

When you are done, you should have the following resources in your new resource group:
- sdfd
- sdlfjsdkf

## Create a Function to Run the Model

### Prepare a Python Development Environment in VS Code
If you want to perform custom model development in Python, you will need to complete the following steps to prepare your python development environment:

Start by reading this document: <https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python> then this document: <http://www.roelpeters.be/using-python-in-azure-functions/>

Now before you do anything, you want to avoid environment hell, so read this on working with virtual environments in VS Code: <https://code.visualstudio.com/docs/python/environments.>  The key is making sure when you select an environment in VS Code the environment is activating.  You will know as the begining of the line in the command prompt lists the name of the virtual environment that is active in green.  If there is no grean name then you are working in the default environment.  You cannot run this project in the default (also known as base) environment because Azure functions requires a virtual environment by default.  You can turn this off but it is generally a bad idea.

Setting Up Python Development Environments with VS Code
https://shunsvineyard.info/2019/09/04/setting-up-python-development-environments-with-visual-studio-code/

## VS Code Environment Installations
Start VS Code and open a terminal. From there run the following commands to install the corresponding tools:

-  Azure Functions Core Tools: This enables you to work with Azure Functions from directly within VS Code enabling things like deploy. For more information see <https://github.com/Azure/azure-functions-core-tools#installing>

        npm i -g azure-functions-core-tools --unsafe-perm true  
        pip install -azure-functions
        npm install -g azure-functions-core-tools

- HTTP handling: This will allow you to work with HTTP requests and communicate between the framework and the model.

        pip install requests

- Azure Computer Vision: Depending on whether you are using the Static or Trained model you'll want to install the Computer Vision or Custom Vision Service.
    - For Static:

            pip install azure-cognitiveservices-vision-computervision

    - Or for Trained:
        
            pip install azure-cognitiveservices-vision-customvision 


Install the Following VS Code Extensions

- Python
- Azure Functions
- Azure Account

## Deploy Your Azure Function to the Cloud
After installing, log into Azure from VS Code <https://www.ntweekly.com/2018/01/10/connect-microsoft-azure-directly-visual-studio-code/> and complete the following steps to deploy your function to Azure.

- Click on the Azure plug in icon on the left of your VS Code environment 
- Open your subscription 
- Right click on your project and select "Deploy Function"

## Run Function Quick Start
Now you are ready to start coding.  Start by running this Python Azure Function quick start.  It will provide a very simple function that takes in a name parameter and returns a hello response.  You will then be able to add your code to this function and start deploying and running it.
<https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/quickstarts/python-analyze>

The short sample which calls the static Azure Vision Services image analysis web service uses the vanilla
code generated by the quick start and adds the ability to call the vision API via http, updates the analysis JSON with the average confidence for the target brand, 'Microsoft' as a root key and puts the updated JSON response from the analysis service into the function response for processing by the semisupervised framework.

Once you have the quick start code running you will need to add these imports to the top of your python code in addition to the lines quick start added to your code:

- import os
- import json
- import requests
- from azure.cognitiveservices.vision.computervision import ComputerVisionClient
- from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
- from msrest.authentication import CognitiveServicesCredentials
- from io import BytesIO

You can test the sample function using a public image simply pass in 'test' as your file name to be analyzed and the model will analyze an image from wikipedia, the URL will look something like this: https://{the name of your function app}.azurewebsites.net/{the name of your function}/?name=test or
<https://branddetectionapp.azurewebsites.net/api/detectbrand/?name=test>

## Considerations

Note: If you are using a Jupyter notebook, include the following lines.
%matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image

Finally, if you want to debug locally you will need to read this article about how to set up local debugging.  <https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local>

Long running fucntions ********* need to see if there is a response time limitation on functions and advise how to handle this in the model python.************
