# pylint: disable=C0103,C0111,C0302,W0212
import pytest
import quasardb.pandas as qdbpd
from functools import reduce
import numpy as np
import pandas as pd
import test_ts_batch as batchlib

def test_can_read_series(qdbd_connection, table, many_intervals):
    batch_inserter = qdbd_connection.ts_batch(
        batchlib._make_ts_batch_info(table))

    doubles, blobs, integers, timestamps = batchlib._test_with_table(
        batch_inserter,
        table,
        many_intervals,
        batchlib._row_insertion_method,
        batchlib._regular_push)

    total_range = (many_intervals[0], many_intervals[-1] + np.timedelta64(1, 's'))
    double_series = qdbpd.as_series(table, "the_double", [total_range])
    blob_series = qdbpd.as_series(table, "the_blob", [total_range])
    int64_series = qdbpd.as_series(table, "the_int64", [total_range])
    ts_series = qdbpd.as_series(table, "the_ts", [total_range])

    assert type(double_series) == pd.core.series.Series
    assert type(blob_series) == pd.core.series.Series
    assert type(int64_series) == pd.core.series.Series
    assert type(ts_series) == pd.core.series.Series

    np.testing.assert_array_equal(double_series.to_numpy(), doubles)
    np.testing.assert_array_equal(blob_series.to_numpy(), blobs)
    np.testing.assert_array_equal(int64_series.to_numpy(), integers)
    np.testing.assert_array_equal(ts_series.to_numpy(), timestamps)

def test_dataframe(qdbd_connection, table, many_intervals):
    batch_inserter = qdbd_connection.ts_batch(
        batchlib._make_ts_batch_info(table))

    doubles, blobs, integers, timestamps = batchlib._test_with_table(
        batch_inserter,
        table,
        many_intervals,
        batchlib._row_insertion_method,
        batchlib._regular_push)

    df = qdbpd.as_dataframe(table)

    np.testing.assert_array_equal(df['the_double'].to_numpy(), doubles)
    np.testing.assert_array_equal(df['the_blob'].to_numpy(), blobs)
    np.testing.assert_array_equal(df['the_int64'].to_numpy(), integers)
    np.testing.assert_array_equal(df['the_ts'].to_numpy(), timestamps)

def test_dataframe_can_read_columns(qdbd_connection, table, many_intervals):
    batch_inserter = qdbd_connection.ts_batch(
        batchlib._make_ts_batch_info(table))

    doubles, blobs, integers, timestamps = batchlib._test_with_table(
        batch_inserter,
        table,
        many_intervals,
        batchlib._row_insertion_method,
        batchlib._regular_push)

    df = qdbpd.as_dataframe(table, columns=['the_double', 'the_int64'])

    np.testing.assert_array_equal(df['the_double'].to_numpy(), doubles)
    np.testing.assert_array_equal(df['the_int64'].to_numpy(), integers)

def test_dataframe_can_read_ranges(qdbd_connection, table, many_intervals):
    batch_inserter = qdbd_connection.ts_batch(
        batchlib._make_ts_batch_info(table))

    doubles, blobs, integers, timestamps = batchlib._test_with_table(
        batch_inserter,
        table,
        many_intervals,
        batchlib._row_insertion_method,
        batchlib._regular_push)

    first_range = (many_intervals[0], many_intervals[1])
    second_range = (many_intervals[1], many_intervals[2])

    df1 = qdbpd.as_dataframe(table, ranges=[first_range])
    df2 = qdbpd.as_dataframe(table, ranges=[first_range, second_range])

    assert df1.shape[0] == 1
    assert df2.shape[0] == 2

def test_dataframe_can_use_alternative_index(qdbd_connection, table, many_intervals):
    batch_inserter = qdbd_connection.ts_batch(
        batchlib._make_ts_batch_info(table))

    doubles, blobs, integers, timestamps = batchlib._test_with_table(
        batch_inserter,
        table,
        many_intervals,
        batchlib._row_insertion_method,
        batchlib._regular_push)

    df1 = qdbpd.as_dataframe(table)
    df2 = qdbpd.as_dataframe(table, index='the_int64')

    assert (type(df1.index)) == pd.core.indexes.datetimes.DatetimeIndex
    assert (type(df2.index)) == pd.core.indexes.numeric.Int64Index
