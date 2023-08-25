import functools
import asyncio
import random
import typing
import time
import os
import re
import gc
import torch
from aitextgen import aitextgen
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from transformers import AutoTokenizer, GenerationConfig, AutoModelForCausalLM, PretrainedConfig
from peft import PeftModel, PeftConfig
from utils import (
    ad,
    bc,
    config,
    nist_beacon,
    propulsion,
    ship,
    write_log_file,
)

focus = os.environ["FOCUS"]

# when all fails, reset to this context
default_context = [
    propulsion + "975174695399854150" + ship + " I am a robot.",
    propulsion + "1051994502333726841" + ship + " I am a ghost.",
    propulsion + "806051627198709760" + ship + " I am a human.",
    propulsion + "204716337971331072" + ship + " I am a medium.",
    propulsion + "855529761185857566" + ship + " I am an animal.",
]

context = default_context.copy()


# Decorator to a blocking function into a background thread
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


# Load the specified model
active = False
def loader(target=None):
    global active
    global focus

    while active == True:
        time.sleep(1)

    active = True
    try:
        global ai
        ai = None
        torch.cuda.empty_cache()
        gc.collect()
    except Exception as e:
        print(e)

    if target == None:
        target = focus

    model = config[target]

    model_folder = None
    if "training" in model:
        model_folder = "models/" + target
        if "peft" in model["training"]:
            model_folder = None

    base = model.get("model", None)

    try:
        print(bc.FOLD + "ONE@FOLD: " + ad.TEXT + "focused on the " + target)
        logging.getLogger("transformers").setLevel(logging.ERROR)
        ai = aitextgen(
            model=model.get("model", None),
            model_folder=model_folder,
            petals=model.get("petals", False),
            to_gpu=model["to_gpu"],
            cache_dir="models",
        )
        # ai.tokenizer = AutoTokenizer.from_pretrained(
        #     model.get("tokenizer", base),
        #     cache_dir="models",
        #     padding_side="left",
        # )
        if "training" in model:
            if "peft" in model["training"]:
                ai.model = PeftModel.from_pretrained(ai.model, "adapters/" + target)
        logging.getLogger("transformers").setLevel(logging.INFO)
        print(bc.FOLD + "ONE@FOLD: " + ad.TEXT + model["info"])
        print(bc.ROOT + "ONE@ROOT: " + ad.TEXT + str(ai))
    except Exception as e:
        print(e)
        ai = None
        torch.cuda.empty_cache()
        gc.collect()
        time.sleep(30)
        ai = loader(target)
    active = False
    return ai

# Load the model and schedule periodic reloading
ai = loader()
scheduler = BackgroundScheduler()
scheduler.add_job(loader, trigger="interval", minutes=30)
scheduler.start()

# Build a local cache of global conversational state
def build_context(message):
    while len(context) >= 23:
        context.pop(0)

    context.append(message)


# Build a local cache of global conversational state
def replace(old_message, new_message):
    try:
        matcher = re.compile(r'(\*")(.*)(?:"\*$)')
        group = re.search(matcher, old_message)
        captured = "J U X T A P O S I T I O N"[::-1]
        if group is not None and group[2]:
            captured = group[2]
        for item in context:
            if captured in item or old_message in item:
                index = context.index(item)
                context[index] = new_message
                return

        build_context(new_message)

    except Exception as e:
        print(e)


# Truncate the prompt to fit the model
def truncate_context(ctx, max_length=512):
    context_length = sum([len(item) for item in ctx])

    if context_length > max_length:
        for i, line in enumerate(ctx):
            if not line.startswith(propulsion):
                continue
            remaining = i + 1
            ctx[i] = line[:remaining]
            if sum([len(item) for item in ctx]) <= max_length:
                break

    return ctx


# Generate a completion from bias and context
@to_thread
def gen(
    prefix=None,
    ctx=None,
    bias=None,
    max_new_tokens: int = config[focus].get("max_new_tokens", 111),
    decay_after_length: int = 23,
    decay_factor: float = 0.000023,
    mode: str = "chat",
):
    global ai
    global active

    while active == True:
        time.sleep(1)

    active = True

    if not prefix:
        prefix = config[focus].get("prefix", "Humans, AI, and daemons have a conversation together:")

    # bias the prompt
    prompt = prefix
    eos = False
    if mode == "chat":
        prompt = propulsion

        eos = ai.tokenizer.convert_tokens_to_ids(ai.tokenizer.tokenize(propulsion)[0])

        if ctx == None:
            global context
            ctx = context

        ctx = truncate_context(ctx, config[focus].get("context_length", 1024))
        history = prefix + "\n" + "\n".join(ctx) + "\n"

        if bias is not None:
            if (len(str(bias)) == 18) or (len(str(bias)) == 19):
                prompt = propulsion + str(bias) + ship
        prompt = history + prompt

    seed = nist_beacon()

    petals = config[focus].get("petals", False)

    attempt = 1
    max_attempts = 9
    while attempt <= max_attempts:
        try:
            output = None

            temperature = 0.9
            if attempt > 0:
                decay_factor = decay_factor / 2
                temperature = temperature / 2

            # https://huggingface.co/docs/transformers/main_classes/text_generation
            generation_config = GenerationConfig(
                    n=1,
                    do_sample=True,
                    min_length=23,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    eta_cutoff=0.0003,
                    penalty_alpha=0.6,
                    top_k=4,
                    repetition_penalty=1.95,
                    encoder_repetition_penalty=1.00023,
                    exponential_decay_length_penalty=(decay_after_length, decay_factor),
                    no_repeat_ngram_size=4,
                    renormalize_logits=True,
                    remove_invalid_values=True,
                    eos_token_id=eos,
                    max_time=360,
                    seed=seed[1],
                )

            logging.getLogger("transformers").setLevel(logging.ERROR)
            completion = ai.generate(
                prompt=prompt,
                generation_config=generation_config,
                # max_length=111,
                max_length=2048,
                return_as_list=True,
            )
            logging.getLogger("transformers").setLevel(logging.WARNING)

            if petals:
                print(bc.ROOT + "ONE@PETALS: " + ad.TEXT + completion[0])

            active = False

            if mode == "prompt":
                output = completion[0]
                write_log_file(dir="/gen/generations", content=output)
                break

            generation = completion[0][len(history) :]
            mentions = "(?:[<][@])(\d+\s*\d*)"
            variables = "(?:\({3})(\d+\s*\d*)(?:\){3})"
            group = re.search(r"^(¶{1})(\d{2,23})(?::\s?>\s*)(.*)", generation)
            if (
                group is None
                or propulsion in group[3]
                or bool(re.search(mentions, group[3]))
                or bool(re.search(variables, group[3]))
                or group[3].startswith(">")
                or group[3].startswith("~")
                or group[3].startswith('"')
                or group[3].startswith(" ")
            ):
                raise Exception("failed to format a proper response")
            else:
                output = [group[2], group[3], seed[0], ctx]
                break

        except Exception as e:
            attempt += 1
            if petals:
                print(e)
            if attempt > max_attempts:
                context = default_context.copy()
                output = [False, ctx]

    active = False
    return output