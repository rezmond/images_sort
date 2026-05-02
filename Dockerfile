FROM python:3.10-slim

WORKDIR /workspace

RUN groupadd -g 1000 devuser || true \
    && useradd -m -u 1000 -g 1000 devuser || true

RUN python -m pip install --upgrade pip setuptools wheel

COPY requirements.txt /workspace/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PATH="/home/devuser/.local/bin:${PATH}"

CMD ["bash"]
