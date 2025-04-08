#/bin/bash
docker-compose run --rm api bash -c "python3 -m pip install safety && safety check $@"