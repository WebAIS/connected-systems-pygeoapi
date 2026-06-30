# connected-systems-pygeoapi

Proof of Concept of the OGC API Connected Systems based on pygeoapi.

The implementation is split across two backends:

- **Part 1** (systems, deployments, procedures, ...) is served from **Elasticsearch**.
- **Part 2** (datastreams, observations, ...) is served from **TimescaleDB**.

## Local Development

For local development the supporting backends run in Docker while the application itself runs
on the host, so it can be debugged directly.

### 1. Start the backends

```commandline
cp .env.sample .env
docker compose -f docker-compose-dev.yml up -d
```

This brings up the supporting services and forwards their ports to the host:

| Service       | Port   |
| ------------- | ------ |
| TimescaleDB   | `5433` |
| Elasticsearch | `9200` |
| Kibana        | `5601` |
| pgAdmin       | `5050` |

The application container is intentionally commented out in `docker-compose-dev.yml` so it can
be run and debugged on the host (see below).

### 2. Install Python dependencies

Dependencies are managed with [`uv`](https://docs.astral.sh/uv/). Python is pinned to `3.12.12`
via `.python-version`.

```commandline
uv sync
```

### 3. Run the application

```commandline
uv run connected-systems-api/app.py
```

This starts a debug server on `http://localhost:5000` with basic-auth test credentials
(`test` / `test`).

### Configuration

Defaults are read from [`connected-systems-api/default-config.yml`](connected-systems-api/default-config.yml)
and can be overridden with `CSA_*` environment variables. The backend defaults from
`docker-compose-dev.yml` (hosts, ports, passwords) already match the default config, so no extra
configuration is required for a standard local setup.

## Docker

Build the production image:

```commandline
docker build -t connected-systems-pygeoapi .
```

The container serves the API via [`hypercorn`](hypercorn.conf.py) on port `5000`.

## Example Data

You can insert example data into a running instance using the
[simulator](./tools/simulator/simulator.py). Set up a separate Python environment for it and
install its [dependencies](./tools/simulator/requirements.txt). The number of observations to
insert (`num_of_obs_to_insert`) can be adjusted inside `simulator.py`.

## Usage

The API is accessible at `<host>:5000` and provides an HTML landing page for easy navigation.

## License

The software is licensed under the `Apache 2.0 License`. See [LICENSE](LICENSE) for details.

## Contributors
