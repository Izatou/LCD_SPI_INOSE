import itertools
import pickle
import struct
from os import path
from sys import exit, stdin, stdout, stderr

import numpy as np
import pandas as pd
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

import fitur as fitur

__DIR__ = path.dirname(path.realpath(__file__))


def extractFeatureA(dataPerSampling):
    listFitur = []
    listFitur.append(fitur.SensorValueMovement(dataPerSampling))
    listFitur.append(fitur.maxSensorValue(dataPerSampling))
    listFitur.append(fitur.minSensorValue(dataPerSampling))
    listFitur.append(fitur.overlapValue(dataPerSampling))
    listFitur.append(fitur.cekDeo(dataPerSampling))
    listFitur.append(fitur.KenaikanP1P2(dataPerSampling))
    return pd.DataFrame([list(itertools.chain(*listFitur))])


def createNetworkA():
    model = Sequential()
    model.add(Dense(units=2048, activation='relu'))
    model.add(Dense(units=2048, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    optimizer = Adam(lr=0.001)
    model.compile(loss='binary_crossentropy',
                  optimizer=optimizer, metrics=['accuracy'])
    return model


def bootstrap():
    modelA = createNetworkA()
    modelA.build(input_shape=(1, 28))
    modelA.load_weights(__DIR__ + "/1.000_0.000_6284.0.multifit.hdf5")
    with open(__DIR__ + '/1.000_0.000_0.986_0.271_1425.0.pkl', 'rb') as handle:
        standarScaler = pickle.load(handle)
    return modelA, standarScaler


def predictA(modelA, standarScaler, data):
    features = extractFeatureA(data)
    data = np.array(features.iloc[:, :-2])
    data = standarScaler.transform(data)
    pred = modelA.predict(data)
    return pred


def main():
    # Bootstrapping
    modelA, standarScaler = bootstrap()
    stderr.write("Model Siap")
    stderr.flush()

    # Main Loop
    while(True):
        try:
            CMD = struct.unpack("<B", stdin.buffer.read(1))[0]
            stderr.write("Terima Command " + str(CMD))
            stderr.flush()
            if CMD == 1:
                CMD1_PREDICT(modelA, standarScaler)
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            stderr.write(e.format_exc())
            stderr.flush()
            pass


def CMD1_PREDICT(modelA, standarScaler):
    SENSORS = ['MQ2_ADC', 'MQ3_ADC', 'MQ4_ADC', 'TGS2610_ADC',
               'TGS2600_ADC', 'TGS822_ADC', 'MQ137_ADC', 'MQ138_ADC']
    NumToRead = np.frombuffer(
        buffer=stdin.buffer.read(2 * 3), dtype="uint16")
    P1 = np.frombuffer(buffer=stdin.buffer.read(
        NumToRead[0] * 8 * 2), dtype="uint16").reshape((NumToRead[0], 8))
    P2 = np.frombuffer(buffer=stdin.buffer.read(
        NumToRead[1] * 8 * 2), dtype="uint16").reshape((NumToRead[1], 8))
    P3 = np.frombuffer(buffer=stdin.buffer.read(
        NumToRead[2] * 8 * 2), dtype="uint16").reshape((NumToRead[2], 8))
    dataP1 = pd.DataFrame(P1, columns=SENSORS)
    dataP1["PROCESS"] = "P1"
    dataP2 = pd.DataFrame(P2, columns=SENSORS)
    dataP2["PROCESS"] = "P2"
    dataP3 = pd.DataFrame(P3, columns=SENSORS)
    dataP3["PROCESS"] = "P3"
    data = pd.DataFrame([])
    data = data.append(dataP1)
    data = data.append(dataP2)
    data = data.append(dataP3)

    isUnder100 = False
    for sensor in SENSORS:
        if np.min(dataP1[sensor]) < 100 or np.min(dataP2[sensor]) < 100:
            isUnder100 = True
            break
    autoInvalid = data[data['PROCESS'] == 'P2'].shape[0] <= 50 or isUnder100
    predictionA = 0 if autoInvalid else predictA(modelA, standarScaler, data)[0]
    predictionB = 0

    stdout.buffer.write(struct.pack("<f", float(predictionA))) # Valid/Invalid
    stdout.buffer.write(struct.pack("<f", float(predictionB))) # Positif/Negatif
    stdout.buffer.flush()


if __name__ == "__main__":
    main()
