<<<<<<< HEAD
# HSM-test
```
+-------------------------------------------------------------------+  
|        Guest VM running  AMD SEV SEV-ES SEV-SNP                   |
| SEV-SNP ensures that all computations are encrypted within memory.|
|    + within virtual machine +                                     |
| +-------------------+     +------------------------------------+  |   
| | Python App        |     | .env.aes File                      |  | In my proof of concept i have made python application that securely processes data. 
| |                   |     | (Stored on Back store)             |  | This application receives Point of Sale (POS) transaction data, encrypts it with a key derived from (ASP).
| | - Receives POS    |     | - POSTGRES_USER=...                |  | then stores this encrypted data both in a database and on AWS S3 cloud storage. 
| |   data via POST   |     | - POSTGRES_PASSWORD=...            |  | A crucial element is our .env.aes and .env.db.aes file, which holds sensitive configuration data like user credentials
| | - Encrypts data   |     | - SECRET_KEY=...                   |  | This file is encrypted and stored securely on disk, and only decrypted by the application using the ASP-derived key in 
| |   with ASP-       |     |                                    |  | in-memory.
| |   derived key     |     |                                    |  | Which enhances server security by encrypting sensitive environment variables,
| | - Pushes encrypted|     |                                    |  | protecting against automated script attacks.
| |   data to database|     |                                    |  |  
| | - Pushes encrypted|     |                                    |  | Second, it provides enhanced data encryption for POS data, using a 256-bit CBC encryption method
| |   data to S3      |     +------------------------------------+  | This dual-layer protection makes our application, 'securevault,' highly resistant to data breaches
| |                   |                 |                           | and unauthorized access, especially suitable for financial applications
| | - Uses .env       |                 | Encrypted using           |  
| |   variables       |                 | ASP-derived key           | Let's demonstrate it.
| +-------------------+                 |  256-bit CBC              |  
|                                       V                           |  
| (startup.sh copies .env into App directory)                       | 
+-------------------------------------------------------------------+
                                  |
                                  V 
The entire application is under the governance of a key derived from an ASP(AMD Secure Processor)

```
=======
`


`
>>>>>>> 2c55601 (fix .env variable as it was showing)
