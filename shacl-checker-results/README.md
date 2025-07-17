# SHACL (Shapes Constraint Language) Checker Results

All metadata submitted to **opendata.swiss** is ultimately stored in a SQL database. During this process, the *original structure* of the incoming data — such as RDF or DCAT-AP — is flattened or lost.

As a result, our *Metadata Quality Audit* operates on the SQL-stored data, querying it after the fact. This means we can no longer validate metadata against its original schema using SHACL in a meaningful way.

Attempting to assign a **DCAT-AP compliance score** based on this transformed data would be misleading. It could distract data publishers from more impactful improvements and fail to reflect their actual metadata quality.

Instead, we run **internal SHACL-based tests** separately to identify potential issues and improvements. The results of those tests can be found in this folder.

Such improvements will most likely be implmented in the next version of the *Metadata Quality Audit* software.
