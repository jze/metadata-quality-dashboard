# API Documentation

[View API Documentation (HTML)](../rest-api/templates/index.html)

| **Endpoint**                                  | **Description**                                                                              |
| --------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `/organisation-list`                          | Returns all available organisation identifiers.                                              |
| `/detailed-organisation-list`                 | Returns all organisations with multilingual display names, descriptions, and package counts. |
| `/organisation/<identifier>`                  | Full audit for a given organisation, including score breakdowns.                             |
| `/organisation/<identifier>/overview`         | Score summary across all five categories.                                                    |
| `/organisation/<identifier>/findability`      | Findability audit and score.                                                                 |
| `/organisation/<identifier>/accessibility`    | Accessibility audit and score.                                                               |
| `/organisation/<identifier>/reusability`      | Reusability audit and score.                                                                 |
| `/organisation/<identifier>/contextuality`    | Contextuality audit and score.                                                               |
| `/organisation/<identifier>/interoperability` | Interoperability audit and score.                                                            |
| `/status`                                     | Status of latest audit (OK/failure, date, version info).                                     |
| `/version`                                    | Current data-updater version and date of last update.                                        |
