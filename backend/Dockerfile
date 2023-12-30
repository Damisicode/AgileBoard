# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

# Set working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Fix dependencies issues
RUN sed -i '1 s/from django.conf.urls import url/from django.urls import re_path as url/g' /usr/local/lib/python3.11/site-packages/rest_auth/urls.py
RUN sed -i '9 s/ugettext_lazy/gettext_lazy/g' /usr/local/lib/python3.11/site-packages/rest_auth/views.py 
RUN sed -i '6 s/ugettext_lazy/gettext_lazy/g' /usr/local/lib/python3.11/site-packages/rest_auth/serializers.py
RUN sed -i '7 s/force_text/force_str/g' /usr/local/lib/python3.11/site-packages/rest_auth/serializers.py
RUN sed -i '2 s/from django.conf.urls import url/from django.urls import re_path as url/g' /usr/local/lib/python3.11/site-packages/rest_auth/registration/urls.py
RUN sed -i '3 s/ugettext_lazy/gettext_lazy/g' /usr/local/lib/python3.11/site-packages/rest_auth/registration/views.py
RUN sed -i '2 s/ugettext_lazy/gettext_lazy/g' /usr/local/lib/python3.11/site-packages/rest_auth/registration/serializers.py

# Copy project code
COPY . /code/