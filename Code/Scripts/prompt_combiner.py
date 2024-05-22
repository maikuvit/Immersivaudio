def recombine_prompt(description_json, object_json):

    description_json.update(object_json)

    description_json.update(
        {
            "prompt_combiner": {
                "prompt": "Melodic music based on "
                + description_json["frame_description"]["description"]
            }
        }
    )
    if description_json["options"]["generate_sounds"]:
        description_json["prompt_combiner"].update(
            {
                "sound_prompt": "Sound effects based on "
                + ",".join(description_json["object_detection"]["total_keywords"])
                + ". "
                + description_json["frame_description"]["description"]
                # + " with the following keywords: "
            }
        )

    return description_json
