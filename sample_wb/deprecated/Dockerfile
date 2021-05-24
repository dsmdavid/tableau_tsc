FROM python:3.8.2-buster

RUN apt-get update -yqq \
  && apt-get install -yqq \
    vim 

# upgrade pip
RUN pip install --upgrade pip

RUN echo 'alias ll="ls -lari"' >> ~/.bashrc

# Install dependencies:
COPY ./ /app/
RUN chmod 777 -R /app
WORKDIR /app
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
