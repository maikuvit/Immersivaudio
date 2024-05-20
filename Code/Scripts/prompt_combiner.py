
def recombine_prompt(description_json,object_json):

    description_json.update(object_json)

    description_json.update({"prompt_combiner":{
        "prompt" : "Melodic music based on " + 
        description_json["frame_description"]["description"] +
        "Considering the keywords: " + 
        ",".join(description_json["object_detection"]["total_keywords"])
    }})

    return description_json