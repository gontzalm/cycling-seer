import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
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
    ]),

    "percentage": Pipeline([
        ("transformer", PercentageTransformer()),
    ]),

    "normal_std": Pipeline([
        ("imputer", SimpleImputer()),
        ("scaler", StandardScaler())
    ]),

    "percentage_std": Pipeline([
        ("transformer", PercentageTransformer()),
        ("scaler", StandardScaler())
    ]),

    "normal_minmax": Pipeline([
        ("imputer", SimpleImputer()),
        ("scaler", MinMaxScaler())
    ]),

    "percentage_minmax": Pipeline([
        ("transformer", PercentageTransformer()),
        ("scaler", MinMaxScaler())
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

    "normal_std": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_std"], ["weight", "height"] + SPECIALTIES),
        ("nationality", OneHotEncoder(), ["nationality"])
    ]),

    "percentage_std": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_std"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage_std"], SPECIALTIES),
        ("nationality", OneHotEncoder(), ["nationality"])
    ]),

    "normal_minmax": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_minmax"], ["weight", "height"] + SPECIALTIES),
        ("nationality", OneHotEncoder(), ["nationality"])
    ]),

    "percentage_minmax": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_minmax"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage_minmax"], SPECIALTIES),
        ("nationality", OneHotEncoder(), ["nationality"])
    ]),

    "numeric_normal": ColumnTransformer([
        ("numeric", NUM_PIPE["normal"], ["weight", "height"] + SPECIALTIES)
    ]),

    "numeric_percentage": ColumnTransformer([
        ("numeric", NUM_PIPE["normal"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage"], SPECIALTIES)
    ]),

    "numeric_normal_std": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_std"], ["weight", "height"] + SPECIALTIES)
    ]),

    "numeric_percentage_std": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_std"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage_std"], SPECIALTIES)
    ]),

    "numeric_normal_minmax": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_minmax"], ["weight", "height"] + SPECIALTIES)
    ]),

    "numeric_percentage_minmax": ColumnTransformer([
        ("numeric", NUM_PIPE["normal_minmax"], ["weight", "height"]),
        ("points", NUM_PIPE["percentage_minmax"], SPECIALTIES)
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


def model_summary(riders, strategy, k):
    """Show model summary."""
    # Define pipeline and do clustering
    pipeline = Pipeline([
        ("preprocessor", PREPROCESSORS[strategy]),
        ("kmeans", KMeans(n_clusters=k)),
    ])
    pipeline.fit(riders)

    # Inertia & silhouette score
    print(f"K-Means with strategy '{strategy}' and {k} clusters: Summary".center(80, "_"))
    print(f"Inertia: {pipeline['kmeans'].inertia_}")
    sil = silhouette_score(pipeline["preprocessor"].transform(riders), pipeline["kmeans"].labels_)
    print(f"Silhouette score: {sil}\n")
    
    # Number of riders in each cluster
    labels = pipeline["kmeans"].labels_
    for i in np.unique(labels):
        print(f"Riders in cluster {i}: {np.count_nonzero(labels == i)}")
    print()

    # Show 10 riders in each cluster
    riders_labeled = riders.copy()
    riders_labeled["cluster"] = labels
    for cluster in range(k):
        print(f"Cluster {cluster}".center(80, "-"))
        riders = riders_labeled[riders_labeled["cluster"] == cluster]
        print(riders.describe())
        print("\nSome riders in this cluster:\n")
        print(riders["name"].head(10).to_list())
        print()
