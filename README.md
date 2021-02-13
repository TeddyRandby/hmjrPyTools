# hmjr

hmjr is a package of tools to help researchers as well as users with simpler
needs directly interact with the HMJr diary collection.

## Prerequisites

- Python3
- Pip
- Thats it!

Alternatively, you can use Google Colab to load up a new PyNotebook, which will
automatically have everything you need. For the rest of this documentation, it
 will be assumed that you're using a Python Notebook.

## Getting started

To install our package and import what you need, run the following two lines.

    pip install hmjr
    from hmjr import Entries

`Entries` here is the first point of contact for interacting with the
 HMJR Diary database. In order to use it, we need to initialize the object.
Don't worry about what that means behind the scenes, just make sure to follow
 `Entries` up with a `()` whenver we use it, like this: `Entries()`

At this point, you may be seeing some suggestions popping up, especially
if you're using a Notebook. The best starting point here is `all()`, which
 just grabs entries in the simplest way possible, just the order they
 happen to be stored in the database.

So for now, we'll go with that.

    Entries().all().results

`.results` selects the data the query gave us out of the `Entries` object.
And after running that, you should see the data output!

Before we get to some new queries, lets go over some of the ways we can influence
 the queries we make. One way is with the default argument **max**. It refers to
 the maximum number of entries the query should ask for.
 This can be changed like this:

    Entries().all(max=5).results

This time we should see a lot fewer entries when we run the query.

The `all()` query has another default argument: **offset**. It offsets where the
 query starts picking entries out of the database.

    Entries().all(offset=200,max=5).results

Here we should see 5 new queries, from much later volumes in the diaries
 than we were looking at before.

Speaking of volumes - lets move on to a more complex query.

    Entries().withBookBetween(1,5).results

This query should be self explanatory, but it does have a quirk in that the
book range includes the lower bound, and excludes the upper bound. So this
query will return entries with books 1, 2, 3, 4.
