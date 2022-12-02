from simhash import Simhash
from scipy.ndimage import gaussian_filter1d
import json
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import hashlib
import re
from scipy.spatial import distance


def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]


def segment_and_substitue(array):
    new = []
    for i in range(0, 512, 4):
        new.append(sum(array[i:i+4])//4)
    return new


m = hashlib.sha256()
filename = input("Enter filename: ")
data = json.load(open(filename, "r"))
colours=['r','g','c','m', 'y','b','k', 'w']


for i in range(len(data)):
    item = data[i]
    item = gaussian_filter1d(item, 1)
    # item = np.reshape(item, (2, 2))
    # print(len(item))
    # print("string : ", ''.join([hex(i) for i in item[:192]]))
    pos = np.max(np.nonzero(item))
    # string_data = ''.join([str(i & ~(1<<1) & ~(1<<0) & ~(1<<2) & ~(1<<3)) for i in item])
    string_data = ''.join([hex(i)[2:] for i in item[:]])
    # print(hashlib.sha256(bytes(string_data, "utf-8")).hexdigest())
    print("Hash : ", hex(Simhash((string_data)).value))
    # print("last nonzero: ", pos)
    # print("Cosine Distance : ", distance.cosine(item, [1]*512))
    # plt.plot([j for j in range(len(item))],item,colours[i])
    # plt.figure()
    # plt.matshow(item)
    # plt.show()