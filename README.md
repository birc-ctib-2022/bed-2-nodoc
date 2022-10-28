# Processing BED files (Part 2)

If our BED files are sorted, we should be able to extract regions in logarithmic time instead of linear time, if we use binary search instead of linear search.

We won't *quite* get there in this project, because it will take us linear time to load a BED file into memory, but once there we will be able to do such queries. Doing it from file is possible, but involves some technical issues that we don't care to look at here. If you were to look a little deeper into files, and how to make random access queries in files, we could get the rest of the way.

If you are interested in a fully fledged tool that does what we are attempting here, you can check out [Tabix](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3042176/).

## Sorting BED files

In the file `src/sort_bed.py` there is a function

```python
def sort_file(table: Table) -> None
```

that almost sorts a BED file. I is just lacking the sorting part. The function runs through all the chromosomes in the input, and you get them as a list for each chromosome. Sort that list according to the start position. Then the rest of the program should work.

## Merging sorted BED files

If you have two sorted BED files and you want a single sorted BED file with the features from them, it is more efficient to merge them than to concatenate them and then sort them. Merging them can be done in time O(n + m), where *n* and *m* are their length, but sorting the concatenated file alone would take O((n+m)log(n+m)) with a comparison-based sorting algorithm.

The tool `src/merge_bed.py` is almost done, except for the merging. Write the code to merge the features from two BED files. When you merge, you need to consider both the chromosome and the chromosomal position. Because of the simplifying assumptions we have made about features, that they only span one nucelotide, you don't have to worry about their end position; just merge according to chromosomes and start positions.


## Querying BED files with binary search

Now, if we have a sorted BED file and we want to get the region `chrom start end` we can use the hash table I already wrote to get all features on chromosome `chrom` and from there we just need to filter these to only get those with start postion in range `start <= pos < end`.

We can break this down into two parts. First, find the first position in the interval (let's call it `pos_i`)

```
   chrom pos_{i-3} ...
   chrom pos_{i-2} ...
   chrom pos_{i-1} ...
=> chrom pos_i ...
   chrom pos_{i+1} ...
   chrom pos_{i+2} ...
```

This `pos_i` is the smallest position greater or equal to `start`. This kind of value is know as the *lower bound* of `start` in the range; it is admittedly a weird name for something that can be greater than `start`, but the idea is that if you have a block of features with position `start`, then the lower bound is the first (lowest) of them. There is a similar position, the *upper bound* that is the smallest number greater than `start`. For any sorted sequence `x`, if `lb(a)` is the lower bound of a value `a` and `ub(a)` is the upper bound, then `x[lb(a):ub(a)]` contains all the positions with the value `a` (and it will be empty if `a` is not in `x`).

Lower and upper bounds are useful when you need to not only determine whether a value is in a set, but also identify where it is or with which associated features. You can compute both with binary search, so you can think of them as slightly more powerful generalisations of binary search.

We don't necessarily need the upper bound in this project, but in the file `src/bounds.py` I have put some code you can use to experiment with computing lower and upper bounds, and in `src/test_bounds.py` there are a few tests. You can use this to figure out how to adapt a binary search to a lower bound search, and once you have that, you can write code to find `pos_i` in a BED file using lower bound.

From `pos_i` we can scan forward, emitting every feature we see, until we reach a `pos_j >= end`. At that point we have left the region, and we can stop emitting. This isn't the only way to identify the region of features to emit, but it is a simple one, and it is as efficient as we can hope to make it (since we spend time O(z) to emit z features). You can also use an upper bound to figure out where to stop emitting (but it is not the upper bound of `start`); you can even use a lower bound. I'll leave it up to you to figure out how, but if everything else faisl, the strategy described above will work.

In the previous project, where the features weren't sorted, we would have to scan through the entire chromosome to get all the positions that fell within a desired region. If they are sorted, however, we can obviously stop emitting as soon as we reach a position that falls later than (or equal to) `end`, so we only need O(z) time to emit z features in a region.

Furthemore, to find `pos_i`, we can make use of binary search (in the form of a lower bound). If we scan the entire chromosome, as you would in the previous project, it takes time O(m) to find `pos_i` (where m is the number of features in the chromosome). With a binary search, instead, you would only need O(log m).

Once you have implemented a lower bound search for the start of the range, implement the query functionality in `src/query_bed.py`.


## Report

*Answer the questions below and then push this file to GitHub.*

*How do you use binary search to find the lower bound of a number? How did you have to modify the binary search algorithm?*

*Would anything be more difficult if the features covered ranges instead of single nucleotides (like real BED files)? What could go wrong, if anything?*

*We wrote a tool for merging two BED files, but what if we had a bunch of them? What would the complexity be if we merged them in, one at a time? What would the complexity be if we merged all of the files at the same time?*

