import json
from openai import AsyncClient
import detailer as d
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()  # This will load the variables from .env into the environment
client = AsyncClient(api_key=os.getenv("API_KEY"))

async def query_prep(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    data_index = 0
    total_list = ""
    for current_data in data:
        data_index += 1
        query_prep = str(data_index) + ". "
        if current_data['image_alt']:
            query_prep += "Description: " + current_data['image_alt'] + " "
        if current_data['file_name']:
            query_prep += "FileName: " + current_data['file_name']
        total_list += query_prep
    return(total_list)

async def imageMatcher(facts, images):
    completion = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"""
                You are a matching assistant that is knowledgeable about music.
                You are responsible for taking a paragraph of image filenames and descriptions and matching them to the closest,
                corresponding listed fact. The goal is to match a fact with an image so that a timeline can be built with images. 
                You are using the context clues of the image alt_id and the filename to try and make an image match with a filename. 

                NOTE: If the image and filename are not a match, leave the image unmatched and denoted with -1
                      It is very important to have images matchup properly to the fact provided.  If you are unsure, denote the image number as -1

                Facts are initially in JSON, ordered, chronological format.
                The image information is denoted by an ongoing list where a description and filename are detailed following a numbered image. 

                The response should be a JSON object in the following format:
                JSON and JSON ONLY!
                IMAGE Numbers MUST NEVER BE Repeated. 
                {{
                    "fact_image_pairs": [
                        {{"Fact": "1", "Image_Number": "The image number."}},
                        {{"Fact": "2", "Image_Number": "The image number.}},
                        {{"Fact": "3", "Image_Number": "-1"}},
                        ...
                    ]
                }}
                Here is the JSON containing the facts: {facts}
                And here is the string containing the image descriptions and filenames: {images}
                Note: Some images only have filenames.  
                """
            }
        ]
    )
    result = completion.choices[0].message.content 
    return result 

async def condenserFinal(information_json, facts_string_json, to_match_as_dict):
    final_list = []
    pair_length = len(to_match_as_dict["fact_image_pairs"])
    for idx in range(0, pair_length):
        image_index = int(to_match_as_dict["fact_image_pairs"][idx]["Image_Number"])

        fact = facts_string_json["facts"][idx]
        path = ""
        if image_index != -1:
            path = (information_json[image_index - 1]["image_path"])
        pair = {
            "date": fact["date"],
            "fact": fact["fact"],
            "path": path
        }
        final_list.append(pair)

    json_output = json.dumps(final_list)
    return json_output

async def fact_imager(file_path, artist_name):    

   
    facts_string = await d.fact_producer(artist_name, "10")

    images = await query_prep(file_path)
    matching = await imageMatcher(facts_string, images)
    
    with open(file_path, 'r') as file:
        information = file.read()

    information_json = json.loads(information)
    facts_string_json = json.loads(facts_string)
    to_match_as_dict = json.loads(matching)
    return (await condenserFinal(information_json, facts_string_json, to_match_as_dict))

    # return await condenserFinal(information_json, facts_string_json, to_match_as_dict)
    # facts_string = asyncio.run(d.fact_producer(artist_name, "10"))
    # images_file_path = "facts.txt"
    # with open(images_file_path, 'w') as file:  
    #     file.write(facts_string)

    # images = asyncio.run(query_prep(file_path))
    # facts_file_path = "images.txt"
    # with open(facts_file_path, 'w') as file:
    #     file.write(images)

    # matching = asyncio.run(imageMatcher(facts_string, images))
    # matches_file_path = "matches.json"
    # with open(matches_file_path, 'w') as file:
    #     file.write(matching)
    
    # with open(file_path, 'r') as file:
    #     information = file.read()

    # information_json, facts_string_json, to_match_as_dict = json.loads(information), json.loads(facts_string), json.loads(matching)

#8 cents per query - we can reduce this for sure
if __name__ == "__main__":
    file_path = "en.wikipedia.org_detail.json"
    artist_name = "The Beatles"
    final_json = (fact_imager(file_path, artist_name))

    output_path = "output.json"
    with open(output_path, 'w') as file:
        file.write(final_json)