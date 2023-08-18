from telegraph.aio import Telegraph
import head


async def orchestrate(config):
    return

    telegraph = Telegraph()
    print(await telegraph.create_account(short_name="Ink"))

    for target in config:
        if "prompt" in config[target]:
            try:
                output = await head.gen(
                    prefix=config[target].get("prompt"),
                    max_new_tokens=1536,
                    mode="prompt",
                    decay_after_length=512,
                    decay_factor=0.00000023,
                )
                print(output)
                response = await telegraph.create_page(
                    title="A Test",
                    author_name="Ink",
                    html_content=output,
                )
                print(response["url"])
            except Exception as e:
                print(e)
