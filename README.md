# BERT(S) for Relation Extraction between Trigger-Action Rules

An implementation of a system that uses a machine learning approach to infer cause-effect relations between actions and triggers in trigger-action rules.

It utilizes a BERT model, as implemented by the following repository: https://github.com/plkmo/BERT-Relation-Extraction.

## Getting started

### Training

You can train the BERT model running the script *main_pretraining.py*. As described in the *BERT-Relation-Extraction* repository, pre-training data can be any .txt continuous file.

    main_pretraining.py [-h]
        [--pretrain_data TRAIN_PATH]
        [--batch_size BATCH_SIZE]
        [--freeze FREEZE]
        [--gradient_acc_steps GRADIENT_ACC_STEPS]
        [--max_norm MAX_NORM]
	    [--fp16 FP_16]  
	    [--num_epochs NUM_EPOCHS]
	    [--lr LR]
	    [--model_no MODEL_NO (0: BERT ; 1: ALBERT ; 2: BioBERT)]
        [--model_size MODEL_SIZE (BERT: 'bert-base-uncased', 'bert-large-uncased';   
				ALBERT: 'albert-base-v2', 'albert-large-v2';   
				BioBERT: 'bert-base-uncased' (biobert_v1.1_pubmed))]

### Fine-tuning

For fine-tune the model on data, you can run the script *main_task.py*.

    main_task.py [-h] 
	[--train_data TRAIN_DATA]
	[--test_data TEST_DATA]
    [--train_data_size TRAIN_DATA_SIZE]
	[--use_pretrained_blanks USE_PRETRAINED_BLANKS]
	[--batch_size BATCH_SIZE]
	[--gradient_acc_steps GRADIENT_ACC_STEPS]
	[--max_norm MAX_NORM]
	[--fp16 FP_16]  
	[--num_epochs NUM_EPOCHS]
	[--lr LR]
	[--model_no MODEL_NO (0: BERT ; 1: ALBERT ; 2: BioBERT)]  
	[--model_size MODEL_SIZE (BERT: 'bert-base-uncased', 'bert-large-uncased';   
				ALBERT: 'albert-base-v2', 'albert-large-v2';   
				BioBERT: 'bert-base-uncased' (biobert_v1.1_pubmed))]    
	[--train TRAIN]
	[--infer INFER]

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

### Fine-tuning directly on trigger-action rules

You can fine-tune the model directly on trigger-action rules, to do this, you must generate a training and a test file from labelled datasets. To do this, run the script *create_train_test_files.py*.

    create_train_test_files.py [-h]
        [--train_input_file INPUT DATASET CONTAINING TRAINING LABELLED DATA, CSV FORMAT]
        [--test_input_file INPUT DATASET CONTAINING TEST LABELLED DATA, CSV FORMAT]
        [--train_output_file OUTPUT FILE CONTAINING TRAINING DATA]
        [--train_output_file OUTPUT FILE CONTAINING TEST DATA]