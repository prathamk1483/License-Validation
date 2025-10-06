import random

chars = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'

def generateString(num):
    return [random.choice(chars) for _ in range(num)]

def createId(typeOfId):
    additionalString = ""
    uuid = []
    uuid_str = ""
    if typeOfId == "App":
        uuid = generateString(29)
        uuid_str = ''.join(uuid)
        additionalString = "app"
    
    elif typeOfId == "License":
        uuid = generateString(57)
        uuid_str = ''.join(uuid)
        additionalString = "license"

    elif typeOfId == "Business":
        uuid = generateString(24)
        uuid_str = ''.join(uuid)
        additionalString = "business"
    
    elif typeOfId == "Owner":
        uuid = generateString(11)
        uuid_str = ''.join(uuid)
        additionalString = "owner"

    return uuid_str + additionalString

