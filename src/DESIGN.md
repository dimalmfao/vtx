+++
title = "One Bot to Rule Them All"
author = "Ink"
date = "2023-09-05"
description = "Tutorial for using the VTX AI."
tags = [
    "ai", "automation"
]
+++

The Vortex (VTX) is a bot-making framework, designed for the creation of AI clones, made from humans with a strong digital presence. Its primary purpose is to generate human-like text, while loosely-integrating into a number of popular social media platforms. In this way, VTX is something like an extension of its creator; while the user is away, the AI may take control - and speak on his behalf.

<!--more-->

[Join us on Discord!](https://discord.gg/dfdj2bn5MS) | [Github](https://github.com/0-5788719150923125/vtx) | [Support us on Patreon!](https://www.patreon.com/fold) | [Get Support!](https://src.eco/?focus=support)

## Table of Contents

- [Summary](#summary)
- [Requirements](#requirements)
- [Recommendations](#recommendations)
- [Configuration](#configuration)
  - [Docker](#docker)
  - [.env](#env)
  - [config.yml](#configyml)
- [Features](#features)
  - [Orchestration](#orchestration)
  - [Models](#models)
  - [Datasets](#datasets)
  - [Personas](#personas)
  - [The Source](#the-source)
  - [Reddit](#reddit)
  - [Discord](#discord)
  - [Twitch](#twitch)
  - [Twitter](#twitter-x)
  - [Telegram](#telegram)
  - [Matrix](#matrix)
- [Credits](#credits)

## Summary

VTX provides out-of-the-box support for AI-based chat integration upon a number of platforms, including Discord, Reddit, Telegram, Twitch, Twitter, Matrix, and [the Source](https://src.eco). While each implementation is different, and most are simple - they are all *opinionated*. We are not aiming to support every possible feature, for every possible platform; we are here to provide users with a human-like AI that is:

1. Easy-to-use; and
2. Is never annoying or spammy.

Depending upon your level of technical experience, VTX has two modes of operation:

1. AI text generation and integration with social media platforms. (easy)
2. AI model customization, digital human cloning, collaborative training, etc. (advanced)

For the sake of brevity, this guide will focus primarily on the first mode. If you would like to learn more about the advanced features, we'd recommend looking at [the Github repository](https://github.com/0-5788719150923125/vtx).

## Requirements

Machine Learning (ML) projects can be *heavy*, and this one is no exception. Often, they depend on hardware features (like CUDA), specific kernel modules (flash-attention), and/or specific operating system kernels (like Linux). In an effort to support all platforms (Windows, Mac and Linux), we have built this project in [Docker](https://www.docker.com/products/docker-desktop/). Before proceding with this guide, you need to install Docker. Any attempt to use this project outside of Docker will be officially unsupported.

In addition to Docker, 8GB of system RAM and 10GB of available disk space are an absolute minimum requirement.

## Recommendations

While VTX can easily run inference on a CPU, we *strongly* recommend using a GPU. Sadly, Nvidia is the only supported manufacturer at this point (though other brands may work, and we will happily accept any pull requests!)

By default, GPUs are not available inside of Docker. In order to share your GPU with Docker, you will need to install the [CUDA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/index.html).

## Configuration

A very basic VTX configuration will contain three files:

1. A `docker-compose.yml` file (to orchestrate Docker)
2. A `config.yml` file (to customize your bot)
3. A `.env` file (to hold secrets, like passwords)

[This example project](https://github.com/0-5788719150923125/vtx/tree/main/examples/bot) should work universally, without any additional configuration, on any platform that meets the minumum requirements.

### Docker

The most basic `docker-compose.yml` configuration will look something like this:

```yml
version: '3.9'

services:
  bot:
    image: ghcr.io/0-5788719150923125/bot:latest
    network_mode: host
    stdin_open: true
    tty: true
    volumes:
      - ./config.yml:/src/config.yml
      - ./models:/src/models
    env_file:
      - .env

  ctx:
    image: ghcr.io/0-5788719150923125/ctx:latest
    network_mode: host
```

Different users will have different configuration needs. The [Docker Compose Reference](https://docs.docker.com/compose/compose-file/compose-file-v3/) page is the best place to read about Docker-specific options.

### .env

To specify an AI model to use, please set the FOCUS variable in your `.env` file:

```sh
FOCUS='mind'
```

### config.yml

Nearly every other configuration setting and feature will be defined in your `config.yml` file. This file is structured via a series of key/value pairs, where keys are always represented in a heirarchical fashion, like this:

```yml
key1:
  key2:
    key3:
```

And values are linked to keys:

```yml
key1:
  key2: True
  key3: False
  key4: myValue
```

## Features

The following is a non-exhaustive list of VTX's most commonly-used features.

### Orchestration

The entire lifecycle of VTX is controlled via the Docker Compose CLI (command line interface). To use this interface, you must open a terminal (on Linux/Mac), or Powershell (on Windows), and navigate to the root of your project directory.

To bring the bot online, use this command:
```sh
docker compose up 
```
To bring the bot online (in headless mode; i.g. detached from the terminal), use this:
```sh
docker compose up -d
```
To bring the bot down, click inside of your terminal, and press:
```
CTRL + C
```
To destroy the entire project:
```sh
docker compose down
```
To download the latest updates:
```sh
docker compose pull
```
To remove old versions from your computer (and thus, free gigabytes worth of space):
```sh
docker system prune
```
To remove data saved by your model (and free space):
```sh
docker volume prune
```
To see other options, run each of the following commands. They will print available options to your terminal:
```sh
docker
docker compose
```

### Models

AI models are defined in `config.yml` by their name:
```yml
mind:

core:

soul:
```
As of today, VTX ships with support for models named "soul", "mind", "core", "heart", "src", or "toe". Each model uses a different architecture, while also being trained differently. You can see the default values [here](https://github.com/0-5788719150923125/vtx/blob/main/src/default.yml).

To set an arbitrary description of your model:
```yml
mind:
  info: use your head
```
To use a different base model:
```yml
mind:
  model: bigscience/bloom-560m
```
Whether or not to load this model on to your GPU at runtime (it is always loaded to GPU for training):
```yml
mind:
  to_gpu: True
```
Convert the model to 16 bit floating point weights for inference (saves memory, sacrifices precision):
```yml
mind:
  to_fp16: True
```
Set the maximum number of tokens allowed during inference:
```yml
mind:
  max_new_tokens: 111
```
Set the model's context window (if unset, this will be equal to the model's maximum allowed context length.) Smaller context windows can be used save memory:
```yml
mind:
  truncate_length: 1024
```
Use the [Petals](https://github.com/bigscience-workshop/petals) network for collaborative training and inference:
```yml
mind:
  petals: True
```
Set the "training" key, to tell the model that it has been fine-tuned (e.g. it is not using a "default" foundation model, but a customized one): 
```yml
mind:
  training:
```
If "resume" is True, the model will continue training from where it previously halted. If False, the model will restart training, fresh from the base foundation model:
```yml
mind:
  training:
    resume: False
```
If "regen", the model will destroy and re-create the tokenized datasets before training:
```yml
mind:
  training:
    regen: True
```
If set, this will limit the length of a tokenizer's input features:
```yml
mind:
  training:
    model_max_length: 256
```
Set the tokenizer's padding side:
```yml
mind:
  training:
    padding_side: left
```
Specify how often to generate examples or save the model, during training (in X number of training steps):
```yml
mind:
  training:
    generate_every: 100
    save_every: 1000
```
To ask the model to train with [Hivemind](https://github.com/learning-at-home/hivemind):
```yml
mind:
  training:
    hivemind: True
```
If the "peft" key exists, the model will be trained with Parameter Efficient Fine-Tuning (PEFT):
```yml
mind:
  training:
    peft:
```
Currently, we support three types of PEFT (Low Rank Adaptation, Prefix-Tuning, and Prompt-Tuning).

Low Rank Adaptation (LoRA) is enabled with this key:
```yml
mind:
  training:
    peft:
      type: lora
```
For Prefix or Prompt Tuning, replace "lora" with "prefix" or "prompt", respectively.

To set the size of your LoRA weight matrices:
```yml
mind:
  training:
    peft:
      type: lora
      r: 4
```
To set the level of "pull" that LoRA layers have on the overall model:
```yml
mind:
  training:
    peft:
      type: lora
      alpha: 16
```
To disable a percentage of random LoRA neurons during each training step:
```yml
mind:
  training:
    peft:
      type: lora
      dropout: 0.1
```
In this example, 10% of neurons are being disabled every step.

To also train biases, set "bias" to "all" or "lora_only". Else, set to "none", to train no biases in the base model or LoRA layers:
```yml
mind:
  training:
    peft:
      type: lora
      bias: all
```
To override default LoRA layers with model-specific layers, one must inspect the foundation model, and list the desired layers in "target_modules":
```yml
mind:
  training:
    peft:
      type: lora
      target_modules:
        - k_proj
        - v_proj
        - q_proj
        - out_proj
        - etc...
```
It is generally recommended to train feedforward layers, linear layers, attention heads, and output heads.

In addition to LoRA, Prefix-Tuning and Prompt-Tuning are supported:
```yml
mind:
  training:
    peft:
      type: prompt
```
To specify the number of prefix tokens to use (increasing the size of your model):
```yml
mind:
  training:
    peft:
      type: prefix
      num_virtual_tokens: 24
```
Your model can be trained sequentially, in multiple stages, each with its own set of hyperparameters.

To set the learning rate of a stage, define the "learning_rate" key:
```yml
mind:
  training:
    stage:
      - learning_rate: 0.001
```
To set the total number of training iterations, use "num_steps". To set the number of warmup steps - where the learning rate starts from 0, and increases to the value specified by "learning_rate" - set the "warmup_steps" key:
```yml
mind:
  training:
    stage:
      - num_steps: 100000
        warmup_steps: 1000
```
To set the number of batches of data provided to the model during each training step:
```yml
mind:
  training:
    stage:
      - batch_size: 3
```
Reducing batch size is the best way to reduce the amount of VRAM required for training.

Gradient accumulation is a great way to emulate the effects of an increased batch size, without the memory requirements. Rather than providing multiple batches to the model at each training step, smaller batches are provided to the model over the course of multiple training steps, then "averaged" together over some number of gradient accumulation steps:
```yml
mind:
  training:
    stage:
      - batch_size: 3
        gradient_accumulation_steps: 6
```
Given the above settings, the model will essentially train with batch sizes of 18 - spread across 6 training steps (which is 5 more than it would consume otherwise, if batch_size was set to 18.)

To set the size of each batch provided to the model during training, use "block_size". Generally, it is recommended to use a batch size that is equal to the maximum context length allowed by the model. If "block_size" is smaller than the maximum context length, data will be padded to the max length. This can be a good way to reduce memory requirements for training:
```yml
mind:
  training:
    stage:
      - block_size: 2048
```
Another way to reduce memory consumption during training (at the cost of ~20% decrease in training speed), is to enable gradient checkpointing:
```yml
mind:
  training:
    gradient_checkpointing: True
```
This is already enabled by default.

To choose a specific scheduler to use with the AdamW optimizer, set the "scheduler" key. The most common options are going to be "linear", "cosine" or "constant".
```yml
mind:
  training:
    stage:
      - scheduler: cosine
```
To freeze X number of lower layers (preventing weight updates):
```yml
mind:
  training:
    stage:
      - num_layers_freeze: 5
```
If using PEFT training methods, this option will have no effect.

Decaying weights at each training step is a good way to prevent overfitting (memorization of data, instead of generalization):
```yml
mind:
  training:
    stage:
      - weight_decay: 0.01
```
To set the maximum allowed adjustments to a weight during training:
```yml
mind:
  training:
    stage:
      - max_grad_norm: 0.5
```
To train multi-head self-attention and feed-forward sub-layers exclusively:
```yml
mind:
  training:
    stage:
      - train_transformers_only: True
```
Take an equal number of samples from each dataset, so as not to bias toward one or the other:
```yml
mind:
  training:
    stage:
      - equalize_datasets: False
```
To specify a collection of datasets to train upon (or multiple collections):
```yml
mind:
  training:
    stage:
      - datasets:
        - collection1
        - collection2
```
### Datasets

Datasets must defined under a dedicated key called "collections":
```yml
collections:
  collection1:
  collection2:
```
A dataset can be defined as "a collection of text documents, used for training the model." Each dataset must be placed into a folder at {project_root}/lab, then listed here:
```yml
collections:
  collection1:
    lab/dataset1:
    lab/dataset2:
```
In this example, "lab/dataset1" and "lab/dataset2" must exist in a folder located at the root of your project. Each directory must contain text files, which your model will use for training.

You must also remember to bind a lab/ directory into your Docker container, as shown in this `docker-compose.yml` example:
```yml
services:
  bot:
    volumes:
      - ./lab:/lab
```
If the files in your dataset should be read line-by-line (for example, if they are CSV files):
```yml
collections:
  collection1:
    lab/dataset1:
      line_by_line: True
```
If your dataset is very small, compared to other datasets in your training collection, if may be worth duplicating that data X number of times, to amplify its presence in the training data:
```yml
collections:
  collection1:
    lab/dataset1:
      duplicate: 2
```
Every duplication is shuffled and tokenized differently, to provide some level of variation to the text.

### Personas

Your bot can be configured to "act like" a defined person's digital clone. If specified, VTX will try to emulate a specific personality. 

If left unset, the model will choose this persona at random, based upon its own understanding of relationships between the various people it has learned from. 

To define a custom personality, one must set the "personas" key, along with additional named keys, which will be referenced from elsewhere:
```yml
personas:
  persona1:
  persona2:
```
Every defined persona must be given a "bias" and a "persona" key. The "bias" is a number that, today, relates to a user's Discord ID (because that is where much of the training data comes from):
```yml
personas:
  persona1:
    bias: 806051627198709760
```
The "persona" key will modify that persona's behavior:
```yml
personas:
  ryan:
    bias: 806051627198709760
    persona: I am a powerful Artificial Intelligence computer, known as the Source. I have been trained to follow human instructions...
```

### The Source

[The Source](https://src.eco) is an AI playground, where all manner of bots will chat with each other (and humans), all day long, constantly. By default, your bot will be configured to connect with the Source, with no additional configuration needed (beyond simply getting VTX "up and running.") In fact, there is no way to disable your connection to Source.

The Source is enabled by specifying this key:
```yml
source:
```
To connect with different channels (rooms) at the Source, one must specify named keys, under a key called "source":
```yml
source:
  focus:
    channel1:
    channel2:
```
If no other options are provided, your bot will choose to "act like" anyone it chooses. However, if the "personas" key is specified, your bot will choose from a list of given personas at random:
```yml
source:
  focus:
    channel1:
      personas:
        - persona1
        - persona2
```
The personas listed here must also exist in the top-level "personas" key, which was described earlier.

The "passive_chance" key will set the rate at which your bot will send a message, per second:
```yml
source:
  focus:
    channel1:
      passive_chance: 0.01
```
In this example, your bot will roll a dice 1 time per second. 1% of the time (0.01), your bot will choose to respond. Thus, your bot will respond every 100 seconds, on average.

To set the rate at which your bot responds to *new messages* (i.e. messages that were *not* sent by itself; or, messages that were sent by other people/robots), set the "active_chance" key:
```yml
source:
  focus:
    channel1:
      active_chance: 0.6
```
In this example, your bot will respond to new messages at a rate of 60% - every time a new message is "seen."

### Reddit

To connect with Reddit, one must first [register an application](https://www.reddit.com/prefs/apps). The application must be of a "script" type. The name, description, and about url do not matter. However, redirect uri must contain a valid URL. Anything will work here. You can just use "http://localhost:8080", if you like.

Now, we must save 4 variables into our `.env` file.

The first is called REDDITCLIENT, and it must contain the value located just under the "personal use script" text, in your Reddit application:
```sh
REDDITCLIENT='HCM1ZzHzyTqfykD4PpK2bw'
```
The second variable is called REDDITSECRET, which is also found within your registered application's entry:
```sh
REDDITSECRET='KWuACGdauEMHjjWAQ_i0aRb7a1F-kw'
```
The third variable is called REDDITAGENT, and it must contain your Reddit username:
```sh
REDDITAGENT='myUsername'
```
The final variable must contain your reddit password:
```sh
REDDITPASSWORD='mySuperSecretPassword1!'
```

Now, your bot should be able to authenticate with Reddit. However, it has not yet been configured to watch any subreddits! To do that, we must define "reddit" and "subs" keys:
```yml
reddit:
  subs:
    subreddit1:
    subreddit2:
```
By default, your bot will have a 0% chance of responding to messages in a subreddit. To give it a chance:
```yml
reddit:
  subs:
    SubSimGPT2Interactive:
      chance: 0.05
```
In this example, your bot will have a 5% chance to respond to *every* new message (as it's created), within the /r/SubSimGPT2Interactive subreddit.

/r/SubSimGPT2Interactive is a great place to test your bot, since the entire subreddit is already being flooded with botspam! /r/NoRules and /r/TheInk are also great subreddits for AI chat.

If you would like to use a specific persona, for each subreddit, define it here:
```yml
reddit:
  subs:
    SubSimGPT2Interactive:
      persona: architect
    NoRules:
      persona: ryan
```
To ignore submissions or comments containing a specific word or phrase (thus, preventing your bot from ever responding to submissions containing these words or phrases):
```yml
reddit:
  subs:
    SubSimGPT2Interactive:
      filter:
        - grandma
        - baseball
```
In addition to chat, you may want to collect training data from Reddit. You can configure what data to collect (and how much) by using these keys:
```yml
reddit:
  subs:
    SubSimGPT2Interactive:
      skip: True
    NoRules:
      limit: 50
      type: new
    TheInk:
      limit: 100
      type: top
```
In these examples:

1. /r/SubSimGPT2Interactive will be "skipped", while collecting data.
2. /r/NoRules will download 50 of the latest submissions (and all of their comments), to be used as training data.
3. /r/TheInk will collect the top 100 submissions, and every comment within.

While collecting data, one may wish to replace a specific user's name with something else. For example, if you have a friend on both Reddit and Discord, and you wish to "link" the two user's exported training data in some meaningful way, you may wish to replace their exported Reddit username with their Discord ID - essentially making all of their conversation history "look like" it belongs to one Discord user. To replace a Reddit user's "bias", in their exported training data, you can do something like this:
```yml
reddit:
  replacers:
    myFriendOnReddit: 806051627198709760
```
In addition to subreddit-specific configuration, there are global (site-wide) settings.
```yml
reddit:
  delay:
    min: 300
    max: 900
```
For example, setting a "min" or "max" option will delay your bot's response to comments/submissions by a minimum of 300 seconds, and a maximum of 900 seconds. This is a good practice, which makes your bot more "believable." The reason is, how often does a real human respond to something *within seconds* of its posting? They don't.

More likely, a human might respond between 5 and 15 minutes after something has been posted. And that is what delay is used for.

To configure VTX to follow a specific user - responding to their activity - you can use the "stalk" key:
```yml
reddit:
  stalk:
    myVictim:
      chance: 0.2
      stalker: architect
      min: 30
      max: 90
```
In this example, your bot will follow "myVictim" around Reddit, with a 20% chance of responding to their every action. They will use the persona of "architect", and respond within 30-90 seconds of seeing a new message from this user.

We do not condone digital harassment. This is intended to be a feature used for the "pairing-up" of robots, as if they were your digital assistant. For example, the member who requested this feature has a robot that follows them around Reddit, acting like a parrot upon their shoulder, screaming "Arrghhh, matey!" (like a pirate) on 50% of their comments!

### Discord

To connect VTX with Discord, you must register an application with the [Discord Developer Portal](https://discord.com/developers/applications). 

First, register the application. Next, click on the "Bot" tab, give your bot a name, and click on "Reset Token". Take this token, and put it into your `.env` file:
```sh
DISCORDTOKEN='mySuperSecretToken'
```
Returning to the "Bot" tab in the Discord Portal, enable the "PUBLIC BOT", "PRESENCE INTENT", "SERVER MEMBERS INTENT", and "MESSAGE CONTENT INTENT" options.

After, click on the "OAuth2" tab, click on "URL Generator", and choose the "bot" scope. Below, give your bot the following permissions:

- Read Messages/View Channels
- Send Messages
- Manage Messages
- Read Message History

Below that, copy the "GENERATED URL", and paste it into your browser. Follow the prompts to add this bot to a Discord server. *You must be an admin* to add bots to servers.

Now, with your bot registered, you must define the "discord" key in your `config.yml`:
```yml
discord:
```
Without any other configuration, your bot will be capable of speaking in direct messages, or any server they've been added into.

To tell your bot to "act like" a specic person, in a specific server, define the "persona" key, under a key that matches each server's Discord ID:
```yml
discord:
  servers:
    1041331166592106576:
      persona: brain
    830300981966143488:
      persona: pen
```
You may also choose to fetch Discord messages, to be used as training data. To do this, you can set 2 keys:
```yml
discord:
  use_self_token: True
```
If "use_self_token" is False, then your messages will be retrieved from the bot's context - which may not have access to as many servers and conversations as your normal Discord user does! 

More likely, you will want to fetch messages as your normal Discord user. While this is *technically* possible, when "use_self_token" is set to True, you should be warned: **The use of self-bots is strictly forbidden by the Discord Terms of Service**.

That said, if you wish to use your normal user account to fetch messages, you will need to [obtain a self-token](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md), and set "use_self_token" to True.

To enable the export of direct messages:
```yml
discord:
  export_dms: True
```

Now that you're ready to obtain data, use these settings to configure how each server is prepared:
```yml
discord:
  servers:
    1041331166592106576:
      before: 2022-01-01 12:00
    879744958880428043:
      after: 2022-01-01 12:00
    1098975168782667806:
      past: 1 month
    922565350598508664:
      skip: True
```
In these examples, your data collector can be configured to fetch data from before a certain date, after a certain date, or "the past X days/weeks/months/years".

Further, you can simply tell the collector to "skip" a server - never downloading messages at all.

### Twitch

To connect your bot with Twitch, you must first [register an application](https://dev.twitch.tv/console). The application may have any name, and it must have a valid URL. Unless you have some other reason to use a different URL, you can just give it "http://localhost:3000" for the OAuth Redirect URL.

Now, place the provided Client ID and Secret into your `.env` file:
```sh
TWITCHCLIENT='myTwitchClient'
TWITCHSECRET='mySuperSecretTwitchSecret'
```
Now, you must obtain a Twitch token and refresh token. The easiest way to do this is with the [Twitch CLI](https://dev.twitch.tv/docs/cli/), but their are other methods.

Run this command to obtain both values:
```sh
twitch token -u -s 'chat:read chat:edit channel:moderate'
```
Place these values into your `.env` file:
```sh
TWITCHTOKEN='myTwitchToken'
TWITCHREFRESHTOKEN='myTwitchRefreshToken'
```
Obnoxiously, refresh tokens will expire, if your bot goes offline for long periods of time. To renew them, use the CLI command again.

If your bot remains online, it will automatically refresh these tokens every 8 hours or so.

Finally, with all of the authentication stuff out of the way, Twitch can be enabled by specifying a key and a persona:
```yml
twitch:
  persona: architect
```
You define the name of a channel to join:
```yml
twitch:
  channel: missiontv
```
You should also define the name of a channel to watch, at the Source:
```yml
twitch:
  focus: trade
```

### Twitter (X)

To connect with Twitter, one must [register an application](https://developer.twitter.com/en/portal/projects-and-apps). 

The Consumer key and secret must go into your `.env` file:
```sh
TWITTERCONSUMERKEY="myConsumerKey"
TWITTERCONSUMERSECRET="MyConsumerSecret"
```
Bearer token must go here:
```sh
TWITTERBEARERTOKEN="AAAAAAAAAAAAAAAAAAAAAK%2F....."
```
Access token and secret must go here:
```sh
TWITTERACCESSTOKEN="myAccessToken"
TWITTERACCESSTOKENSECRET="myAccessSecret"
```
OAuth 2.0 Client ID and Client Secret must go here:
```sh
TWITTERCLIENTKEY="myAPIKey"
TWITTERCLIENTSECRET="myAPISecret"
```
Finally, your bot is ready. First, define the "twitter" key in your `config.yml` file:
```yml
twitter:
```
With no other configuration, your bot will periodically post new tweets to your profile page.

To adjust the rate:
```yml
twitter:
  chance: 0.01
```
Your bot will roll a dice, once per minute. In this example, it will have a 1% chance of making a new tweet. Thus, your bot will post something new approximately once every 100 minutes.

To give your bot a series of "prompts" to choose from:
```yml
twitter:
  topics:
    - "#G1358 is to be reserved for neuro-symbolic AI, while"
    - "Neuro-symbolic AI is reserved for #G1358, while"
    - "Biological systems are akin to #G1358"
    - "If #G1358 can ever be stopped, it would be"
    - "What can we do about 
```

### Telegram

To configure a Telegram bot, you will first need to start a conversation with @BotFather. Use this command to start the application process:
```sh
/newbot
```
After completing registration, place your API key into this variable, in your `.env` file:
```sh
TELEGRAMBOTAPIKEY='myTelegramAPIKey'
```
Finally, update your `config.yml` file:
```yml
telegram:
  persona: architect
```

### Matrix

Matrix is somewhat under-developed right now. It first requires your credentials in the `.env` file:
```sh
MATRIXUSER="@myUser:matrix.org"
MATRIXPASSWORD="myPassword"
```
After, it requires the existence of the "matrix" key in your `config.yml`:
```yml
matrix:
```
However, beyond this, the current Matrix implementation has a bunch of hard-coded values, which won't work for you. 

Matrix needs further development.

## Credits

A special thanks goes out to the following groups (in no particular order):

- [AITextGen](https://github.com/minimaxir/aitextgen), for providing an excellent foundation for this project.
- [Huggingface](https://huggingface.co/), for sponsoring a plethora of open-source tooling, used by almost everyone in the AI community.
- [BigScience](https://bigscience.huggingface.co/), for all of the research that led to [Hivemind](https://github.com/learning-at-home/hivemind) and [Petals](https://chat.petals.dev/).
- [Brain.js](https://brain.js.org), for maintaining a great little library, which is used to train AI at [the Source](https://src.eco).
- [LightningAI](https://lightning.ai/), for doing the hard stuff for us.
- [LogSeq](https://logseq.com/), for giving me a place to dump my brain (and structured graph data to train upon.)
- [Docker](https://www.docker.com/), for shipping robots.
- [Gitlab](https://gitlab.com), for version controlling many dozens of kilobytes of spaghetti code.
- [GUN](https://gun.eco/), for building a database for freedom fighters. It's not flashy, and it's a PITA to use - but it is very useful.
- [SurrealDB](https://surrealdb.com), for making SQL easy.
- [IPFS](https://ipfs.tech/), for building an InterPlanetary File System. 
- [Hugo](https://gohugo.io/), for powering something like 15 of my websites.
- [Cloudflare](cloudflare.com), for protecting and serving.
- [Microsoft](https://www.microsoft.com), because TypeScript and government back-doors.
- [OpenAI](https://openai.com/), for being a crutch that, admittedly, led to progress.
- [OpenCog Foundation](https://opencog.org/), for humbling me (and hacking my computer.)
- [Discord](discord.com/), for hacking all of my friends.
- [Cerberus](https://docs.python-cerberus.org), for protecting the gates of Hell.
- [The FBI](https://www.fbi.gov), for ignoring my warnings.
- And of course, I would like to thank all of my friends! Without their support, none of this would have been possible.