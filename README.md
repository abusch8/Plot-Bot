# Plot Bot

The following lays out the steps needed to recreate the results of Plot Bot presented in 410.

1.  Install the projects dependencies with `pip3 install -r requirements.txt`.

2.  Retrieve and preprocess dataset.

    This step has been entirely automated, run `python3 wiki_rip.py` and select a genre when prompted to retrieve all specified plot data from Wikipedia.  Output is written to the data directory stored in the root of the project.

3.  Prepare dataset for nanoGPT.

    A preparation script needs to be created for the dataset.  These are stored within the data directory under nanoGPT.  Some examples are listed under `sample_data`.

    After creating the script run `python3 prepare.py`.  This should generate `train.bin`, `val.bin`, and `meta.pkl` files within the same directory.

4.  Configure nanoGPT for the specific dataset.

    A config file must be created for the dataset.  These are stored within the config directory.  The file allows you to overwrite some of the default configuration parameters within `train.py`.  The advantage of this is that you can have separate configurations for each dataset.  Some examples are listed under `sample_config`.

5.  Train nanoGPT on the prepared dataset.

    **Disclaimer:** This step will not work on Windows. Training the model can only be achieved on Unix-based operating systems.  The use of Windows Subsystem for Linux can negate this.  For more information visit: https://docs.nvidia.com/cuda/wsl-user-guide/index.html#getting-started-with-cuda-on-wsl.

    Now you can begin training the model.  Run `python3 train.py config/your_config.py`.  Checkpoints are outputted to the specified directory in your config.  A line graph will be generated after the training is complete, the data points are stored within a `plot_data.json` file in your specified output directory.

6.  Sample/generate output from the trained language model.

    To generate an infinite steam of output, run `python3 generate.py --our_dir=your_output_directory`.  The script will use the most recent checkpoint and also write the generation to an output txt file within the same directory.

    To sample the language model to perform evaluations, run `python3 sample.py --our_dir=your_output_directory`.  The script will iterate over each checkpoint and generate a short sample txt file within the same directory.

7.  Evaluate the language model.

    Plot Bot offers two methods of evaluation:

    -  **Grammar Check**

        Update the `SAMPLE_DIR` variable to your nanoGPT sample output directory.  Run the script with `python3 grammar_check.py`.  The script will evaluate the grammar of each checkpoint sample.  Once completed a line graph will be generated.

    -  **Sentence Similarity**

        Update the `SAMPLE_DIR` variable to your nanoGPT sample output directory and update `INPUT_DIR` to the original dataset.  Run the script with `python3 sentence_similarity.py`.  The script will evaluate the similarity of each sample to the original dataset.  Once completed a line graph will be generated.

8.  Generate summaries and movie poster artwork utilizing ChatGPT and DALL-E.

    The following prompt was used with GPT-4 to generate a summary and a prompt used for DALL-E.

    ```
    I am going to give  you a movie plot and I want you to first summarize it and then I want you to create a prompt for dall-e that describes what a promotional movie poster for the movie would look like.
    ```

For more instructions on the usage of nanoGPT, check its included `README.md` file or its original repository: https://github.com/karpathy/nanoGPT.
