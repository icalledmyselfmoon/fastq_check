from typing import Union


def sort_by_length(seqs: dict, length_bounds: Union[int, tuple[int]] = (0.2 ** 32)):
    """

    Returns a list of sequence names with length out of the given range().
    Allows to sort out unsuitable sequences based on their length.

    Arguments:
    -dictionary with keys -strings (names of sequences): values-tuples of strings (sequence, quality scores)
    -length_bounds: int or tuple[int], int = the maximum allowed length, tuple = allowed range of lengths
                    0.2**32 by default

    """
    unsuitable_by_length = []
    for name, (sequence, quality) in seqs.items():
        if type(length_bounds) is tuple:
            if length_bounds[0] > len(sequence) > length_bounds[1]:
                unsuitable_by_length.append(name)
        elif type(length_bounds) is int:
            if len(sequence) > length_bounds:
                unsuitable_by_length.append(name)
    return unsuitable_by_length


def sort_by_quality(seq: dict, quality_threshold: int = 0):
    """

    Returns a list of sequence names with the mean of quality scores lower than the threshold value (phred33 score).
    Allows to sort out unsuitable sequences based on the mean of quality scores.

    Arguments:
    -dictionary with keys -strings (names of sequences): values-tuples of strings (sequence, quality scores)
    -quality_threshold: int (phred33 quality scores)
                        0 by default

    """
    unsuitable_by_quality = []
    for name, (sequence, quality) in seq.items():
        q_score = [(ord(sign) - 33) for sign in quality]
        if (sum(q_score) / len(q_score)) < quality_threshold:
            unsuitable_by_quality.append(name)
    return unsuitable_by_quality


def sort_by_gc(seqs: dict, gc_bounds: Union[int, tuple[int]] = (0, 100)):
    """

    Returns a list of sequence names with gc percentage out of the given range (determined by gc_bounds argument).
    Allows to sort out unsuitable sequences based on the percentage of (G + C) in the nucleotide sequence.

    Arguments:
    -dictionary with keys -strings (names of sequences): values-tuples of strings (sequence, quality scores)
    -qc_bounds: int or tuple[int]: int = the maximum allowed gc percentage, tuple = allowed range of gc percentage
                (0,100) by default

    """
    unsuitable_by_gc = []
    for name, (sequence, quality) in seqs.items():
        gc_score = 100 * ((sequence.count('G') + sequence.count('C')) / len(sequence))
        if type(gc_bounds) is tuple:
            if gc_bounds[0] > gc_score > gc_bounds[1]:
                unsuitable_by_gc.append(name)
        elif type(gc_bounds) is int:
            if gc_score > gc_bounds:
                unsuitable_by_gc.append(name)
    return unsuitable_by_gc


def fastq_check(seqs: dict, length_bounds: Union[int, tuple[int]] = (0.2 ** 32),
                gc_bounds: Union[int, tuple[int]] = (0, 100), quality_threshold: int = 0) -> dict:
    """

    Returns a dictionary with sequences satisfying given criteria: length, gc proportion, quality threshold.

    Arguments:
    -dictionary with keys -strings (names of sequences): values-tuples of strings (sequence, quality scores)
    -length_bounds: int or tuple[int], int = the maximum allowed length, tuple = allowed range of lengths
                     0.2**32 by default
    -gc_bounds: int or tuple[int]: int indicates = maximum allowed gc percentage, tuple =  allowed range of percentage
                (0,100) by default
    -quality_threshold: int (phred33 quality scores)
                        0 by default


    """
    unsuitable_seqs = (sort_by_length(seqs) + sort_by_gc(seqs) + sort_by_quality(seqs))
    unsuitable_seqs_set = set(unsuitable_seqs)
    selected_seqs = {name: value for name, value in seqs.items() if name not in unsuitable_seqs_set}
    return selected_seqs