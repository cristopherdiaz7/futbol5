# Helper to build and run docker compose for futbol5
param(
    [switch]$Build
)

if ($Build) {
    docker compose build
}

docker compose up
