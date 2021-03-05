# Anonymous Inbox Bot

This bot manages an anonymous inbox for your students, so they can do
anonymised suggestions about the course of your teaching, and what can
you do to improve it. It also supports identifiable suggestions, and
the type of suggestion is decided by the student at the moment of
sending the message.

# Basic functionality

The functionality of the bot is pretty simple. Using the `/start`
command triggers the welcome message of the bot. It welcomes the
students and tells them how to perform new suggestions.

The main function of the bot is built around the `/suggest` command.
Using this command, the student can send a new message. After using
the command, the bot asks you about the nature the suggestion
(anonymous or identifiable), showing a button keyboard. After pressing
one of the buttons, the bot asks for the message to be sent. When the
message has been sent, the bot thanks the student for the suggestion,
and sends the message to the teacher, indicating the name and alias
of the student if it has decided to send an identifiable suggestion.

# Requirements

The bot has been developed using Python 3.8. It should work
independently of the Python version, as long as it is Python 3. The
requirements for the project are specified in
[`requirements.txt`](requirements.text).  Basically, the libraries
needed are

- Flask==1.1.2
- gunicorn==20.0.4
- python-telegram-bot==13.2

# Deployment on Google Cloud Run

The current state of the bot is prepared to run in Google Cloud Run
out-of-the-box. However, there are a few steps you have to perform
in order to make it running. To begin with, you should clone this
repository in your machine:

``` shell
git clone https://github.com/fluque1995/anonymous_inbox_bot.git
```

## Talking to the BotFather

In order to create a new bot, you have to talk to the BotFather.  You
can start a conversation with him [here](https://t.me/BotFather).
Creating a new bot using the BotFather is pretty straightforward, you
can find more information in this link:
https://core.telegram.org/bots#6-botfather

After creating you bot, BotFather should give you the `API_TOKEN` of
your bot. This token is a huge alphanumerical code that identifies
your bot with Telegram. Store this key in a safe place, and be careful
not to give it to anybody, since they can take control of your bot
using it.  The `API_TOKEN` is something similar to this:

``` shell
1234567890:aaaaaaaaaaaaaaaaaaaaaa_aaaaaaaaaaa
```

## Getting your contact information

In order to get your contact information, specifically your chat ID,
you have to talk to [@userinfobot](https://t.me/userinfobot). This
number is the identifier or your account, so again be careful not
to show it publicly, or your account can be easily spammed. From
now on, we will refer to this number as `TEACHER_CHAT_ID`, since
it is the name we will give to the variable in our code.

After getting this two descriptors, `TOKEN_ID` and `TEACHER_CHAT_ID`,
we are ready to deploy the bot in Google Cloud Run.

## Getting an account in Google Cloud Run

__Disclaimer__: The next steps are strongly inspired by this tutorial:
https://nullonerror.org/2021/01/08/hosting-telegram-bots-on-google-cloud-run/
.  This is the resource I first followed to deploy my instance of the
bot, and it is a really valuable resource. I will show the specific
steps I took, since I had never worked with Google Cloud before this
project. Because of that, this tutorial can be a bit basic for
experienced users. In that case, I recommend you to follow the
previous link. Thanks to the original author!
