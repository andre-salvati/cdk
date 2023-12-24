## AWS CDK Demo with RDS, Redshift, Data Migration Service (DMS), and SCT (Schema Conversion Tool)

This CDK script:

- creates an RDS (SQL Server) instance and a Redshift cluster
- allows connections from the Internet to RDS and Redshift through a database management tool like [DBeaver](https://dbeaver.io/). Caution: RDS and Redshift are deployed on a public subnet, this is just for test purposes, it is not the best architecture for production environments.
- configures a DMS instance with RDS and Redshift endpoints, and a migration task.

After stack creation, you can manually:

- load data on the RDS database.
- convert schemas from RDS to Redshift. Please, refer to [Schema Conversion Tool installation](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html).
- start the migration task on DMS.

## Architecture

<img src="diagram.png" width="800">
