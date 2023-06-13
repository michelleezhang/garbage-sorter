import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.applications.mobilenet_v2 import decode_predictions
import numpy as np
import os 
from configparser import ConfigParser
import boto3
import pathlib
from PIL import Image
import urllib
import json
import base64

# Load the pre-trained MobileNet model
model = tf.keras.applications.MobileNet(weights='imagenet')

def lambda_handler(event, context):
    try: 
        #Setup access to S3 bucket with relevant credentials
        config_file = 'credentials'
        s3_profile = 's3-read-write'
        print("The path is: ", os.getcwd())

        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = 'credentials'
        boto3.setup_default_session(profile_name=s3_profile)

        configur = ConfigParser()
        configur.read(config_file)
        bucketname = configur.get('s3', 'bucket_name')

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucketname)

        #Downloads the image from S3 based on the key
        bucketkey = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        actual = '/tmp/' + bucketkey
        bucket.download_file(bucketkey, actual)

        # Load and preprocess the input image
        img = image.load_img(actual, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Make predictions
        predictions = model.predict(x)
        predicted_class = tf.keras.applications.imagenet_utils.decode_predictions(predictions)[0][0][1]

        print("The predicted class is: ", predicted_class)

        # Classify recyclability based on if it is in the recyclability dictionary or not
        recyclable = {'binder': True, 'ring-binder': True, 'notebook': True, 'book jacket': True, 'dust cover': True, 'dust jacket': True, 'dust wrapper': True, 
                'crossword puzzle': True, 'crossword': True, 'menu': True, 'comic book': True, 'napkin': True, 'toilet tissue': True, 'toilet paper': True, 
                'paper towel': True, 'bathroom tissue': True, 'envelope': True, 'file': True, 'plastic bag': True, 'milk can': True, 'water bottle': True, 
                'pill bottle': True, 'ballpoint': True, 'ballpoint pen': True, 'ballpen': True, 'whiskey jug': True, 'water jug': True, 'beer glass': True,
                'Petri dish': True, 'wine bottle': True, 'beaker': True,  'measuring cup': True, 'pop bottle': True, 'soda bottle': True, 'beer bottle': True, 
                'bucket': True, 'pail': True, 'plunger': True, 'rubber eraser': True, 'rubber': True, 'pencil eraser': True, 'wooden spoon': True, 'cup': True, 
                'plate': True, 'pot': True, 'pitcher': True, 'soup bowl': True, 'flowerpot': True, 'ewer': True, 'coffee mug': True, 'mixing bowl': True, 
                'vase': True, 'binoculars': True, 'field glasses': True, 'opera glasses': True, 'sunglasses': True, 'dark glasses': True, 'shades': True, 
                'loupe': True, "jeweler's loupe": True}

        if predicted_class in recyclable.keys():
            recyclability = 'recyclable'
            to_upload = bucketkey[:-4] + '_recyclable.jpeg'
        else:
            recyclability = 'not recyclable'
            to_upload = bucketkey[:-4] + '_notrecyclable.jpeg'

        # Print the classification
        print(f"The object is {recyclability}, predicted as {predicted_class}")

        #Upload the image by appending to image name back to S3 
        bucket.upload_file(actual, 
                        to_upload, 
                        ExtraArgs={
                            'ACL': 'public-read',
                            'ContentType': 'text/plain'
                        })
        
        return {
                'statusCode': 200,
                'body': json.dumps(recyclability)
            }
    except Exception as err:
        print("**ERROR**")
        print("The error is: " + str(err))
        return {
                'statusCode': -1,
                'body': json.dumps(str(err))
            }
