import gpt_2_simple as gpt2

import os

MODEL_DIR = 'finetuned_model'
MODEL_NAME = 'run1'

def get_encoder():
    encoder = gpt2.src.encoder.get_encoder(os.path.join(MODEL_DIR, MODEL_NAME))
    return encoder

def load_gpt2():
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, checkpoint_dir=MODEL_DIR, run_name=MODEL_NAME)
    return sess, gpt2
