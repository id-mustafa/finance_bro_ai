# finance_bro_ai
Finance Bro AI is an AI RAG (Retrieval Augmented Generation) application that is specifically tailored to answer the questions you have about stocks!


### Setting up the environment
You can run ```bash python3 -m venv ./venv ``` to create your virtual environment. Then run ```bash source ./venv/bin/activate ``` to activate the newly created environment. 

MAKE SURE YOU ADD THIS TO THE .gitignore FILE AS /venv

The dependencies needed to install for this project are going to be placed within the requirements.txt file for easy package management. You can run the following command to install all dependencies:

you may also run the command: 
```bash pip3 install -r requirements.txt```

Make sure you have an OpenAI API key, if you already have an account, then you can set the OpenAPI key in the .env file. Note that to run this application, you need to have OpenAI credits. This is done for simplicity sake of getting an MVP up fast with a model that is able to respond well to user input. As a stretch goal, it would be nice to migrate this setup to a model that has a free tier!

First create the .env file and the OpenAPI key usage is going to be listed in the .env file as:

```env OPENAI_API_KEY=<YOUR API KEY>```

IMPORTANT: DO NOT PUSH YOUR API KEY TO GITHUB. MAKE SURE TO INCLUDE .env IN THE .gitignore FILE IF IT IS NOT ALREADY PRESENT.

Ensure that you run the indexing.py script to create your vector store with chroma, you can easily do this by running the following command:

```bash python3 indexing.py```

If it isn't included already, you must also make sure that you include /chroma_store in the .gitignore to avoid pushing up a large sqlite database.

### Running the application 
To run the application, you would need to run the following command:
```bash streamlit run 1_🤖_Finance_Bro_AI.py```

### Environment for Developers
If you plan on adding packages to this project then you may install them with pip and then freeze them to the requirements.txt file using the following command:

```bash pip3 freeze > requirements.txt```

##### Branching off for feature updates
Make sure that you branch off main to develop features and open up a PR request for your seperate branch. 


