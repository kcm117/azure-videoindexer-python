'''
11/19/2018
KC Munnings, Microsoft
Video Indexer API - Example upload from Blob Storage
** FOR DEMONSTRATION PURPOSES ONLY **
'''
from azure.storage.blob import (
    ContentSettings,
    BlobBlock,
    BlockListType,
    BlockBlobService
)
import requests
import os
import io
import json


# Important stuff
storage_account_name = 'PUT YOUR STORAGE ACCOUNT NAME HERE'
storage_account_key = 'PUT YOUR STORAGE ACCOUNT KEY HERE'
storage_container_name = 'PUT YOUR STORAGE CONTAINER NAME HERE'

video_indexer_account_id = 'ACCOUNT ID' # Get this from https://www.videoindexer.ai/settings/account
video_indexer_api_key = 'KEY' # Get this from subscription at https://api-portal.videoindexer.ai/products/authorization
video_indexer_api_region = 'REGION' # Get this from https://www.videoindexer.ai/settings/account

file_name = 'NAME OF AUDIO/VIDEO BLOB IN STORAGE' # Example: myfile.wav

print('Blob Storage: Account: {}, Container: {}.'.format(storage_account_name,storage_container_name))

# Get File content from blob
block_blob_service = BlockBlobService(account_name=storage_account_name,
                                      account_key=storage_account_key)
audio_blob = block_blob_service.get_blob_to_bytes(storage_container_name,file_name)
audio_file = io.BytesIO(audio_blob.content).read()

print('Blob Storage: Blob {} loaded.'.format(file_name))

# Authorize against Video Indexer API
auth_uri = 'https://api.videoindexer.ai/auth/{}/Accounts/{}/AccessToken'.format(video_indexer_api_region,video_indexer_account_id)
auth_params = {'allowEdit':'true'}
auth_header = {'Ocp-Apim-Subscription-Key': video_indexer_api_key}
auth_token = requests.get(auth_uri,headers=auth_header,params=auth_params).text.replace('"','')

print('Video Indexer API: Authorization Complete.')
print('Video Indexer API: Uploading file: ',file_name)

# Upload Video to Video Indexer API
upload_uri = 'https://api.videoindexer.ai/{}/Accounts/{}/Videos'.format(video_indexer_api_region,video_indexer_account_id)
upload_header = {'Content-Type': 'multipart/form-data'}
upload_params = {
    'name':file_name,
    'accessToken':auth_token,
    'streamingPreset':'Default',
    'fileName':file_name,
    'description': '#CallCenterLife'}
files= {'file': (file_name, audio_file)}
r = requests.post(upload_uri,params=upload_params,files=files)
response_body = r.json()

print('Video Indexer API: Upload Completed.')
print('Video Indexer API: File Id: {} .'.format(response_body.get('id')))

# Check Status of Job
# You can sleep and loop hitting the Get Video Index API to view the status
# https://api-portal.videoindexer.ai/docs/services/operations/operations/Get-Video-Index?
