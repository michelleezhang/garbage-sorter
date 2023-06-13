//
// app.get('/download/:assetid', async (req, res) => {...});
const { GetObjectCommand, HeadObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');

exports.get_download = async (req, res) => {
  console.log("call to /download...");

  // define asynchronous function to check if file exists
  async function checkFileExists(bucketName, fileName) {
  try {
    const command = new HeadObjectCommand({
      Bucket: bucketName,
      Key: fileName
    });
    
    // Use await to asynchronously wait for the send() operation to complete
    await s3.send(command);
    // file found!
    return true;
  } catch (error) {
    if (error.name === 'NotFound') {
      console.log(`File '${fileName}' does not exist in bucket`);
      return false;
    }
     res.status(400).json({
      "message": "Error searching for file",
    });
    return;
  }};

 
  // define async function to delete object
   async function deleteObject(bucketName, fileName) {
    try {
      const delObject = async () => { 
        const command = new DeleteObjectCommand({
          Bucket: bucketName,
          Key: fileName
        });
        try {
          const response = await s3.send(command);
          console.log("deleted");
          return;
        } catch (err) {
          res.status(200).json({
            "message": "Error deleting object",
          });
          return;
        }
      };
      delObject();
    } catch (err) {
      res.status(200).json({
        "message": "Error deleting object",
      });
      return;
    }}


  // main function loop
  try {
    // extract image name
    var image_name = req.params.imageid;

    // see if object was classified as recyclable
    const rec_file = image_name + "_recyclable.jpeg";
    result = await checkFileExists(s3_bucket_name, rec_file)
      .catch(error => {
        console.error('Error occurred:', error);
      });

    if (result == true) {
      // RECYCLABLE
      // if image has been classified, delete it
      deleteObject(s3_bucket_name, rec_file)

       // send result to client
      res.json({
        "message": "recyclable"
      });
      return;
    } else {
      // see if object was classified as not recyclable
      const notrec_file = image_name + "_notrecyclable.jpeg";
      
      new_result = await checkFileExists(s3_bucket_name, notrec_file)
      .catch(error => {
        console.error('Error occurred:', error);
      });
      
      if (new_result == true) {
        // NOT RECYCLABLE

        // if image has been classified, delete it
        deleteObject(s3_bucket_name, notrec_file)

        // send result to client
        res.json({
          "message": "not recyclable"
        });
        return;
      }
      else {
        res.json({
          "message": ""
        })
        return;
      };
    }
  } 
  catch (err) {
    res.status(400).json({
      "message": err.message
    })
  }
}