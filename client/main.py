# Client-side python app
import requests  # calling web service
import jsons  # relational-object mapping
import uuid
import pathlib
import logging
import sys
import os
import base64
from configparser import ConfigParser

def upload_image(baseurl, image_name):
  '''
  Uploaded image is encoded as a base64 string
  API is called to upload image to S3
  '''
  try:
    # check that image is .jpg (necessary to avoid double triggering the lambda function)
    image_ending = image_name.rsplit('.', 1)[1]
    if image_ending != 'jpg':
      print("Image must have '.jpg' ending")
      return

    # call image api
    api = '/image'
    url = baseurl + api + "/" + image_name

    # covert image to binary file -- returns array of bytes
    with open(image_name, 'rb') as file:
      input_data = bytearray(file.read()) 
    # encode as base64
    input_data = base64.b64encode(input_data)
    input_data = input_data.decode()

    # send encoded image (json) 
    data = {
      'data': input_data
      }
    res = requests.post(url, json=data)
    
    # let's look at what we got back:
    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      return

    # deserialize and extract assets:
    body = res.json()

  except Exception as e:
    logging.error("assets() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return
  

def get_result(baseurl, image_path):
  '''
  Return recyclability classification
  API is called to search for classification and return it
  '''
  try:
    # call api
    api = '/download'
    image_path = image_path.rsplit('.', 1)[0]
    url = baseurl + api + "/" + image_path
    
    res = requests.get(url)

    if res.status_code != 200:
      # failed:
      print("Failed with status code:", res.status_code)
      print("url: " + url)
      if res.status_code == 400:  # we'll have an error message
        body = res.json()
        print("Error message:", body["message"])
      return
      
    # deserialize and extract stats:
    body = res.json()
    
    return body["message"]

  except Exception as e:
    logging.error("downloads() failed:")
    logging.error("url: " + url)
    logging.error(e)
    return


### main ###
print('** Welcome to Gaslight, Gatekeep, Garbage Collect <3 **')
# setup base URL to web service:
# config_file = 'client_config'
config_file = 'ec2_client_config'
configur = ConfigParser()
configur.read(config_file)
baseurl = configur.get('client', 'webservice')

# take in user input
input_filename = input("Enter local file name>\n")
upload_image(baseurl, input_filename)

while True:
  try:
    pred_class = get_result(baseurl, input_filename)
    if pred_class == "recyclable" or pred_class == "not recyclable":
      print("Recyclability:", pred_class)
      break
  except:
    pass