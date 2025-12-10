# test_run.py
try:
    import flask, requests, bs4, urllib3
    print("Imports OK")
except Exception as e:
    print("Import error:", e)
