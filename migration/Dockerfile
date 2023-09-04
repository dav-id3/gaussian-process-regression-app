FROM python:3.11.0-bullseye
WORKDIR /workspace

ENV TZ 'Asia/Tokyo'
ENV PYTHONPATH /workspace:${PYTHONPATH}
ENV PATH /root/.local/bin:$PATH
ENV LD_LIBRARY_PATH /workspace/instantclient:${LD_LIBRARY_PATH}

COPY alembic.ini pyproject.toml poetry.lock ./

RUN pip install --upgrade pip

RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false && \
    poetry install

CMD ["bin/ash"]
