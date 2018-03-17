import os
import re
import json
import pandas as pd
import pickle
from tweet_helpers import *

""" Module for data set preparation from turkish twitter """

cache_dir = os.path.join(os.getcwd(), 'cache')


def dir_content_list(path):
    content = os.listdir(path)
    dir_content = []
    for file in content:
        dir_content.append(file)
    return dir_content


def find_json(file):
    """
        Finds *.json file in folder content
        :param folder: A folder data directory
    """
    json_file = {"file": [], "swear": []}
    if len(re.findall(r"(?<=/)*(?=.json)", file)) > 0:
        json_file["file"].append(os.path.join(cache_dir, file))
        swear = file.split('/')[9:-1]
        json_file["swear"].extend(swear)

    return json_file


def get_dict_keys(dictionary):
    keys = []
    for key in dictionary:
        keys.append(key)
    return keys


def parse_json(json_meta):

    jsons = json_meta["file_path"]

    # List of dictionaries
    raw_tweets = []
    for i, file in enumerate(jsons):
        with open(file, 'r') as f:
            for line in f.readlines():
                print("Reading files in: " + json_meta["swear"][i])
                raw_tweets.append([json_meta["swear"][i], json.loads(line)])

    data = {"tweet_body": [],
            "tweet_id": [],
            "lang": [],
            "is_url": [],
            "hash-tags": [],
            "swear": []}

    for line in raw_tweets:
        # Only turkish tweets
        if line[1]["metadata"]["iso_language_code"] == 'tr':
            print("Parsing: " + line[1]["text"])
            data["tweet_body"].extend(line[1]["text"])
            data["tweet_id"].append(str(line[1]["id"]))
            data["lang"].append(line[1]["metadata"]["iso_language_code"])
            if "extended_entities" in get_dict_keys(line[1]):
                data["is_url"].extend([1 if len(line[1]["extended_entities"]["media"][0]["url"]) > 0 else 0])
            else:
                data["is_url"].extend([1 if len(line[1]["entities"]["urls"]) > 0 else 0])
            data["hash-tags"].extend([line[1]["entities"]["hashtags"] if len(line[1]["entities"]["hashtags"]) > 0 else 0])
            data["swear"].append(line[0])
        else:
            continue

    return data


def prepare_raw_data_set():
    base_json = os.path.join(cache_dir, 'json')
    folders = dir_content_list(base_json)
    json_paths = []
    for folder in folders:
        contents = dir_content_list(os.path.join(base_json, folder))
        for file in contents:
            json_paths.append(os.path.join(base_json, folder, file))

    # Only jsons and the file names as swear keys

    jsons = {"file_path": [], "swear": []}
    for path in json_paths:
        meta = find_json(path)
        jsons["file_path"].extend(meta["file"])
        jsons["swear"].extend(meta["swear"])
    return parse_json(jsons)


def write_to_excel(data):
    veri = pd.DataFrame({'text': data["tweet_body"], 'id': data["tweet_id"], "key": data["swear"]})
    veri.to_csv(os.path.join(cache_dir, 'to_label.xlsx'), sep='\t', index=False)


if __name__ == '__main__':
    data = prepare_raw_data_set()
    file_path = os.path.join(cache_dir, 'data.pickle')
    with open(file_path, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    write_to_excel(data)
