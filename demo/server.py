# Limitations under the MIT License.
# Copyright 2019 Katsuya Shimabukuro.
import responder
import pickle
import pathlib
from py_rap_gen import generator


# Load pre-trained objects
with open('mecab_tone_yomi.pkl', 'rb') as w:
    tone_list = pickle.load(w)
with open('prefix_searcher.pkl', 'rb') as w:
    prefix_searcher = pickle.load(w)
with open('learner.pkl', 'rb') as w:
    learner = pickle.load(w)

route = pathlib.Path(__file__).parent
api = responder.API(static_dir=route.joinpath('static'))
api.add_route("/", static=True)


@api.route("/generate")
def greet_world(req, resp):
    # return generating rap
    sentence = req.params['sentence']
    nums = int(req.params['nums'])
    resp.media = {"result": generator.generate_rapv2(sentence, tone_list, prefix_searcher, learner, nums)}


def main():
    api.run()
