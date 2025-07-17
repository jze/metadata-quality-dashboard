# Environment Variables

## Data Updater
* **AUDIT_DEV**: Development mode toggle (`0` or `1`).  
  When set to `1`, the Data Updater uses predefined local output folders instead of the `SHARED` environment variable.
* **SHARED**: Output folder path used in production (e.g., inside a Docker container).  
  Defaults to `/shared/` if not set.
* **AUDIT_HTTP_PROXY**: Optional HTTP proxy address.
* **AUDIT_HTTPS_PROXY**: Optional HTTPS proxy address.

## REST API
* **AUDIT_HTTP_PROXY**: Optional HTTP proxy address.
* **AUDIT_HTTPS_PROXY**: Optional HTTPS proxy address.
