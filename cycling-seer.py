#!/home/gontz/miniconda3/envs/ih/bin/python3

import click
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from src import dbops
from src.img_preprocessing import clean_profile


@click.command()
@click.argument("profile")
def predict():
    """Predict riders with most probability of winning stage with profile PROFILE."""
    model = keras.models.load_model("model/clf.h5")
    
    # Load profile
    profile = keras.preprocessing.image.load_img(profile, target_size=(256, 256))
    profile = keras.preprocessing.image.img_to_array(profile)
    profile = clean_profile(tf.constant(profile, dtype=tf.float32))
    profile = tf.image.rgb_to_grayscale(profile)
    profile = tf.expand_dims(profile, 0)

    # Make prediction
    prediction = model.predict(profile)
    cluster = np.argmax(prediction)
    probability = np.max(prediction)
    
    # Get active riders from predicted cluster
    riders = dbops.fetch_riders()
    riders = pd.json_normalize(riders)
    riders = riders[(riders["cluster"] == cluster) & (riders["active"])]
    riders.drop(columns=["active", "img"], inplace=True)
    riders["total_points"] = riders.loc[:, "points.classic":"points.climber"].sum(axis=1)
    riders.sort_values("total_points", inplace=True)
    
    # Display prediction info
    click.echo(f"Predicted cluster: {cluster}".center(80, "-"))
    click.echo(f"Top active riders in cluster {cluster}:".center(80, "-"))
    print(riders.head(10))
