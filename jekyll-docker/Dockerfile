# Dockerfile for jekyll
FROM ruby:2.7

RUN apt-get update && apt-get install -y nodejs npm python3-pip && rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install jupyter nbconvert
RUN gem update --system
RUN gem install bundler jekyll

WORKDIR /srv/jekyll

EXPOSE 4000

CMD ["jekyll", "serve", "--force_polling", "-H", "0.0.0.0"]
