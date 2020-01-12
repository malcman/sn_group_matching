_WIP_

# sn_group_matching

Group Matching API for the [Support Network](https://www.umichwsn.org).

For deployment as a Google Cloud Function.


## The Support Network

The Support Network was founded in 2014 at the University of Michigan to improve student mental health and well-being through the implementation, development, and collaboration of peer support initiatives.

Over the past 5 years, thousands of students have found supportive communities through the program, and today, there are growing chapters at several other colleges and high schools across the country.


### Weekly Group Matching

A core part of the Support Network is the weekly meeting group, comprised of 6-10 student members and 2-3 trained student leaders. Over the course of a given semester/year, this serves as an accessible, inclusive, and confidential space where students feel comfortable sharing with each other.

At Michigan, several hundred students participate each semester. Currently it takes several days of trial and error to find a set of groups that works with students' availability. This results in suboptimal groups, and takes away valuable time from the leadership team—at the expense of other program preparation.

We would like to find a better, more scalable way to place students into groups.


### Optimization

We can formulate this group matching as a mixed-integer programming problem, in which we maximize the number of placed students, subject to constraints such as time, location, etc.
