import gpt_2_simple as gpt2

import os

MODEL_DIR = 'finetuned_model'
MODEL_NAME = 'run1'

class Gpt2Generator(object):
    def __init__(self, max_tokens=915, **kwargs):
        self.max_tokens = max_tokens
        self.kwargs = kwargs

    def get_encoder(self):
        encoder = gpt2.src.encoder.get_encoder(os.path.join(MODEL_DIR, MODEL_NAME))
        self.encoder = encoder

    def load_gpt2(self):
        sess = gpt2.start_tf_sess()
        gpt2.load_gpt2(sess, checkpoint_dir=MODEL_DIR, run_name=MODEL_NAME)
        self.sess = sess
        self.gpt2 = gpt2

    def generate_titles(self, comment):
        assert self.gpt2, 'Must run load_gpt2() first'
        assert self.encoder, 'Must run get_encoder() first'
        try:
            author = 'u/' + comment.author.name
        except:
            author = 'u/Redditor'
        body_ = '\n'.join([author, comment.body])
        max_body_tokens = self.max_tokens - 15  # we will append more tokens
        body_trunc = self.encoder.decode(self.encoder.encode(body_)[:max_body_tokens])
        body = '\n'.join([body_trunc, comment.id, '<|rbestof|>'])
        titles = self.gpt2.generate(self.sess,
            length=100,
            temperature=0.7,
            prefix=body,
            nsamples=5,
            batch_size=5,
            include_prefix=False,
            truncate='<|endoftext|>',
            return_as_list=True,
            checkpoint_dir=MODEL_DIR,
            run_name=MODEL_NAME
        )
        titles = [title.split(maxsplit=1)[1] for title in titles]
        return titles
