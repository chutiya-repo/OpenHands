ARG WSAI_CODE_BUILD_VERSION=dev
FROM node:25.2-trixie-slim AS frontend-builder

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend ./
RUN npm run build

FROM python:3.13.7-slim-trixie AS base
FROM base AS backend-builder

WORKDIR /app
ENV PYTHONPATH='/app'

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update -y \
    && apt-get install -y curl make git build-essential jq gettext \
    && python3 -m pip install poetry --break-system-packages

COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN export POETRY_CACHE_DIR && poetry install --no-root && rm -rf $POETRY_CACHE_DIR

FROM base AS wsai_code-app

WORKDIR /app

# re-declare for this section
ARG WSAI_CODE_BUILD_VERSION

ENV RUN_AS_WSAI_CODE=true
# A random number--we need this to be different from the user's UID on the host machine
ENV WSAI_CODE_USER_ID=42420
ENV SANDBOX_LOCAL_RUNTIME_URL=http://host.docker.internal
ENV USE_HOST_NETWORK=false
ENV WORKSPACE_BASE=/opt/workspace_base
ENV WSAI_CODE_BUILD_VERSION=$WSAI_CODE_BUILD_VERSION
ENV SANDBOX_USER_ID=0
ENV FILE_STORE=local
ENV FILE_STORE_PATH=/.wsai_code
ENV INIT_GIT_IN_EMPTY_WORKSPACE=1
RUN mkdir -p $FILE_STORE_PATH
RUN mkdir -p $WORKSPACE_BASE

RUN apt-get update -y \
    && apt-get install -y curl ssh sudo \
    && rm -rf /var/lib/apt/lists/*

# Default is 1000, but OSX is often 501
RUN sed -i 's/^UID_MIN.*/UID_MIN 499/' /etc/login.defs
# Default is 60000, but we've seen up to 200000
RUN sed -i 's/^UID_MAX.*/UID_MAX 1000000/' /etc/login.defs

RUN groupadd --gid $WSAI_CODE_USER_ID wsai_code
RUN useradd -l -m -u $WSAI_CODE_USER_ID --gid $WSAI_CODE_USER_ID -s /bin/bash wsai_code && \
    usermod -aG wsai_code wsai_code && \
    usermod -aG sudo wsai_code && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R wsai_code:wsai_code /app && chmod -R 770 /app
RUN sudo chown -R wsai_code:wsai_code $WORKSPACE_BASE && sudo chmod -R 770 $WORKSPACE_BASE
USER wsai_code

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH='/app'

COPY --chown=wsai_code:wsai_code --chmod=770 --from=backend-builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=wsai_code:wsai_code --chmod=770 ./skills ./skills
COPY --chown=wsai_code:wsai_code --chmod=770 ./wsai_code ./wsai_code
COPY --chown=wsai_code:wsai_code --chmod=777 ./wsai_code/runtime/plugins ./wsai_code/runtime/plugins
COPY --chown=wsai_code:wsai_code pyproject.toml poetry.lock README.md MANIFEST.in LICENSE ./

# This is run as "wsai_code" user, and will create __pycache__ with wsai_code:wsai_code ownership
RUN python wsai_code/core/download.py # No-op to download assets
# Add this line to set group ownership of all files/directories not already in "app" group
# wsai_code:wsai_code -> wsai_code:wsai_code
RUN find /app \! -group wsai_code -exec chgrp wsai_code {} +

COPY --chown=wsai_code:wsai_code --chmod=770 --from=frontend-builder /app/build ./frontend/build
COPY --chown=wsai_code:wsai_code --chmod=770 ./containers/app/entrypoint.sh /app/entrypoint.sh

USER root

WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["uvicorn", "wsai_code.server.listen:app", "--host", "0.0.0.0", "--port", "3000"]
