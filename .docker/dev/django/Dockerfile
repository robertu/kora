ARG PYTHON_VERSION=3.11.0-bullseye


# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=dev

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /wheels -r ${BUILD_ENVIRONMENT}.txt


# Python 'run' stage
FROM python as python-run-stage
ARG UID=1000
ARG GID=1000
ARG BUILD_ENVIRONMENT=dev
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels/

COPY ./.docker/dev/django/entrypoint /entrypoint

COPY ./.docker/dev/django/start-* /
# RUN chmod +x /start-*
RUN /usr/sbin/groupadd -g "${GID}" app  && /usr/sbin/useradd --create-home --no-log-init -u "${UID}" -g "${GID}" app
WORKDIR ${APP_HOME}
USER app
# copy application code to WORKDIR
# COPY . ${APP_HOME} # <-- not needed in dev env

ENTRYPOINT ["/entrypoint"]
