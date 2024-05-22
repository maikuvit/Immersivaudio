def recombine_prompt(description_json, object_json, for_music=True):

    description_json.update(object_json)

    if for_music:
        description_json.update(
            {
                "prompt_combiner": {
                    "prompt": "Melodic music based on "
                    + description_json["frame_description"]["description"] 
                    + ",".join(description_json["object_detection"]["total_keywords"])
                }
            }
        )
    else:
        description_json.update(
            {
                "prompt_combiner": {
                    "prompt": "Sound effects based on "
                    + description_json["frame_description"]["description"]
                    + " with the following keywords: "
                    + ",".join(description_json["object_detection"]["total_keywords"])
                }
            }
        )
