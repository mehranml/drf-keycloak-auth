#/bin/bash
docker-compose run --rm test bash -c "python3 -m pip install safety && safety check $@"