import numpy as np
import tensorflow as tf

GREEN_RGB = [140, 195, 50]


def clean_profile(batch):
    """Clean profile image."""
    # Iterate through batch
    for img_tensor in batch.shape[0]

    # Convert tensor to numpy array
    img_array = np.array(img_tensor)

    # Find green areas
    mask = np.all(np.isclose(img_array, GREEN_RGB, rtol=0.3), axis=-1)

    # Set green areas to black and the rest to white
    img_array[mask] = [0, 0, 0]
    img_array[np.logical_not(mask)] = [255, 255, 255]

    return tf.constant(img_array, dtype=tf.float32)
