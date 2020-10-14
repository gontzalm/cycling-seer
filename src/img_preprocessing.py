import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


GREEN_RGB = [140, 195, 50]


def clean_profile(img_tensor):
    """Clean profile image."""
    # Convert tensor to numpy array
    img_array = img_tensor.numpy()

    # Find green areas
    mask = np.all(np.isclose(img_array, GREEN_RGB, rtol=0.3), axis=-1)

    # Set green areas to black and the rest to white
    img_array[mask] = [0, 0, 0]
    img_array[np.logical_not(mask)] = [255, 255, 255]

    return tf.constant(img_array, dtype=tf.float32)


def tf_clean_profile(img, label):
    """Tensorflow version of clean_profile."""
    img_shape = img.shape
    [img,] = tf.py_function(clean_profile, [img], [tf.float32])
    img.set_shape(img_shape)
    return img, label
    

def overview(dataset, class_names, cmap=None):
    """Show overview of dataset."""
    for imgs, labels in dataset.take(1):
        _, axs = plt.subplots(3, 3, figsize=(10, 10))
        for i, ax in enumerate(axs.flat):
            ax.imshow(imgs[i].numpy().astype("uint8"), cmap=cmap)
            ax.set_title(class_names[labels[i]])
            ax.axis("off")
