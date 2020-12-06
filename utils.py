import math
import time
import os
from memory_profiler import profile


# Similarity Function
def hamming(a, b):
    return -sum(a ^ b)


# Similarity Function
def cosine(a, b):
    return sum([x * y for x, y in zip(a, b)]) / \
           math.sqrt(sum([x * x for x in a]) * sum([y * y for y in b]))


# Read sequences
# @profile
def read_sequences(file_names, sequence_len):
    sequences = {}
    start = time.time()
    for file_name in file_names:
        # Read test sequences and insert
        f = open(file_name, 'r')
        sequences[file_name] = f.readline()[:sequence_len]
        f.close()
    end = time.time()
    print("Read Time           ", end - start)
    return sequences


# Insert sequences into SBT
# @profile
def insert_sequences(sbt, sequences):
    start = time.time()
    for name, sequence in sequences.items():
        sbt.insert_sequence(sequence=sequence, experiment_name=name)
    end = time.time()
    print("Insert Time         ", end - start)


# Insert sequences into SBT using clustering
# @profile
def insert_cluster_sequences1(sbt, sequences, bits_to_check):
    start = time.time()
    sbt.insert_cluster_sequences1(sequences=sequences.values(), experiment_names=sequences.keys(),
                                  bits_to_check=bits_to_check)
    end = time.time()
    print("Insert Time         ", end - start)


# Insert sequences into SBT using clustering
# @profile
def insert_cluster_sequences2(sbt, sequences, bits_to_check):
    start = time.time()
    sbt.insert_cluster_sequences2(sequences=sequences.values(), experiment_names=sequences.keys(),
                                  bits_to_check=bits_to_check)
    end = time.time()
    print("Insert Time         ", end - start)


# Query from SBT and report results
# @profile
def query_sequences(sbt, q_sequences, all_sequences):
    start = time.time()
    for q_sequence in q_sequences.values():
        for sequence in all_sequences.values():
            if q_sequence in sequence:
                pass
    end = time.time()
    print("Boyer-Moore Time    ", end - start)

    start = time.time()
    total_positives = 0
    true_positives = 0
    false_negatives = 0
    for name, q_sequence in q_sequences.items():
        results = sbt.query_sequence(sequence=q_sequence)
        total_positives += len(results)
        true_positives += name in results
        false_negatives += name not in results
    end = time.time()
    print("Query Time          ", end - start)
    print("Precision           ", true_positives / total_positives)
    print("False Negatives Oops", false_negatives)


# Save SBT and report size
# @profile
def save_sbt(sbt, file_name):
    sbt.save(file_name)
    print("SBT Size (Bytes)    ", os.stat(file_name)[6])