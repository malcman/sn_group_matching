# sn_group_matching

Group Matching API for the [Support Network](https://www.umichwsn.org).

For deployment as a Google Cloud Function.

---

## The Support Network

The Support Network was founded in 2014 at the University of Michigan to improve student mental health and well-being through the implementation, development, and collaboration of peer support initiatives. Over the past 5 years, thousands of students have found supportive communities through the program, and today, there are growing chapters at several other schools across the country (high schools and colleges).


### Weekly Group Matching

Given sign-up data from students, we want to create a set of weekly meeting groups, subject to a number of constraints.

Currently, it takes days of trial and error to place all of the students manually. This results in suboptimal groups and takes valuable time away from the leadership team—at the expense of other preparation. We would like to find a better, more scalable way to  place students into groups.

We formulate this group matching as a mixed-integer programming problem, in which we maximize the number of placed students, subject to a number of group size and balance constraints.
