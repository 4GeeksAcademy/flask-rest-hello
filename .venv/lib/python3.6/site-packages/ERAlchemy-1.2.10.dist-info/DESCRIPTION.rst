Entity relation diagrams generator
==================================

|Join the chat at https://gitter.im/Alexis-benoist/eralchemy|

ERAlchemy generates Entity Relation (ER) diagram (like the one below)
from databases or from SQLAlchemy models.

Example
-------

.. figure:: https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/newsmeme.png?raw=true
   :alt: Example for NewsMeme

   Example for a graph

`Example for NewsMeme <https://bitbucket.org/danjac/newsmeme>`__

Quick Start
-----------

Install on a mac
~~~~~~~~~~~~~~~~

The simplest way to install eralchemy on OSX is by using
`Homebrew <http://brew.sh>`__

::

    $ brew install eralchemy

Install
~~~~~~~

To install ERAlchemy, just do:

::

    $ pip install eralchemy

``ERAlchemy`` requires
`GraphViz <http://www.graphviz.org/Download.php>`__ to generate the
graphs and Python. Both are available for Windows, Mac and Linux.

Usage from Command Line
~~~~~~~~~~~~~~~~~~~~~~~

From a database
^^^^^^^^^^^^^^^

::

    $ eralchemy -i sqlite:///relative/path/to/db.db -o erd_from_sqlite.pdf

The database is specified as a
`SQLAlchemy <http://docs.sqlalchemy.org/en/rel_1_0/core/engines.html#database-urls>`__
database url.

From a markdown file.
^^^^^^^^^^^^^^^^^^^^^

::

    $ curl 'https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/example/newsmeme.er' > markdown_file.er
    $ eralchemy -i 'markdown_file.er' -o erd_from_markdown_file.pdf

From a Postgresql DB to a markdown file excluding tables named ``temp`` and ``audit``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er --exclude-tables temp audit

From a Postgresql DB to a markdown file excluding columns named ``created_at`` and ``updated_at`` from all tables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -o filtered.er --exclude-columns created_at updated_at

From a Postgresql DB to a markdown file for the schema ``schema``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    $ eralchemy -i 'postgresql+psycopg2://username:password@hostname:5432/databasename' -s schema

Usage from Python
~~~~~~~~~~~~~~~~~

.. code:: python

    from eralchemy import render_er
    ## Draw from SQLAlchemy base
    render_er(Base, 'erd_from_sqlalchemy.png')

    ## Draw from database
    render_er("sqlite:///relative/path/to/db.db", 'erd_from_sqlite.png')

Architecture
------------

.. figure:: https://raw.githubusercontent.com/Alexis-benoist/eralchemy/master/eralchemy_architecture.png?raw=true
   :alt: Architecture schema

   Architecture schema

Thanks to it’s modular architecture, it can be connected to other
ORMs/ODMs/OGMs/O*Ms.

Contribute
----------

Every feedback is welcome on the `GitHub
issues <https://github.com/Alexis-benoist/eralchemy/issues>`__.

To run the tests, use : ``$ py.test``. Some tests require a local
postgres database with a schema named test in a database named test all
owned by a user named postgres with a password of postgres.

All tested PR are welcome.

Notes
-----

ERAlchemy was inspired by `erd <https://github.com/BurntSushi/erd>`__,
though it is able to render the ER diagram directly from the database
and not just only from the ``ER`` markup language.

Released under an Apache License 2.0

Creator: Alexis Benoist
`Alexis_Benoist <https://twitter.com/Alexis_Benoist>`__

.. |Join the chat at https://gitter.im/Alexis-benoist/eralchemy| image:: https://badges.gitter.im/Alexis-benoist/eralchemy.svg
   :target: https://gitter.im/Alexis-benoist/eralchemy?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


