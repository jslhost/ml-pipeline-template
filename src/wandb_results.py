import os
import pickle
import wandb
import json

api = wandb.Api()
sweep = api.sweep("jslhost-jean-simon-lhost/ml-pipeline-experiment/j5cmmlj2")
best = sweep.best_run(order="accuracy/test")
cfg_raw = best.config

cfg_dict = json.loads(cfg_raw)

wanted = {k: cfg_dict.get(k)['value'] for k in ["C", "gamma", "kernel", "probability"]}
print(wanted)

model_artifacts = [a for a in best.logged_artifacts() if a.type == "model"]
best_model_art = model_artifacts[-1]  # le plus récent si plusieurs
dirpath = best_model_art.download()   # télécharge dans le dossier artifacts

model_path = os.path.join(dirpath, "model.pkl")

with open(model_path, "rb") as f:
    best_model = pickle.load(f)

print("Modèle chargé depuis:", model_path)
