# Run Locally
This document explains how to run the **Data Updater** and **Rest API** locally for development purposes.

## Data Updater

1. Install the required Python packages:
   ```bash
   pip install --no-cache-dir -r data-updater/requirements.txt
   ```
   
2. Set the development mode environment variable:
   ```bash
   export AUDIT_DEV=1
   ```

    > Optionally, set proxy variables if needed:
    >
    > ```bash
    > export AUDIT_HTTP_PROXY=http://your-proxy:port
    > export AUDIT_HTTPS_PROXY=https://your-proxy:port
    > ```

3. Run the script
    ```bash
    python data-updater/main.py
    ```
    **OUTPUT:**
    ```bash
    11:31:36 INFO: [env] AUDIT_DEV: 1
    11:31:36 INFO: [env] SHARED: None
    11:31:36 INFO: [env] AUDIT_HTTP_PROXY: http://proxy-bvcol.admin.ch:8080
    11:31:36 INFO: [env] AUDIT_HTTPS_PROXY: http://proxy-bvcol.admin.ch:8080
    11:31:36 INFO: Output folder: C:\Users\U80875594\Documents\Code\Python\metadata-quality-audit\data-updater\data\output
    ```

4. Notice the data saved in `data-updater\data\output`.


## Rest API
1. Install the required Python packages:
   ```bash
   pip install --no-cache-dir -r rest-api/requirements.txt
   ```
   
2. (OPTINAL) Set proxy variables if needed:
    ```bash
    export AUDIT_HTTP_PROXY=http://your-proxy:port
    export AUDIT_HTTPS_PROXY=https://your-proxy:port
    ```

3. Run the script
    ```bash
    python rest-api/app.py
    ```
    **OUTPUT:**
    ```bash
    [env] INPUT_ORG_AUDIT: data\output\audit_organisation.json
    [env] INPUT_TOTAL_AUDIT: data\output\audit_total.json
    [env] AUDIT_HTTP_PROXY: http://proxy-bvcol.admin.ch:8080
    [env] AUDIT_HTTPS_PROXY: http://proxy-bvcol.admin.ch:8080
    * Serving Flask app "app" (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Restarting with watchdog (windowsapi)
    * Debugger is active!
    * Debugger PIN: 324-188-063
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ...
    ```

4. Open your preferred web browser and go to the address shown above, e.g.:    
    ```
    http://127.0.0.1:5000/
    ```
