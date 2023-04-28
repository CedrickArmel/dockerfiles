package(default_visibility = ["//visibility:public"])

licenses(["unencumbered"])

py_binary(
    name = "query_license",
    srcs = [
        "query_license.py",
    ],
    deps = [
        "//third_party/py/google/cloud/datastore",
    ],
)

py_test(
    name = "query_license_test",
    size = "small",
    srcs = ["query_license_test.py"],
    deps = [
        ":query_license",
        "//cloud/ml/dset/dlenv/build/package/common:db_constants",
        "//testing/pybase",
        "//third_party/py/google/cloud/datastore",
    ],
)
