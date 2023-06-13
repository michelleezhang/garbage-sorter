// node js web service that interacts with AWS S3

const express = require('express');
const app = express();
const config = require('./config.js');
const { HeadBucketCommand, ListObjectsV2Command } = require('@aws-sdk/client-s3');
const { s3, s3_bucket_name, s3_region_name } = require('./aws.js');
// enable JSON deserialization of incoming JSON data 
app.use(express.json({strict: false, limit: "50mb"}));
var startTime;
app.listen(config.service_port, () => {
  startTime = Date.now();
  console.log('web service running...');
  // Configure AWS to use our config file:
  process.env.AWS_SHARED_CREDENTIALS_FILE = config.gc_config;
});

app.get('/', (req, res) => {
  var uptime = Math.round((Date.now() - startTime) / 1000);
  res.json({
    "status": "running",
    "uptime-in-secs": uptime
  });
});


// FUNCTIONS
var download = require('./api_download.js');
var image = require('./api_image.js');

app.get('/download/:imageid', download.get_download); 
app.post('/image/:imageid', image.post_image);
