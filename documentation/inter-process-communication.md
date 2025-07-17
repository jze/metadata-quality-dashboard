# Inter-process Communication

The `data-updater` and `rest-api` services communicate via a shared volume mounted at `/shared/`.

```
  [data-updater] ─── /shared/ ───▶ [rest-api]
        ▲                               |
        |                               ▼
   Downloads &                        Serves
   audits data                     API endpoint
```

Each component runs in its own container. This separation ensures that if the `data-updater` encounters an error, the API remains functional and continues to serve the most recent valid data.

A `status.json` file in the shared volume tracks the health and activity of the `data-updater`. It includes:
* Timestamps for the last run and last successful update
* The current operational state (`OK` or `ERROR`)
* The data version used

This status file can easily be accessed through the API.

**Endpoint:** ```[base-url]/status```:

**Example Response:**
```
{
  "status": "OK",
  "message": "",
  "last_update": "10.07.2025",
  "last_update_ok": "10.07.2025",
  "version": 0.7,
  "version_last_update": "13.03.2025"
}
```