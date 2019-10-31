# Import gcloud
from google.cloud import storage
import os
from datetime import date
os.environ["GOOGLE_API_KEYS"]="/home/pi/Downloads/rpitraffic-firebase-adminsdk-526ol-d331fc91c9.json"

DIRECTORY = "./jumpers/"
def cloud_upload():

	 
	try: 
		# Getting all the file names
		files = []
		# r=root, d=directories, f = files
		for r, d, f in os.walk(DIRECTORY):
		    for jpeg in f:
			    files.append((os.path.join(r, jpeg),jpeg))

		# Enable firebase Storage
		client = storage.Client()
		# Reference an existing bucket.
		bucket = client.get_bucket('rpitraffic.appspot.com')
		# Getting the date and creating filename according to date and time fetched
		today = date.today()
		cloud_dir = str(today.strftime("%d-%m-%Y"))+"/"
		for path,name in files:
		# Upload a local file to the Created Cloud file in your bucket. 
			Blob = bucket.blob(cloud_dir+name)
			Blob.upload_from_filename(filename=path)
			os.remove(path)
		return 1
	except:
		#For failures
		return 0

