from dotenv import load_dotenv, dotenv_values
from azure.storage.blob import BlobServiceClient, ContainerClient
from PIL import Image
import time


conn_str = dotenv_values('.env').get('AZURE_STORAGE_CONNECTION_STRING')

def readContainers():
    blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)
    containers = blob_service.list_containers()
    container_list = list(containers)
    return container_list

def readBlobs(container_name):
    container_client = ContainerClient.from_connection_string(conn_str=conn_str, container_name=container_name)
    blob_list = container_client.list_blobs()
    blob_list = list(blob_list)
    return blob_list

def previewBlob(blob_name,container_name):
    blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)
    blob_client = blob_service.get_blob_client(container_name, blob_name)
    blob_data = blob_client.download_blob()
    blob_name = blob_name.split('/')[-1]
    with open(".data/{}".format(blob_name), "wb") as my_blob:
        blob_data = blob_client.download_blob()
        blob_data.readinto(my_blob)
        my_blob.close()
    img = Image.open('.data/{}'.format(blob_name))
    img.show()


containers = readContainers()
for container in containers:
    print("reading blobs of container: {}".format(container.name))
    blobs = readBlobs(container.name)
    for blob in blobs:
        print("showing blob: {}".format(blob.name))
        previewBlob(blob.name,container.name)
        time.sleep(3)