window.BENCHMARK_DATA = {
  "lastUpdate": 1623274896817,
  "repoUrl": "https://github.com/UCL-CCS/EasyVVUQ",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "unaudio@gmail.com",
            "name": "Vytautas Jancauskas",
            "username": "orbitfold"
          },
          "committer": {
            "email": "unaudio@gmail.com",
            "name": "Vytautas Jancauskas",
            "username": "orbitfold"
          },
          "distinct": true,
          "id": "4b7b2bc211223e5ea0e31bde35e7504dc091a4e0",
          "message": "remove restartable_campaign_tutorial.rst",
          "timestamp": "2021-06-09T17:23:24+02:00",
          "tree_id": "a26a0d511462a07338e61526847cc854861b3be0",
          "url": "https://github.com/UCL-CCS/EasyVVUQ/commit/4b7b2bc211223e5ea0e31bde35e7504dc091a4e0"
        },
        "date": 1623252632029,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_db_benchmark.py::test_draw",
            "value": 0.07506642935430319,
            "unit": "iter/sec",
            "range": "stddev: 0.09353045095964799",
            "extra": "mean: 13.321534121200012 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_store_results",
            "value": 0.08806415454707352,
            "unit": "iter/sec",
            "range": "stddev: 0.09689396430580743",
            "extra": "mean: 11.355357978999995 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_get_collation_result",
            "value": 89.47276781398557,
            "unit": "iter/sec",
            "range": "stddev: 0.00024177134303478935",
            "extra": "mean: 11.176585059702257 msec\nrounds: 67"
          },
          {
            "name": "tests/test_db_benchmark.py::test_draw_add",
            "value": 0.07487460449251762,
            "unit": "iter/sec",
            "range": "stddev: 0.15948948211257938",
            "extra": "mean: 13.355663202200049 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_store_results_add",
            "value": 0.08807804985753805,
            "unit": "iter/sec",
            "range": "stddev: 0.09205692923449443",
            "extra": "mean: 11.353566542600015 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_get_collation_result_add",
            "value": 47.69482756959306,
            "unit": "iter/sec",
            "range": "stddev: 0.0003414148087468053",
            "extra": "mean: 20.96663413953783 msec\nrounds: 43"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "email": "unaudio@gmail.com",
            "name": "Vytautas Jancauskas",
            "username": "orbitfold"
          },
          "committer": {
            "email": "unaudio@gmail.com",
            "name": "Vytautas Jancauskas",
            "username": "orbitfold"
          },
          "distinct": true,
          "id": "8e2f14c7e5ba4b8a24af283c455bd7dfce4bc127",
          "message": "fix inconsistencies in basic_tutorial",
          "timestamp": "2021-06-09T17:22:00+02:00",
          "tree_id": "011aee1a79fe61def2d888480c6050eef6ee6c3e",
          "url": "https://github.com/UCL-CCS/EasyVVUQ/commit/8e2f14c7e5ba4b8a24af283c455bd7dfce4bc127"
        },
        "date": 1623252649919,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_db_benchmark.py::test_draw",
            "value": 0.05527478900106718,
            "unit": "iter/sec",
            "range": "stddev: 0.13039862937802407",
            "extra": "mean: 18.0914304346 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_store_results",
            "value": 0.07527690059378288,
            "unit": "iter/sec",
            "range": "stddev: 0.09768853755483912",
            "extra": "mean: 13.284287638199999 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_get_collation_result",
            "value": 82.30924947318333,
            "unit": "iter/sec",
            "range": "stddev: 0.0009769472124703466",
            "extra": "mean: 12.149302859647673 msec\nrounds: 57"
          },
          {
            "name": "tests/test_db_benchmark.py::test_draw_add",
            "value": 0.054939378107413436,
            "unit": "iter/sec",
            "range": "stddev: 0.1662708037499188",
            "extra": "mean: 18.20188059000001 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_store_results_add",
            "value": 0.07444450060185197,
            "unit": "iter/sec",
            "range": "stddev: 0.28066285502326804",
            "extra": "mean: 13.432825687800005 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_get_collation_result_add",
            "value": 41.67381333495836,
            "unit": "iter/sec",
            "range": "stddev: 0.0021977818222307585",
            "extra": "mean: 23.995884225001873 msec\nrounds: 40"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "UCL-CCS",
            "username": "UCL-CCS"
          },
          "committer": {
            "name": "UCL-CCS",
            "username": "UCL-CCS"
          },
          "id": "74a98d8fd59e94d5a08142f86f367fbe6f7a1556",
          "message": "Integration with QCG-PJ",
          "timestamp": "2021-06-09T15:23:31Z",
          "url": "https://github.com/UCL-CCS/EasyVVUQ/pull/343/commits/74a98d8fd59e94d5a08142f86f367fbe6f7a1556"
        },
        "date": 1623274895545,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/test_db_benchmark.py::test_draw",
            "value": 0.07454401997566197,
            "unit": "iter/sec",
            "range": "stddev: 0.11961936120367005",
            "extra": "mean: 13.414892305599995 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_store_results",
            "value": 0.0903406993490119,
            "unit": "iter/sec",
            "range": "stddev: 0.07017456802439143",
            "extra": "mean: 11.069208089000005 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_get_collation_result",
            "value": 85.87786091992461,
            "unit": "iter/sec",
            "range": "stddev: 0.000601660071142638",
            "extra": "mean: 11.64444467163002 msec\nrounds: 67"
          },
          {
            "name": "tests/test_db_benchmark.py::test_draw_add",
            "value": 0.07494976017442623,
            "unit": "iter/sec",
            "range": "stddev: 0.08898386212886493",
            "extra": "mean: 13.342270844800009 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_store_results_add",
            "value": 0.08936281104082082,
            "unit": "iter/sec",
            "range": "stddev: 0.07316030280839685",
            "extra": "mean: 11.190337326600002 sec\nrounds: 5"
          },
          {
            "name": "tests/test_db_benchmark.py::test_get_collation_result_add",
            "value": 42.85481675890026,
            "unit": "iter/sec",
            "range": "stddev: 0.0004075743046942899",
            "extra": "mean: 23.334599833338824 msec\nrounds: 42"
          }
        ]
      }
    ]
  }
}