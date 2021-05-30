# downloads an image with a specified url

import requests

resp  = requests.get('https://media.timeout.com/images/105731796/1024/576/image.jpg')

with open('image.jpg', 'wb') as file2:
    file2.write(resp.content)
