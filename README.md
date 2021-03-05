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

The bot has been developed using Python 3.8. It should work independently
of the Python version, as long as it is Python 3. The requirements for
the project are specified in [`requirements.txt`](requirements.txt)
