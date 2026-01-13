# Daytona Runtime

[Daytona](https://www.daytona.io/) is a platform that provides a secure and elastic infrastructure for running AI-generated code. It provides all the necessary features for an AI Agent to interact with a codebase. It provides a Daytona SDK with official Python and TypeScript interfaces for interacting with Daytona, enabling you to programmatically manage development environments and execute code.

## Quick Start

### Step 1: Retrieve Your Daytona API Key
1. Visit the [Daytona Dashboard](https://app.daytona.io/dashboard/keys).
2. Click **"Create Key"**.
3. Enter a name for your key and confirm the creation.
4. Once the key is generated, copy it.

### Step 2: Set Your API Key as an Environment Variable
Run the following command in your terminal, replacing `<your-api-key>` with the actual key you copied:

Mac/Linux:
```bash
export DAYTONA_API_KEY="<your-api-key>"
```

Windows PowerShell:
```powershell
$env:DAYTONA_API_KEY="<your-api-key>"
```

This step ensures that WSAI CODE can authenticate with the Daytona platform when it runs.

### Step 3: Run WSAI CODE Locally Using Docker
To start the latest version of WSAI CODE on your machine, execute the following command in your terminal:

Mac/Linux:
```bash
bash -i <(curl -sL https://get.daytona.io/wsaicode)
```

Windows:
```powershell
powershell -Command "irm https://get.daytona.io/wsaicode-windows | iex"
```

#### What This Command Does:
- Downloads the latest WSAI CODE release script.
- Runs the script in an interactive Bash session.
- Automatically pulls and runs the WSAI CODE container using Docker.
Once executed, WSAI CODE should be running locally and ready for use.


## Manual Initialization

### Step 1: Set the `WSAI_CODE_VERSION` Environment Variable
Run the following command in your terminal, replacing `<wsaicode-release>` with the latest release's version seen in the [main README.md file](https://github.com/wsaicode/wsaicode?tab=readme-ov-file#-quick-start):

#### Mac/Linux:
```bash
export WSAI_CODE_VERSION="<wsaicode-release>"  # e.g. 0.27
```

#### Windows PowerShell:
```powershell
$env:WSAI_CODE_VERSION="<wsaicode-release>"  # e.g. 0.27
```

### Step 2: Retrieve Your Daytona API Key
1. Visit the [Daytona Dashboard](https://app.daytona.io/dashboard/keys).
2. Click **"Create Key"**.
3. Enter a name for your key and confirm the creation.
4. Once the key is generated, copy it.

### Step 3: Set Your API Key as an Environment Variable:
Run the following command in your terminal, replacing `<your-api-key>` with the actual key you copied:

#### Mac/Linux:
```bash
export DAYTONA_API_KEY="<your-api-key>"
```

#### Windows PowerShell:
```powershell
$env:DAYTONA_API_KEY="<your-api-key>"
```

### Step 4: Run the following `docker` command:
This command pulls and runs the WSAI CODE container using Docker. Once executed, WSAI CODE should be running locally and ready for use.

#### Mac/Linux:
```bash
docker run -it --rm --pull=always \
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.wsaicode.dev/wsaicode/runtime:${WSAI_CODE_VERSION}-nikolaik \
    -e LOG_ALL_EVENTS=true \
    -e RUNTIME=daytona \
    -e DAYTONA_API_KEY=${DAYTONA_API_KEY} \
    -v ~/.wsaicode:/.wsaicode \
    -p 3000:3000 \
    --name wsaicode-app \
    docker.wsaicode.dev/wsaicode/wsaicode:${WSAI_CODE_VERSION}
```

> **Note**: If you used WSAI CODE before version 0.44, you may want to run `mv ~/.wsaicode-state ~/.wsaicode` to migrate your conversation history to the new location.

#### Windows:
```powershell
docker run -it --rm --pull=always `
    -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.wsaicode.dev/wsaicode/runtime:${env:WSAI_CODE_VERSION}-nikolaik `
    -e LOG_ALL_EVENTS=true `
    -e RUNTIME=daytona `
    -e DAYTONA_API_KEY=${env:DAYTONA_API_KEY} `
    -v ~/.wsaicode:/.wsaicode `
    -p 3000:3000 `
    --name wsaicode-app `
    docker.wsaicode.dev/wsaicode/wsaicode:${env:WSAI_CODE_VERSION}
```

> **Note**: If you used WSAI CODE before version 0.44, you may want to run `mv ~/.wsaicode-state ~/.wsaicode` to migrate your conversation history to the new location.

> **Tip:** If you don't want your sandboxes to default to the EU region, you can set the `DAYTONA_TARGET` environment variable to `us`

### Running WSAI CODE Locally Without Docker

Alternatively, if you want to run the WSAI CODE app on your local machine using `make run` without Docker, make sure to set the following environment variables first:

#### Mac/Linux:
```bash
export RUNTIME="daytona"
export DAYTONA_API_KEY="<your-api-key>"
```

#### Windows PowerShell:
```powershell
$env:RUNTIME="daytona"
$env:DAYTONA_API_KEY="<your-api-key>"
```

## Documentation
Read more by visiting our [documentation](https://www.daytona.io/docs/) page.
