FROM python:3

ENV PYTHONUNBUFFERED=1
RUN echo "source activate my_env" > ~/.bashrc

ENV PATH /opt/conda/envs/my_env/bin:$PATH

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./server.py" ]