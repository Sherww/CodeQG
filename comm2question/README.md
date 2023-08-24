# Comment to Question
We use the generator proposed by Kaustubh et al. In order to get up and running, perform the following steps

0. Ensure that you have the Parsing Server installed and running. 
(The Parsing Server is a modified version of the flask server of AllenNLP so it not only contains AllenNLP models 
but other services like wordNet hypernym extraction, verb to noun converter, etc.) 

#### Setting up the Parser Serve

[Conda](https://conda.io/) can be used set up a virtual environment with the
version of Python required for AllenNLP. 

1.  [Download and install Conda](https://conda.io/docs/download.html).

2.  Create a Conda environment with Python 3.6

    ```bash
    conda create -n synqg python=3.6
    ```

3.  Activate the Conda environment. You will need to activate the Conda environment in each terminal in which you want to use AllenNLP.

    ```bash
    conda activate synqg
    ```
    
4. Run pip install . from the root of source folder.

#### Running the module

To run the module, you need to run the following three steps:

1. Start the Parsing server 
    ```bash
    python allennlp/service/server_simple.py
    ```
   
2. Start the Back Translation server
    ```bash
     python backtranslation/back_translation_server.py 
    ```
    
