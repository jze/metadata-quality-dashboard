#  Metadata Quality Audit
Ensuring high-quality metadata across the entire Swiss Confederation administration.


## Description
The **Metadata Quality Audit** is the backend system which drives the [Metadata Quality Dashboard](https://dashboard.opendata.swiss/), supporting metadata excellence across all levels of the Swiss public sector—federal administration, cantons, and communes alike.

This repository is divided into two systems:
* **Data Loader** – A data pipeline that retrieves metadata from [opendata.swiss](https://opendata.swiss/en), audits it, and computes quality scores.
* **REST API** – A flexible and structured interface to expose audit results for integration with dashboards and visual tools.

The system was developed to address inconsistencies in open data metadata and enable quality monitoring at scale. It supports Switzerland's commitment to high-quality [Open Government Data (OGD)](https://www.bfs.admin.ch/bfs/en/home/services/ogd.html), in alignment with the [FAIR principles](https://www.go-fair.org/fair-principles/) and the [Metadata Quality Assessment (MQA)](https://data.europa.eu/mqa/methodology?locale=en) by data.europa.eu.

### Key Features
* Standards-based metadata auditing (FAIR, MQA)
* Automated scoring and tracking over time
* RESTful API for flexible data consumption
* Powers the official public-facing dashboard


## Further Documentation
* [Project Structure](./documentation/project-structure.md)
* [Deployment](./documentation/deployment.md)
* [Inter-Process Communication](./documentation/inter-process-communication.md)

## Technologies
* Python 3.9.7 – For packages, read the per-project requirements.txt files
* Docker – Used to containerize and isolate each sub-project
* Git + Bitbucket – Source control and hosting

> The code is published on GitHub for public access.
Internally, development is managed on a private Bitbucket server, though an “open by default” policy is under consideration as part of FSO’s ongoing transparency efforts.

## License
This project is licensed under the MIT terms. See the [LICENSE](LICENSE) file in this repository for full details.


## Author and Acknowledgements
All code in this repository was developed by **Florian Emmanuel Fasmeyer**.

Special thanks to **Vu Kim Lan** and **Maik Roth** from the **OGD team** for initiating and supporting the project as part of the **Masterplan OGD 2024–2027**.

Appreciation goes to the **PUB/WEB team**—including **Thomas-Christian Schwander**—for building the Metadata Quality Dashboard using data provided by the API developed in this project. Additional thanks to the **PUB/VIZ team**, including **Max Henking**, **Ludivine Stofer**, and **Nicolas Ruetschi**, who created visualizations based on this data.
