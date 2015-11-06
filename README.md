# quasardb Python API

## Installation

### quasardb C API

To build the Python API, you will need the C API. It can either be installed on the machine (e.g. on unix in /usr/lib or /usr/local/lib) or you can unpack the C API archive in qdb.

### Building the extension

You will need [CMake](http://www.cmake.org/), [SWIG](http://www.swig.org/) and the Python dist tools installed. You can also download a pre-compiled package from our download site.

First, run cmake to create a project directory, for example:

```
    mkdir build
    cd build
    cmake -G "your generator" ..
```

Depending on the generator you chose, you will then either have to run make or open the solution with your editor (e.g. Visual Studio).

For example on UNIX:

```
    mkdir build
    cd build
    cmake -G "Unix Makefiles" ..
    make
```

## Usage

Using *quasardb* starts with a Cluster:

```python
    import qdb

    c = qdb.Cluster('qdb://127.0.0.1:2836')
```

Now that we have a connection to the cluster, let's store some binary data:

```python
    b = c.blob('bam')

    b.put('boom')
    v = b.get() # returns 'boom'
```

Want a queue? We have distributed queues.

```python
    q = c.queue('q2')

    q.push_back('boom')
    v = q.pop_front() # returns 'boom'

    q.push_front('bang')
```

quasardb comes out of the box with server-side atomic integers:

```python
    i = c.integer('some_int')

    i.put(3)  # i is equal to 3
    i.add(7)  # i is equal to 10
    i.add(-5) # is equal to 5
```

We also provide distributed hash sets:

```python
    hset = c.hset('the_set')

    hset.insert('boom')

    hset.contains('boom') # True
```