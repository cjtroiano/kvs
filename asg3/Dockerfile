FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt requests==2.10.0
EXPOSE 12345
EXPOSE 12346
EXPOSE 12347
EXPOSE 12348
EXPOSE 12349
ENTRYPOINT ["python"]
CMD ["hello.py"]