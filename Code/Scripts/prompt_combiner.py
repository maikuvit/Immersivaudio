def recombine_prompt(description_json, object_json):

    description_json.update(object_json)

    description_json.update(
        {
            "prompt_combiner": {
                "prompt": "Melodic, clear and high-quality music based on "
                + description_json["frame_description"]["description"]
                # + ",".join(description_json["object_detection"]["total_keywords"])

            }
        }
    )
    if description_json["options"]["generate_sounds"]:
        description_json["prompt_combiner"].update(
            {
                "sound_prompt": "High-quality and clear sound effects based on "
                + description_json["frame_description"]["description"]
                + " Background sounds of: " 
                + ",".join(description_json["object_detection"]["total_keywords"])
                # + " with the following keywords: "
            }
        )

    return description_json
