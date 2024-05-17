# Evaluating Scope 3 Emissions Claims through Language Models  

CS685 Final Project  

## How to Run  
Although we have a well defined pipeline for this project, we do not have a single `entrypoint` of execution. This is by design and largely because (i) several people working asynchronously on different parts of the pipeline have different machine specifications and levels of access (be it GPU vs CPU hardware, or access tokens for the LLMs used in our training and inference), (ii) mixed use of interactive notebooks and pure Python scripts, as preference by group members, and (iii) of the need to iterate over each part, with heavy manual components involved. As such, making an end-to-end run with a single command was never the objective.  

Instead, to to run this pipeline, the user will have to `cd` into the relevant subdirectory before invoking the Python interpreter; launching jupyter lab from the project's root directory will work for those parts of the pipeline. Additionally, the user will need the following pre-requisites:  
- Environment variables for needed for `huggingface.co`, `together.ai`, and `openai.com` API tokens.  

        export HUGGINGFACE_API_KEY=<your_token>
        export TOGETHER_API_KEY=<your_token>
        export OPENAI_API_KEY=<your_token>

- Several external libraries, which we added to the `requirements.txt` file. We recommend running these scripts in a `cuda` virtual environment.  
- Two existing directories, `raw_docs` and `parsed_docs` under `/src/`, with the unprocessed PDF reports in the raw directory.  

The general flow of the pipeline is first preprocessing, then model training and inference, and finally scoring, error, and correlation analyses.  


### Preprocessing  
We first manually collected sustainability reports, in PDF format, for 93 of the largest U.S. companies. The following command (when ran in `scripts/`) parses the raw PDFs, cleans the output, and places the output into text files in `clean_reports/`.  

    python pdftext_cleaner.py


### Model training and inference  
The following set of Jupyer Notebooks are where we run our encoder and decoder models; environment variables , though we do have hard-coded unsloth token in the code.

    encoder_model.ipynb
    decoder_model.ipynb

    run_baseline.ipynb
    run_gpt.ipynb

### Scoring and error analysis  
This script in `report_prediction/` applies the scoring methodology to our model's output.  

    python score_data.py

We used the following scripts for baseline comparisons of the model's results in `errors_annotations/error_analysis_and_annotations/`.  

    baselines_comparison.py
    clean_baselines_scope3.py
    clean_baselines_vagueness.py
    gpt3.5_compare.py
    gpt4_mistral_error_analysis.py

And for error analysis, we leveraged another five custom scripts in the same directory.  

    decoder_test_error_analysis.py
    decoder_test_error_analysis_vagueness.py
    error_analysis_mosaic plot.py
    error_analysis_semantic_syntactic.py
    manual_annotation_plots.py

Finally, in `comp_scores/`, the following notebook compares our model's results against ESG rankings for more than one public dataset.  

    correlate_newsweek.ipynb
