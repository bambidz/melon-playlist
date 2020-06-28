# -*- coding: utf-8 -*-
import fire
from tqdm import tqdm

from arena_util import load_json
from arena_util import write_json
from arena_util import remove_seen
from arena_util import most_popular

import numpy as np

class MostPopular:
    def _generate_answers(self, train, questions,song_meta):
        
        song_infos = {}
        for t in train:
            song_infos[t['id']]=[song_meta[a]  for a in t['songs']]

        plylst_list = {}
        for plylst, songs in song_infos.items():
            plylst_list[plylst] = songs2vec(songs)

        answers = []

        for q in tqdm(questions):
            answers.append({
                "id": q["id"],
                "songs": remove_seen(q["songs"], song_mp)[:100],
                "tags": remove_seen(q["tags"], tag_mp)[:10],
            })

        return answers

    def run(self, train_fname, question_fname, song_meta_fname):
        print("Loading train file...")
        train = load_json(train_fname)

        print("Loading question file...")
        questions = load_json(question_fname)

        print("Loading song_meta file...")
        song_meta = load_json(song_meta_fname)

        print("Writing answers...")
        answers = self._generate_answers(train, questions, song_meta)
        write_json(answers, "results/results.json")

def one_hot_encode(song):
    song_vec = np.zeros(30)
    for genre in song['song_gn_gnr_basket']:
        try:
            song_vec[int(int(genre[2:])/100)-1] = 1
        except:
            pass
            #print("error in : ",genre)
    return song_vec

def normalize(v):
    #norm = np.linalg.norm(v)
    norm = np.sum(v)
    if norm == 0: 
        return v
    return v / norm

def songs2vec(songs):
    plylst_vec_list = np.zeros(30)
    for i in range(len(songs)):
        plylst_vec_list += one_hot_encode(songs[i])
    if np.linalg.norm(plylst_vec_list):
        return plylst_vec_list/np.linalg.norm(plylst_vec_list)
    return plylst_vec_list

def vec_diff(p, q):
    return np.linalg.norm(p-q)


if __name__ == "__main__":
    fire.Fire(MostPopular)
