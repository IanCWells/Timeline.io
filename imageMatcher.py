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

                NOTE: If the image and filename are not a likely match, leave the image unmatched and denoted with -1
                      It is very important to have images matchup properly to the fact provided.  If you are unsure, denote the image number as -1

                Facts are initially in JSON, ordered, chronological format.
                The image information is denoted by an ongoing list where a description and filename are detailed following a numbered image. 

                The response should be a JSON object in the following format:
                JSON and JSON ONLY!
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


if __name__ == "__main__":
    file_path = "en.wikipedia.org_detail.json"
    artist_name = "The Beatles"
    
    # json_result_as_string = asyncio.run(d.fact_producer(artist_name, "10"))
    # images_file_path = "facts.txt"
    # with open(images_file_path, 'w') as file:  
    #     file.write(json_result_as_string)

    # images = asyncio.run(query_prep(file_path))
    # facts_file_path = "images.txt"
    # with open(facts_file_path, 'w') as file:
    #     file.write(images)

    file_path = "facts.txt"
    json_result_as_string = ""
    with open(file_path, 'r') as file:
        json_result_as_string = file.read()

    file_path = "images.txt"
    images = ""
    with open(file_path, 'r') as file:
        images = file.read()

    matching =  asyncio.run(imageMatcher(json_result_as_string, images))
    matches_file_path = "matches.txt"
    with open(matches_file_path, 'w') as file:
        file.write(matching)
