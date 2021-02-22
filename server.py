import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://BeLazy:BeLazy@cluster0.csr3d.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["meme"]
collection = db["server_info"]


def add_server_info(server_name, text_channels_list, roles_list):
    total_server = collection.estimated_document_count()  # gives total server in server_info collection
    if total_server == 0:  # check if database is empty
        server = {"server_name": server_name, "text_channels": text_channels_list, "roles": roles_list}
        collection.insert_one(server)  # insert server info to database
    else:
        data = collection.find_one({"server_name": server_name, "text_channels": text_channels_list})
        if str(data) == "None":
            server = {"server_name": server_name, "text_channels": text_channels_list, "roles": roles_list}
            collection.insert_one(server)
        else:
            print("server is already present")
    return


def get_server_info(server_name):  # used to return server info from database
    print(server_name)
    data = collection.find_one({"server_name": server_name})
    if str(data) == "None":
        print("Server not found")
    else:
        text_channel, roles = data['text_channels'], data['roles']
        return text_channel, roles


def update_server_info(server_name, channel_name):  # used to update channel list when someone delete channel or create channel
    print(server_name)
    print(channel_name)
    data = collection.find_one({"server_name": server_name})
    if str(data) == "None":
        print("Server not found")
    else:
        text_channels = data["text_channels"]
        print(type(text_channels))
        print(text_channels)
        if channel_name in text_channels:
            text_channels.remove(channel_name)
            print(text_channels)
            collection.update_one({"server_name": server_name}, {"$set": {"text_channels": text_channels}})
        else:
            text_channels.append(channel_name)
            print(text_channels)
            collection.update_one({"server_name":server_name},{"$set":{"text_channels":text_channels}})
