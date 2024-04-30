import os
import json
import requests

def get_channel_id(api_key, identifier):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=id&id={identifier}&key={api_key}"
    
    response = requests.get(url)
    data = response.json()
    if 'items' in data and data['items']:
        channel_id = data['items'][0]['id']
        return channel_id
    else:
        return None

def generate_subscribe_link(channel_id):
    subscribe_link = f"https://www.youtube.com/channel/{channel_id}?sub_confirmation=1"
    return subscribe_link

def lambda_handler(event, context):
    api_key = os.getenv('api_key', 'AIzaSyAVZhXNtFnRkq0Dzx8WZLTd4hxRo-w98q4')
    if not api_key:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'API key not found'})
        }
    
    # Retrieve identifier from the API Gateway event
    try:
        body = json.loads(event['body'])
        identifier = body['identifier']
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Identifier not provided'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid JSON body'})
        }

    channel_id = get_channel_id(api_key, identifier)
    
    if channel_id:
        subscribe_link = generate_subscribe_link(channel_id)
        return {
            'statusCode': 200,
            'body': json.dumps({'subscribe_link': subscribe_link})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Unable to retrieve channel information'})
        }

if __name__ == '__main__':
    test_identifier = "UClhSPbp4Qube_SBBYL_kMvg"
    api_key = os.getenv('api_key', 'AIzaSyAVZhXNtFnRkq0Dzx8WZLTd4hxRo-w98q4')
    channel_id = get_channel_id(api_key, test_identifier)
    
    if channel_id:
        subscribe_link = generate_subscribe_link(channel_id)
        print(f"Subscribe link for channel ID '{channel_id}' is: {subscribe_link}")
    else:
        print(f"Unable to retrieve channel ID for identifier '{test_identifier}'")
