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
(https://core.telegram.org/bots#6-botfather)
