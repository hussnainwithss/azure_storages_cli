from dotenv import load_dotenv, dotenv_values
from azure.storage.blob import BlobServiceClient, ContainerClient
import inquirer
from PIL import Image


conn_str = dotenv_values('.env').get('AZURE_STORAGE_CONNECTION_STRING')


def readContainers():
    blob_service = BlobServiceClient.from_connection_string(conn_str=conn_str)
    containers = blob_service.list_containers()
    container_list = list(containers)
    container_list = [
        inquirer.List('container',
                      message="Please select a container:",
                      choices=[container.name for container in container_list],
                      ),
    ]
    
    return container_list


def readBlobs(container_name):
    container_client = ContainerClient.from_connection_string(
        conn_str=conn_str, container_name=container_name)
    blob_list = container_client.list_blobs()
    blob_list = list(blob_list)
    blob_list = [
        inquirer.List('blob',
                      message="Please select a blob:",
                      choices=[blob.name for blob in blob_list],
                      ),
    ]
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
    

def menu():
    print("------Welcome to Azure Storage CLI------")
    menu = [
        inquirer.List('choosen',
                      message="What do you wanna do:",
                      choices=['Explore containers','Exit'],
                      ),
    ]
    selected = inquirer.prompt(menu)['choosen']
    if selected == 'Exit':
        return 0
    else:
        container_list = readContainers()
        while True:
        
            container = inquirer.prompt(container_list)['container']
            blob_list = readBlobs(container)
            blob = inquirer.prompt(blob_list)['blob']
            previewBlob(blob, container)


menu()