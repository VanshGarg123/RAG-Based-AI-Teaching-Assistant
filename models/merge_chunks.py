import os
import json
import math

n = 5

for file_name in os.listdir("jsons"):
    if file_name.endswith(".json"):
        with open(os.path.join("jsons", file_name), "r", encoding="utf-8") as f:
            data = json.load(f)

            new_chunks = []
            num_chunks = len(data['chunks'])
            num_groups = math.ceil(num_chunks / n)

            for i in range(num_groups):
                start_idx = i * n
                end_idx = min((i + 1) * n, num_chunks)

                chunk_group = data['chunks'][start_idx:end_idx]

                new_chunks.append({
                    "number": data['chunks'][0]['number'],
                    "title": chunk_group[0]['title'],
                    "start": chunk_group[0]['start'],
                    "end": chunk_group[-1]['end'],
                    "text": " ".join([chunk['text'] for chunk in chunk_group])
                })

            #Save the new chunks to a new json file
            os.makedirs("merged_jsons", exist_ok=True)
            with open(os.path.join("merged_jsons", file_name), "w", encoding="utf-8") as json_file:
                json.dump({"chunks": new_chunks, "text" : data['text']}, json_file, indent=4)