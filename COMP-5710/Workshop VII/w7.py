from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets, linear_model
import pandas as pd
import numpy as np
import mnist
from sklearn.model_selection import KFold
from sklearn.datasets import load_iris
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.utils import to_categorical
from tensorflow import keras
import myLogger

# Initialize the forensic logger
logObj = myLogger.giveMeLoggingObject()

def readData():
    iris = datasets.load_iris()
    print(type(iris.data), type(iris.target))
    X = iris.data
    Y = iris.target

    # LOGGING: Log dataset shape and feature count to detect poisoning via unexpected data dimensions
    logObj.info("readData - Loaded Iris dataset: shape={}, features={}, targets={}".format(X.shape, X.shape[1], len(np.unique(Y))))

    df = pd.DataFrame(X, columns=iris.feature_names)
    print(df.head())

    # LOGGING: Check for NaN/null values to detect poisoned datasets injecting corrupt/missing entries
    nan_count = df.isnull().sum().sum()
    logObj.info("readData - DataFrame created: rows={}, NaN count={}".format(len(df), nan_count))
    if nan_count > 0:
        logObj.warning("readData - WARNING: {} NaN values detected, possible data poisoning".format(nan_count))

    return df

def makePrediction():
    iris = datasets.load_iris()
    knn = KNeighborsClassifier(n_neighbors=6)
    knn.fit(iris['data'], iris['target'])

    # LOGGING: Log model config to detect tampering with training parameters
    logObj.info("makePrediction - KNN model fitted: training_samples={}, n_neighbors={}, n_features={}".format(iris['data'].shape[0], knn.n_neighbors, iris['data'].shape[1]))

    X = [
        [5.9, 1.0, 5.1, 1.8],
        [3.4, 2.0, 1.1, 4.8],
    ]

    # LOGGING: Log input feature values and ranges to detect anomalous inputs designed to trick the model
    X_arr = np.array(X)
    logObj.info("makePrediction - Prediction input: samples={}, feature_mins={}, feature_maxs={}".format(len(X), X_arr.min(axis=0).tolist(), X_arr.max(axis=0).tolist()))

    prediction = knn.predict(X)

    # LOGGING: Log prediction results to detect unexpected classifications indicating model tricking
    logObj.info("makePrediction - Prediction results: {}".format(prediction.tolist()))

    print(prediction)

def doRegression():
    diabetes = datasets.load_diabetes()
    diabetes_X = diabetes.data[:, np.newaxis, 2]
    diabetes_X_train = diabetes_X[:-20]
    diabetes_X_test = diabetes_X[-20:]
    diabetes_y_train = diabetes.target[:-20]
    diabetes_y_test = diabetes.target[-20:]

    # LOGGING: Log train/test set sizes to detect poisoning via unexpected data split ratios
    logObj.info("doRegression - Data split: train_size={}, test_size={}, total={}".format(len(diabetes_X_train), len(diabetes_X_test), len(diabetes_X)))

    regr = linear_model.LinearRegression()
    regr.fit(diabetes_X_train, diabetes_y_train)

    # LOGGING: Log model coefficients and intercept to detect model manipulation via anomalous learned parameters
    logObj.info("doRegression - Model fitted: coefficients={}, intercept={:.4f}".format(regr.coef_.tolist(), regr.intercept_))

    diabetes_y_pred = regr.predict(diabetes_X_test)

    # LOGGING: Log predicted values summary to detect regression outputs outside expected range
    logObj.info("doRegression - Predictions: min={:.2f}, max={:.2f}, mean={:.2f}".format(diabetes_y_pred.min(), diabetes_y_pred.max(), diabetes_y_pred.mean()))


def doDeepLearning():


    (train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()

    # LOGGING: Log training/test data shapes and label distribution to detect data poisoning via altered dimensions or label imbalance
    unique_labels, label_counts = np.unique(train_labels, return_counts=True)
    logObj.info("doDeepLearning - MNIST loaded: train_shape={}, test_shape={}, labels={}, label_distribution={}".format(train_images.shape, test_images.shape, unique_labels.tolist(), label_counts.tolist()))

    train_images = (train_images / 255) - 0.5
    test_images = (test_images / 255) - 0.5


    train_images = np.expand_dims(train_images, axis=3)
    test_images = np.expand_dims(test_images, axis=3)

    num_filters = 8
    filter_size = 3
    pool_size = 2

    model = Sequential([
    Conv2D(num_filters, filter_size, input_shape=(28, 28, 1)),
    MaxPooling2D(pool_size=pool_size),
    Flatten(),
    Dense(10, activation='softmax'),
    ])

    # Compile the model.
    model.compile(
    'adam',
    loss='categorical_crossentropy',
    metrics=['accuracy'],
    )

    # Train the model.
    history = model.fit(
    train_images,
    to_categorical(train_labels),
    epochs=3,
    validation_data=(test_images, to_categorical(test_labels)),
    )

    # LOGGING: Log final training accuracy and loss to detect model tricking via abnormally low/high training metrics
    final_acc = history.history['accuracy'][-1]
    final_loss = history.history['loss'][-1]
    logObj.info("doDeepLearning - Training complete: final_accuracy={:.4f}, final_loss={:.4f}, epochs={}".format(final_acc, final_loss, len(history.history['accuracy'])))

    model.save_weights('cnn.weights.h5')

    predictions = model.predict(test_images[:5])

    # LOGGING: Log predicted vs actual labels for test samples to detect incorrect predictions indicating model has been tricked
    predicted_labels = np.argmax(predictions, axis=1)
    logObj.info("doDeepLearning - Predictions: predicted={}, actual={}, match={}".format(predicted_labels.tolist(), test_labels[:5].tolist(), (predicted_labels == test_labels[:5]).tolist()))

    print(np.argmax(predictions, axis=1)) # [7, 2, 1, 0, 4]

    print(test_labels[:5]) # [7, 2, 1, 0, 4]

def k_fold_cv_mlp(n_splits):

  iris_data = load_iris()
  X_data = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
  ## to numpy
  X=  X_data.to_numpy()
  y = iris_data.target


  kf = KFold(n_splits)
  folds = []

  for train_index, test_index in kf.split(X):
      folds.append((train_index, test_index))


  # Initialize machine learning model, MLP
  model = MLPClassifier(hidden_layer_sizes=(256,128,64,32),activation="relu",random_state=1)

  # Initialize a list to store the evaluation scores
  scores = []
  ## Initialize fold index
  fold_index = 0


  # Iterate through each fold
  for train_indices, test_indices in folds:
      X_train, y_train = X[train_indices], y[train_indices]
      X_test, y_test = X[test_indices], y[test_indices]


      fold_index += 1
      print(f"Fold {fold_index}:")

      # LOGGING: Log fold index, train/test sizes, and label distribution to detect poisoning via imbalanced or corrupted fold data
      unique_train, train_counts = np.unique(y_train, return_counts=True)
      logObj.info("k_fold_cv_mlp - Fold {}: train_size={}, test_size={}, train_label_distribution={}".format(fold_index, len(X_train), len(X_test), dict(zip(unique_train.tolist(), train_counts.tolist()))))

      # scale data
      sc_X = StandardScaler()
      X_train_scaled=sc_X.fit_transform(X_train)
      X_test_scaled=sc_X.transform(X_test)

      # Train the model on the training data
      model.fit(X_train_scaled, y_train)

      # Make predictions on the test data
      y_pred = model.predict(X_test_scaled)

      # Calculate the accuracy score for this fold
      fold_score = accuracy_score(y_test, y_pred)
      print(f"Fold test score {fold_score}:")

      # Append the fold score to the list of scores
      scores.append(fold_score)

  # Calculate the mean accuracy across all folds
  mean_accuracy = np.mean(scores)

  # LOGGING: Log all fold scores and mean accuracy to detect anomalous accuracy variance indicating data poisoning across folds
  logObj.info("k_fold_cv_mlp - All folds complete: scores={}, mean_accuracy={:.4f}, std_dev={:.4f}".format(scores, mean_accuracy, np.std(scores)))

  print("K-Fold Cross-Validation Scores:", scores)
  print("Mean Accuracy:", mean_accuracy)

if __name__=='__main__':
    # LOGGING: Log application start with timestamp to establish forensic timeline for incident investigation
    logObj.info("APPLICATION START - w7.py forensic logging session initiated")

    data_frame = readData()
    makePrediction()
    doRegression()
    my_k_fold = input('Type in k for cross valdation: ')
    my_k_fold = int(my_k_fold)
    k_fold_cv_mlp(my_k_fold)
    doDeepLearning()
