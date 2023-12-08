<<<<<<< HEAD
# HSM-test
```
+-------------------------------------------------------------------+
|        Guest VM running  AMD SEV SEV-ES SEV-SNP                   |
|                                                                   |
| +-------------------+     +------------------------------------+  |
| | Python App        |     | .env.aes File                      |  |
| |                   |     | (Stored on Back store)             |  |
| | - Receives POS    |     | - POSTGRES_USER=...                |  |
| |   data via POST   |     | - POSTGRES_PASSWORD=...            |  |
| | - Encrypts data   |     | - SECRET_KEY=...                   |  |
| |   with HSM-       |     |                                    |  |
| |   derived key     |     |                                    |  |
| | - Pushes encrypted|     |                                    |  |
| |   data to database|     |                                    |  |
| | - Pushes encrypted|     |                                    |  |
| |   data to S3      |     +------------------------------------+  |
| |                   |                 |                           |
| | - Uses .env       |                 | Encrypted using           |
| |   variables       |                 | HSM-derived key           |
| +-------------------+                 |                           |
|                                       V                           |
| (startup.sh copies .env into App directory)                       |
+-------------------------------------------------------------------+
```
=======
`


`
>>>>>>> 2c55601 (fix .env variable as it was showing)
