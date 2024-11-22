import os
from dotenv import load_dotenv
from openai import AsyncClient
import asyncio
import json

# Load environment variables from .env file
load_dotenv()  # This will load the variables from .env into the environment
client = AsyncClient(api_key=os.getenv("API_KEY"))

async def fact_producer(artist: str, num_facts: str):
    completion = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"""
                You are a helpful assistant that is knowledgeable about music.
                "Write {num_facts} very short (less than one sentence) bullet points outlining the history of the following musical artist or group.  
                These facts should be listed in chronological order.
                These facts should be the most IMPORTANT information related to the artist.  
                Each bullet point should have an associate date or date range.  
                
                The artist/group: {artist}
                The response should be a JSON object in the following format:
                {{
                    "artist": "{artist}",
                    "facts": [
                        {{"date": "YYYY", "fact": "Fact 1"}},
                        {{"date": "YYYY", "fact": "Fact 2"}},
                        ...
                    ]
                }}
                """
            }
        ]
    )
    result = completion.choices[0].message.content  
    return result
    # try:
    #     result_as_json = json.loads(result)
    #     return result_as_json
    # except json.JSONDecodeError as e:
    #     return "JSONDecodeError" 
        
if __name__ == "__main__":
    artist_name = "The Beatles"
    json_result = asyncio.run(fact_producer(artist_name, "10"))
    print(json_result)