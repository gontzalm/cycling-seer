import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from src.transformers import PercentageTransformer


# Set plotting parameters
mpl.rcParams["figure.figsize"] = (15, 6)
plt.style.use("ggplot")
LABELS = ("Inertia", "Silhouette Score")

# Define different preprocessors (strategies)
SPECIALTIES = ["points." + sp for sp in ("classic", "gc", "tt", "sprint", "climber")]

NUM_PIPE = {
    "normal": Pipeline([
        ("imputer", SimpleImputer()),
        ("scaler", StandardScaler())
    ]),

    "percentage": Pipeline([
        ("transformer", PercentageTransformer()),
        ("scaler", StandardScaler())
    ]),
}

PREPROCESSORS = {
    "normal": ColumnTransformer([
        ("numeric", NUM_PIPE["normal"], ["weight", "height"] + SPECIALTIES),
        ("nationality", OneHotEncoder(), ["nationality"])
    ]),

    "percentage": ColumnTransformer([
        ("numeric", NUM_PIPE["normal"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage"], SPECIALTIES),
        ("nationality", OneHotEncoder(), ["nationality"])
    ]),

    "numeric_normal": ColumnTransformer([
        ("numeric", NUM_PIPE["normal"], ["weight", "height"] + SPECIALTIES)
    ]),

    "numeric_percentage": ColumnTransformer([
        ("numeric", NUM_PIPE["normal"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage"], SPECIALTIES)
    ])
}


def compute_inertia_silhouette(riders, preprocessor, kmax=20):
    """Compute inertia and silhouette score for up to kmax clusters."""
    k_vect = np.arange(2, kmax + 1)
    inertia_vect = np.empty_like(k_vect, dtype="float")
    silhouette_vect = np.empty_like(k_vect, dtype="float")

    for i, k in enumerate(k_vect):
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("kmeans", KMeans(n_clusters=k))
        ])
        pipeline.fit(riders)
        inertia_vect[i] = pipeline["kmeans"].inertia_
        silhouette_vect[i] = silhouette_score(pipeline["preprocessor"].transform(riders), pipeline["kmeans"].labels_)

    return inertia_vect, silhouette_vect


def plot_inertia_silhouette(inertia_vect, silhouette_vect, strategy):
    """Plot inertia and silhouette vs number of clusters."""
    fig, axs = plt.subplots(1, 2)
    k_vect = np.arange(2, 2 + len(inertia_vect))
    
    for ax, y, label in zip(axs, (inertia_vect, silhouette_vect), LABELS):
        ax.plot(k_vect, y)
        ax.xaxis.set_major_locator(plt.FixedLocator(k_vect))
        ax.set(xlabel="k", ylabel=label)
    
    fig.suptitle(f"Strategy: {strategy}", fontsize=16)
    plt.show()


def model_summary(riders, pipeline):
    """Show model summary."""
    n = len(pipeline["kmeans"].cluster_centers_)
    
    print(f"K-Means with {n} clusters: Summary".center(80, "-"))
    print(f"Inertia: {pipeline['kmeans'].inertia_}")
    sil = silhouette_score(pipeline["preprocessor"].transform(riders), pipeline["kmeans"].labels_)
    print(f"Silhouette score: {sil}")
    
    labels = pipeline["kmeans"].labels_
    for k in np.unique(labels):
        print(f"Riders in cluster {k}: {np.count_nonzero(labels == k)}")
