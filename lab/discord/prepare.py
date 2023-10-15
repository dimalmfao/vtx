import json
import os
import random
import re
import shutil
import sys

sys.path.append("/src")

from common import config, get_identity, ship, wall

root_dir = "/lab/discord"


# Format Discord messages for training
def main():
    # Replace links and @mentions
    def sanitizer(string):
        sanitized = re.sub(
            r"http\S+",
            "((url))",
            string,
        )
        sanitized = re.sub(
            r"@Unknown",
            "<@" + str(get_identity()) + ">",
            sanitized,
        )
        return sanitized

    # Ensure export path exists and is clean
    if os.path.exists(f"{root_dir}/train"):
        shutil.rmtree(f"{root_dir}/train")

    os.makedirs(f"{root_dir}/train")

    successes = 0
    failures = 0
    for filename in os.listdir(f"{root_dir}/source"):
        try:
            with open(os.path.join(f"{root_dir}/source", filename), "r") as file:
                data = json.load(file)

                data_dict = {obj["id"]: obj for obj in data["messages"]}

                for i in data_dict.values():
                    if i["type"] != "Default" and i["type"] != "Reply":
                        continue

                    if len(i["embeds"]) > 0:
                        if i["content"] != "":
                            i["content"] = i["content"]
                        if i["embeds"][0]["title"]:
                            i["content"] = (
                                i["content"] + " | ((" + i["embeds"][0]["title"] + "))"
                            )
                        if i["embeds"][0]["description"]:
                            i["content"] = (
                                i["content"]
                                + " | (("
                                + i["embeds"][0]["description"]
                                + "))"
                            )

                    author_id = i["author"]["id"]

                    if i["author"]["isBot"] == True:
                        author_id = transform_author(i["author"])
                        if author_id == False:
                            continue

                    with open(f"{root_dir}/train/{filename}.txt", "a") as txt_file:
                        if i["type"] == "Reply":
                            try:
                                message_ref_id = i["reference"]["messageId"]

                                result = data_dict.get(message_ref_id, None)

                                reply_author_id = result["author"]["id"]

                                if result["author"]["isBot"] == True:
                                    reply_author_id = transform_author(result["author"])

                                if reply_author_id != False:
                                    if result is not None:
                                        if len(result["embeds"]) > 0:
                                            if result["content"] != "":
                                                result["content"] = result["content"]
                                            if result["embeds"][0]["title"]:
                                                result["content"] = (
                                                    result["content"]
                                                    + " | (("
                                                    + result["embeds"][0]["title"]
                                                    + "))"
                                                )
                                            if result["embeds"][0]["description"]:
                                                result["content"] = (
                                                    result["content"]
                                                    + " | (("
                                                    + result["embeds"][0]["description"]
                                                    + "))"
                                                )
                                        sanitized = sanitizer(result["content"])
                                        if len(result["mentions"]) > 0:
                                            for mention in result["mentions"]:
                                                sanitized = sanitized.replace(
                                                    "@" + mention["nickname"],
                                                    "<@" + str(mention["id"]) + ">",
                                                )
                                        sanitized = transform_message(sanitized)
                                        content = (
                                            wall
                                            + reply_author_id
                                            + ship
                                            + " "
                                            + sanitized
                                        )
                                        txt_file.write(f"{content}\n".format(content))
                                        successes += 1
                            except Exception as e:
                                failures += 1

                        try:
                            sanitized = sanitizer(i["content"])
                            if len(i["mentions"]) > 0:
                                for mention in i["mentions"]:
                                    sanitized = sanitized.replace(
                                        "@" + mention["nickname"],
                                        "<@" + str(mention["id"]) + ">",
                                    )
                            sanitized = transform_message(sanitized)
                            content = wall + author_id + ship + " " + sanitized
                            txt_file.write(f"{content}\n".format(content))
                            successes += 1
                        except Exception as e:
                            failures += 1
        except Exception as e:
            failures += 1

        os.system("clear")
        print("preparing Discord messages")
        print(f"{successes} successes, {failures} failures")


# Replace unapproved bots with random IDs, so as not to bias the model toward poor outputs
def transform_author(author):
    if (
        str(author["id"]) == "975174695399854150"
        or str(author["id"]) == "315826602187554816"
        or str(author["id"]) == "1053270121218592798"
    ):  # Eliza, Kitsunetsuki, MAINNFRAME
        return str(author["id"])
    elif str(author["id"]) == "1055993037077106718":  # Samn
        return str(get_identity())
    elif "Ghost-" in author["name"]:
        return str(get_identity())
    else:
        return False


# Replace third person messaging from bots, so as not to bias the model towards this format
def transform_message(message):
    matchers = [
        r'(?:The ghost of )(?:<@\d*>)(?: suggests, \*")(.*)(?:"\*$)',
        r'(?:<@\d*>)(?: says, \*")(.*)(?:"\*$)',
        r'(?:<@\d*>)(?: would say, \*")(.*)(?:"\*$)',
        r'(?:They said, \*")(.*)(?:"\*$)',
    ]
    for pattern in matchers:
        matcher = re.compile(pattern)
        if matcher.match(message):
            group = re.search(matcher, message)
            message = group[1]
            break
    return message


if __name__ == "__main__":
    main()