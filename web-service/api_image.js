//
// app.post('/image/:userid', async (req, res) => {...});
//
const { PutObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');
const uuid = require('uuid');

exports.post_image = async (req, res) => {

  console.log("call to /image...");

  try {
    // extract image name parameter from url 
    var image_name = req.params.imageid

    // we recieve an image as a base64-encoded string
    // decode our string into raw bytes
    var body = req.body;  // data => JS object
    var data = Buffer.from(body["data"], 'base64');
    
    // upload image (data) to S3
    const PutObject = async () => {
      const command = new PutObjectCommand({
        Bucket: s3_bucket_name,
        Key: image_name,
        Body: data
      });
      try {
            const response = await s3.send(command);
        res.json({
                "message": "success",
              });
              return;
      } catch (err) {
            res.status(200).json({
              "message": "Error putting object",
            });
            return;
          }
    };
    PutObject();

  }//try
  catch (err) {
    res.status(400).json({
      "message": err.message,
      "assetid": -1
    });
  }//catch

}//post