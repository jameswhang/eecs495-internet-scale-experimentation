RESULT_FILE = 'measurements_021017.csv'

attempt_1_file = open('measurements_021017_1.csv', 'wb')
attempt_2_file = open('measurements_021017_2.csv', 'wb')
attempt_3_file = open('measurements_021017_3.csv', 'wb')
results = open(RESULT_FILE).readlines()

attempt_1_file.write(results[0])
attempt_2_file.write(results[0])
attempt_3_file.write(results[0])

for idx, line in enumerate(results[1:]):
    if idx % 3 == 0:
        attempt_1_file.write(line)
    elif idx % 3 == 1:
        attempt_2_file.write(line)
    else:
        attempt_3_file.write(line)
