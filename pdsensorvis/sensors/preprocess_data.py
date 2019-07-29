import os
import csv
import math
from django.conf import settings

NEWLINE = ''
DELIMITER = ' '
TRIM_RANGE = 7


class Preprocess:
    avg_magnitude = []
    time_stamp = []

    def __init__(self, file_name, start_frame, end_frame):
        self.process_data(file_name, start_frame, end_frame)

    def process_data(self, file_name, start_frame, end_frame):
        sample_list = []

        with open(os.path.join(settings.MEDIA_ROOT, file_name), newline=NEWLINE) as sensor_data:
            sensor_reader = csv.reader(sensor_data, delimiter=DELIMITER)
            for sample in sensor_reader:
                sample_list.append(sample)

        trun_list = sample_list[start_frame:end_frame]

        for i in range(0, TRIM_RANGE):
            [j.pop() for j in trun_list]

        for item in trun_list:
            self.time_stamp.append(int(item[0]))
            self.avg_magnitude.append(math.sqrt((float(item[1]) ** 2 + float(item[2]) ** 2 + float(item[3]) ** 2) / 3))

    @staticmethod
    def get_magnitudes(self):
        return self.avg_magnitude

    @staticmethod
    def get_times(self):
        return self.time_stamp
