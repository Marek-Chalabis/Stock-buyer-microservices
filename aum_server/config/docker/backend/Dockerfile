FROM python:3.9-buster

ARG APP_STATUS
ARG USER_ID
ARG USER=app

ENV USER_ID=${USER_ID} \
  POETRY_VERISON=${POETRY_VERISON} \
  HOME=/home/${USER} \
  PYTHONUNBUFFERED=1 \
  POETRY_CACHE_DIR=/var/cache/pypoetry


RUN apt-get update -qq \
  && apt-get install -qq -y \
  && apt-get clean -qq -y \
  && pip install --upgrade pip \
  && pip install poetry \
  && rm -rf /var/lib/apt/lists/*

# started path for conteiner
WORKDIR /app/

# copy python-poetry dependency
COPY ./backend/poetry.lock ./backend/pyproject.toml /app/

# install packages dependency from poetry
# force `virtualenvs.create false` in case user update it in `pyproject.toml`
# also remove cache if production status
RUN cd /app && poetry config virtualenvs.create false \
  && poetry install \
    $(if [ "$APP_STATUS" = 'production' ]; then echo '--no-dev'; fi) \
    --no-interaction \
    --no-ansi \
  && if [ "$APP_STATUS" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

# copy code
COPY ./backend/ /app/

# sets and create user and group to run the application and adjust permissions
RUN addgroup --system --gid ${USER_ID} ${USER} \
  && adduser --system --home ${HOME} --uid ${USER_ID} --ingroup ${USER} ${USER}
RUN chown -R ${USER} /app /home/${USER}
RUN chmod -R 755 /app

USER ${USER}
