# BERT(S) for Relation Extraction between Trigger-Action Rules

An implementation of a system that uses a machine learning approach to infer cause-effect relations between actions and triggers in trigger-action rules.

It utilizes a BERT model, as implemented by the following repository: https://github.com/plkmo/BERT-Relation-Extraction.

## Getting started

### Training and Fine-tuning

As described in the *BERT-Relation-Extraction* repository, you can train and fine-tune the model using the scripts: *main_pretraining.py* (for the training) and *main_task.py* (for the fine-tuning). Check that repository for the details.

### Generating the input dataset

Once the model was trained, you can infer cause-effect relations between actions and triggers of rules.

To do this, you must first generate a file containing some phrases in the form: *action and trigger*. You can generate such file from a dataset of trigger-action rules running the script *create_recipes_rel_dataset.py*.

    create_recipes_rel_dataset.py [-h]
        [--input_file DATASET OF TRIGGER-ACTION RULES, CSV FORMAT]
        [--output_file OUTPUT DATASET, CSV FORMAT]
        [--start_index START INDEX OF INPUT FILE FROM WHICH GENERATE THE PHRASES]
        [--end-index END INDEX OF INPUT FILE FROM WHICH GENERATE THE PHRASES]

### Inference

Once generated the file as described previously, you can infer cause-effect relations running the script *infer_relations.py*.

    infer_relations.py [-h]
    [--input_dataset THE FILE GENERATED IN THE PREVIOUS STEP]
    [--output_dataset THE FILE WHERE THE INFERRED RELATIONS WILL BE SAVED]