FROM python:3.10-alpine
WORKDIR /burndown
COPY main.py chart.py requirements.txt /burndown/
RUN apk add g++ make
RUN pip install -r /burndown/requirements.txt
RUN mkdir -m a=rwx /burndown/config
CMD ["python", "/burndown/main.py"]
