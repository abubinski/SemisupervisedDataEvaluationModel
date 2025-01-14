import logging
import time
import os

from datetime import datetime

import azure.functions as func

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageUrlCreateEntry

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('ML Professoar HTTP trigger function TrainModel processed a request.')

    # Get Cognitive Services Environment Variables
    projectID = os.environ["projectID"]
    trainingKey = os.environ['trainingKey']
    endpoint = os.environ['clientEndpoint']
    publish_iteration_name = "SampleTreeDetection @ " + str(datetime.now())
    prediction_resource_id = os.environ['predictionID']

    trainer = CustomVisionTrainingClient(trainingKey, endpoint=endpoint)

    try:
        iteration = trainer.train_project(projectID, force_train=True)
        while (iteration.status != "Completed"):
            iteration = trainer.get_iteration(projectID, iteration.id)
            logging.info("Training status: " + iteration.status)
            time.sleep(1)

        # The iteration is now trained. Publish it to the project endpoint
        trainer.publish_iteration(projectID, iteration.id, publish_iteration_name, prediction_resource_id)

    except Exception as e:
        message = str(e)
        logging.info(message)

    return func.HttpResponse(
        "Training complete for ProjectID: " + projectID + " publisehed under iteration name: " + publish_iteration_name,
        status_code=400)

