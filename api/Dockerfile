FROM python:3.11-bookworm
WORKDIR /workspace

ENV PYTHONPATH /workspace:${PYTHONPATH}
ENV PATH /root/.local/bin:$PATH
ENV LD_LIBRARY_PATH /workspace/instantclient:${LD_LIBRARY_PATH}

RUN apt-get update && \
    apt-get upgrade -y && \ 
    apt-get install -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY gunicorn.cfg.py pyproject.toml ./

RUN curl -sSL https://install.python-poetry.org | python - && \
    poetry config virtualenvs.create false && \
    poetry install

COPY src/ src/

CMD ["gunicorn", "--config","gunicorn.cfg.py","src.main:app"]
