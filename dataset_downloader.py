from sklearn import datasets
import pandas as pd


def download_dataset(name):

    name = name.lower()

    if "iris" in name:

        data = datasets.load_iris()

        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["target"] = data.target

        df.to_csv("iris_dataset.csv", index=False)

        print("Iris dataset downloaded successfully.")

    elif "wine" in name:

        data = datasets.load_wine()

        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["target"] = data.target

        df.to_csv("wine_dataset.csv", index=False)

        print("Wine dataset downloaded successfully.")

    elif "breast cancer" in name:

        data = datasets.load_breast_cancer()

        df = pd.DataFrame(data.data, columns=data.feature_names)
        df["target"] = data.target

        df.to_csv("breast_cancer_dataset.csv", index=False)

        print("Breast cancer dataset downloaded successfully.")

    else:

        print("Dataset not supported yet.")