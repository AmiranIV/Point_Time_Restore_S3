Python script to perform a point-in-time restore for an object stored in a version-enabled S3 bucket.

#mybucket: This is the name of the S3 bucket that contains the object to be restored.
#myobject: This is the key (or filename) of the object that needs to be restored.
#2023-05-01T13:45:00.000Z: This is the timestamp representing the point in time to which the object should be restored.

Example of execution : 
python point_in_time_restore.py mybucket myobject 2023-05-01T13:45:00.000Z

#Don't forget to preform aws configure
#Requirements : boto3, sys, time

This script provides a convenient way to perform a point-in-time restore of an object in an S3 bucket, allowing you to revert to a previous version based on a specified timestamp.
