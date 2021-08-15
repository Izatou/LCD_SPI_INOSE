import numpy as np

# VARIABLE TUNING
DESIRED_COLUMNS_MQ = ['MQ2_ADC', 'MQ3_ADC',
                      'MQ4_ADC', 'MQ137_ADC', 'MQ138_ADC']
POTONG_SEBELUM = 15
POTONG_SETELAH = 15
DIVIDE_REGION = 6
MIN_SLOPE = -1
MAX_SLOPE = 1
DELTA_SLOPE_MAX_NEAR_ZERO = .1


def KenaikanP1P2(dataSensor):
    p1 = dataSensor[dataSensor['PROCESS'] == 'P1']
    p1 = p1[2:-2]
    p1_mean = np.mean(p1.iloc[:, 1:9])
    p2 = dataSensor[dataSensor['PROCESS'] == 'P2']
    p2 = p2.iloc[15:-15, :]
    p2 = np.mean(p2.iloc[:, 1:9]) - p1_mean.values

    p2 = p2[DESIRED_COLUMNS_MQ]

    return p2


def SensorValueMovement(dataSensor):
    p1 = dataSensor[dataSensor['PROCESS'] == 'P1']
    p1 = p1[2:-2]
    p1_mean = np.mean(p1.iloc[:, 1:9])
    p2 = dataSensor[dataSensor['PROCESS'] == 'P2']
    p2 = p2.iloc[:, 1:9] - p1_mean.values
    p2 = p2.iloc[15:-15, :]

    p2 = p2[DESIRED_COLUMNS_MQ]
    return (np.max(p2)-np.min(p2)).tolist()


def maxSensorValue(dataSensor):
    p1 = dataSensor[dataSensor['PROCESS'] == 'P1']
    p1 = p1[2:-2]
    p1_mean = np.mean(p1.iloc[:, 1:9])
    p2 = dataSensor[dataSensor['PROCESS'] == 'P2']
    p2 = p2.iloc[:, 1:9] - p1_mean.values
    p2 = p2.iloc[15:-15, :]

    p2 = p2[DESIRED_COLUMNS_MQ]
    return np.max(p2).tolist()


def minSensorValue(dataSensor):
    p1 = dataSensor[dataSensor['PROCESS'] == 'P1']
    p1 = p1[2:-2]
    p1_mean = np.mean(p1.iloc[:, 1:9])
    p2 = dataSensor[dataSensor['PROCESS'] == 'P2']
    p2 = p2.iloc[:, 1:9] - p1_mean.values
    p2 = p2.iloc[15:-15, :]

    p2 = p2[DESIRED_COLUMNS_MQ]
    return np.min(p2).tolist()


def overlapValue(dataSensor):
    p2 = dataSensor[dataSensor['PROCESS'] == 'P2']
    p2 = p2.iloc[15:-15, :]

    p2 = p2[DESIRED_COLUMNS_MQ]

    # Cari selisih terhadap masing-masing nilai sensor

    layer1 = {}  # 5 angka
    for sensorValue in p2.columns:
        layer1[sensorValue] = np.mean(p2[sensorValue])

    # 20 loop
    layer3 = []
    for sensorValue in p2.columns:
        layer2 = []
        for sensorValueAgainst in p2.columns:
            if (sensorValue == sensorValueAgainst):
                continue
            layer2.append(abs(layer1[sensorValue] -
                          layer1[sensorValueAgainst]))
        layer3.append(np.min(np.array(layer2)))

    return layer3  # 5 angka


def fft(signal):
    rft = np.fft.rfft(signal)
    rft[5:] = 0   # Note, rft.shape = 21
    y_smooth = np.fft.irfft(rft)
    return y_smooth


def slope(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    return m


def countSlope(signal):
    slopes = []
    for count, tick in enumerate(signal):
        if count == 0:
            continue
        else:
            slopes.append(slope(count-1, signal[count-1], count, tick))

    return slopes


def divideIntoRegion(data, num):
    data492MQ2FFTSlopeLen = np.floor(len(data) / num)
    data492MQ2FFTSlopeDivided = []
    data492MQ2FFTSlopeDividedCurrent = []
    for count, plot in enumerate(data):
        if count % data492MQ2FFTSlopeLen == 0:
            data492MQ2FFTSlopeDividedCurrent = []
            data492MQ2FFTSlopeDividedCurrentIndex = []
            data492MQ2FFTSlopeDivided.append(
                (data492MQ2FFTSlopeDividedCurrentIndex, data492MQ2FFTSlopeDividedCurrent))

        data492MQ2FFTSlopeDividedCurrent.append(plot)
        data492MQ2FFTSlopeDividedCurrentIndex.append(count)

    return data492MQ2FFTSlopeDivided[:num]


def defineSensorStableValue(signal, slope, regionNum):
    slopeDivided = divideIntoRegion(slope, regionNum)
    dataToAvg = []
    for region, data in enumerate(slopeDivided):
        (originalIndex, slopes) = data
        maxVal = np.max(slopes)
        minVal = np.min(slopes)
        if maxVal <= MAX_SLOPE and minVal >= MIN_SLOPE:
            for index, plotSlope in enumerate(slopes):
                if(np.abs(plotSlope) < DELTA_SLOPE_MAX_NEAR_ZERO):
                    dataToAvg.append(signal[originalIndex[index]])

    if(len(dataToAvg) == 0):
        return 0
    else:
        return np.average(dataToAvg)


def cekDeo(dataSensor):
    p1 = dataSensor[dataSensor['PROCESS'] == 'P1']
    p1 = p1[2:-2]
    p1_mean = np.mean(p1.iloc[:, 1:9])
    p2 = dataSensor[dataSensor['PROCESS'] == 'P2']
    p2 = p2.iloc[:, 1:9] - p1_mean.values
    p2 = p2.iloc[15:, :]

    maxS1 = np.max(p2['MQ2_ADC'])
    maxS2 = np.max(p2['MQ3_ADC'])

    # cek nilai stabil dari S6 dengan karakteristik MQ
    # simpan nilainya
    dataPerSensorTrimmed = list(
        p2['TGS822_ADC'].iloc[POTONG_SEBELUM:-POTONG_SETELAH, ].values)
    dataPerSensorTrimmedFFT = fft(dataPerSensorTrimmed)
    dataPerSensorTrimmedFFTSlope = countSlope(dataPerSensorTrimmedFFT)
    sensorStableValue = defineSensorStableValue(
        dataPerSensorTrimmedFFT, dataPerSensorTrimmedFFTSlope, DIVIDE_REGION)
    sensorStableValue = np.round(sensorStableValue, decimals=2)

    return [maxS1, maxS2, sensorStableValue]
