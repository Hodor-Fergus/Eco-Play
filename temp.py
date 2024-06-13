from azure.storage.blob import BlobServiceClient
from os import remove

# Replace with your connection string and container/blob details
connection_string = "DefaultEndpointsProtocol=https;AccountName=ecoplay;AccountKey=XGjctFWz3oWSA/YzDpQfk6OztAWkeladgc7QqaXm6Rom1h+a2TRABFogUQTKgmh0UnkML5QCg42a+ASt1v4t+g==;EndpointSuffix=core.windows.net"
container_name = "files"
blob_name = "data_csv.csv"

blob_names = ["ListA.txt", "ListB.txt", "best_scores.txt", "data_csv.csv", "hints.txt"]


blob_service_client = BlobServiceClient.from_connection_string(conn_str=connection_string)
blob_name = "best_scores.txt"
blob_service = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

with open("./assets/game_data/best_scores.txt", 'rb') as data:
    blob_service.upload_blob(data, overwrite=True)