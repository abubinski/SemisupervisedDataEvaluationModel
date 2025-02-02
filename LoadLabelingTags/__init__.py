import logging
import requests
import json
import os
import azure.functions as func

# Note, as of 8/7/2019, the python client is not forming URLs correctly.  As a result this sample uses native HTTP calls to the training library.
# from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient

# https://2.python-requests.org//en/latest/api/
# https://stackoverflow.com/questions/9746303/how-do-i-send-a-post-request-as-a-json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('ML Professoar HTTP trigger function LoadLabelingTags processed a request.')

    # Get Cognitive Services Environment Variables
    ProjectID = os.environ["projectID"]
    TrainingKey = os.environ['trainingKey']

    if ProjectID:
        LabelsJson = req.params.get('LabelsJson')
        if not LabelsJson:
            try:
                LabelsJson = req.form['LabelsJson']

            except Exception as e:
                Message = str(e)
                return func.HttpResponse(
                    "Please pass JSON containing valid labels on the query string or in the request body using the parameter name: LabelsJson.  Error: " + Message,
                    status_code=400
                )
        
        if LabelsJson:

            endpoint = os.environ['clientEndpoint']

            # the consol app at this address shows how to properly form URLs for Cognitive Services custom model development https://westus2.dev.cognitive.microsoft.com/docs/services/fde264b7c0e94a529a0ad6d26550a761/operations/59568ae208fa5e09ecb9984e/console
            Endpoint = endpoint + "/customvision/v3.0/Training/projects/" + ProjectID + "/tags"

            # set looping tracking variables
            CountOfLabelsAdded = 0
            CountOfDuplicateLabels = 0

            # code assumes json is in the form: {"Labels":["Hemlock","Japanese Cherry"]}
            LabelDictionary = json.loads(LabelsJson)

            # loop through all labels passed into the function and add them to the project passed into the function
            for Label in LabelDictionary['Labels']:
                headers = {'Training-key': TrainingKey}
                params = {'name': Label}
                response = requests.post(Endpoint, headers=headers,
                                        params=params)
                if "TagNameNotUnique" in response.text:
                    logging.info("Tag " + Label + " is already in project and not unique, project id: " + ProjectID)
                    CountOfDuplicateLabels = CountOfDuplicateLabels + 1
                else:
                    CountOfLabelsAdded = CountOfLabelsAdded + 1
                
            return func.HttpResponse("Loaded " + str(CountOfLabelsAdded) + " labels into project id: " + ProjectID + "  Note: " + str(CountOfDuplicateLabels) + " labels were duplicates to existing project labels.  See log file for label names.")
    else:
        return func.HttpResponse(
             "Please configure projectID and/or trainingKey in your environment variables.",
             status_code=400
        )
