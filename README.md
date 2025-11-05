# Appwrite Jobs - Legacy Backend for QReady

## Overview

This project is an outdated version of the backend for the QReady app. It is important to note that this script is **highly outdated**, with a modified database structure and support for **German-language requests only**.

## What the Script Does

The script listens for job creation events in Appwrite. A "job" refers to a user's request to convert a PDF file into a learning set. When a job request is detected, the script processes it as follows:

1. **PDF to Text Conversion**: The PDF file is converted into text.
2. **Text to JSON Conversion**: Using the OpenAI API, the text is transformed into the appropriate JSON format.
3. **Database Storage**: The resulting JSON is saved in the Appwrite database.

Once the process is complete, the user can access their learning set.

## Limitations

- The script is outdated and may not work with the current database structure.
- It only supports requests in the German language.

## Disclaimer

This project is provided as-is for reference purposes and is not recommended for production use due to its outdated nature.
