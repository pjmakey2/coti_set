#Packages
pip install --upgrade sqlalchemy \
    "pydantic[dotenv]" \
    fastapi \
    beautifulsoup4 \
    'dramatiq[rabbitmq, watch]' \
    urllib3 \
    ujson \
    uvicorn \
    alembic \
    psycopg2
sudo apt install rabbitmq-server