def app(environ, start_response):
    data = b"Hello, World!\n"
    start_response(
        "200 OK",
        [("Content-Type", "text/plain"), ("Content-Length", str(len(data)))],
    )
    return [data]


# gunicorn -w 4 example:app
