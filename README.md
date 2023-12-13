# Hardware security module  application testing on AMD EPYC server Processor - Test
## Table of Contents
- [Badges](#badges)
- [Application Overview](#application-overview)
  - [Message Encryption and Storage](#message-encryption-and-storage)
  - [Secure Configuration Management](#secure-configuration-management)
- [Working Image](#working-image)
- [Use Case Illustration](#use-case-illustration)

![Testing](https://img.shields.io/badge/Testing-Workaround%20Done-green?logo=check-circle)
![HSM-Testing](https://img.shields.io/badge/HSM--Testing-Pass%20Done-green?logo=check-circle)
![Profiling](https://img.shields.io/badge/Profiling-Ongoing-yellow?logo=hourglass-half)
![Security](https://img.shields.io/badge/Security%20Done-yellow?logo=shield-alt)


## Application Functionality Overview
```
+-------------------------------------------------------------------+  
|        Guest VM running  AMD SEV SEV-ES SEV-SNP                   |
| It ensures that all computations are encrypted within vm using    |
|    SEV-ES  + Secure nested page (SEV-SNP)                         |
| +-------------------+     +------------------------------------+  |   
| | Python App        |     | .env.aes File                      |  | 
| |                   |     | (Stored on Back store)             |  | 
| | - Receives POS    |     | - POSTGRES_USER=...                |  | 
| |   data via POST   |     | - POSTGRES_PASSWORD=...            |  |  
| | - Encrypts data   |     | - SECRET_KEY=...                   |  |   
| |   with ASP-       |     |                                    |  |  
| |   derived key     |     |                                    |  |  
| | - Pushes encrypted|     |                                    |  |  
| |   data to database|     |                                    |  |   
| | - Pushes encrypted|     |                                    |  | 
| |   data to S3      |     +------------------------------------+  |   
| |                   |                 |                           |   
| | - Uses .env       |                 | Encrypted using           |  
| |   variables       |                 | ASP-derived key           | 
| +-------------------+                 |  256-bit CBC              |  
|                                       V                           |  
| (startup.sh copies .env into App directory)                       | 
+-------------------------------------------------------------------+
                                  |
                                  V 
The entire application is under the governance of a key derived from an ASP(AMD Secure Processor)

```

```
+---------------------------------+
|  AMD Secure Processor (AMD-SP)  |
|  - Manages encryption keys      |
|  - Integrated within the SOC    |
+---------------------------------+
         |
         | Encryption Key Management
         v
+-----------------------------------+
|  Memory Controller                |
|  - Located on the CPU die         |
|  - Includes AES Encryption Engine |
+-----------------------------------+
         |
         | Encryption/Decryption of Data
         v
+-----------------------------------+
|         DRAM                      |
|  - Data encrypted when written    |
|  - Data decrypted when read       |
+-----------------------------------+
         |
         | OS/Hypervisor Control (Page Tables)
         v
+-----------------------------------+
| OS or Hypervisor (HV)             |
|  - Controls encrypted pages       |
|  - Sets C-bit in page tables      |
+-----------------------------------+
Diagram assumption of flow of data and control in the memory encryption process 
```

```
+------------------------------------------+
|      AMD Secure Processor (AMD-SP)       |
|  - Manages encryption keys               |
|  - Integrated within the SOC             |
+------------------------------------------+
         |
         | Encryption Key Management
         v
+-----------------------------------------+
|        Memory Controller                |
|  - Located on the CPU die               |
|  - Includes AES Encryption Engine       |
+-----------------------------------------+
         |
         | Encryption/Decryption of Data
         v
+----------------------------------------+
|               DRAM                     |
|  - Data encrypted when written         |
|  - Data decrypted when read            |
+----------------------------------------+
         |
         | OS/Hypervisor Control
         v
+-----------------------------------------+
|   OS or Hypervisor (HV) with SEV-SNP    |
|  - Controls encrypted pages             |
|  - Manages VM isolation and integrity   |
|  - Utilizes Reverse Map Table (RMP)     |
+-----------------------------------------+
Diagram  assumption  Secure memory encryption + Secure Nested Paging (SEV-SNP)
```
- Our application offers robust encryption and decryption capabilities, tailored for secure message handling and configuration management. Here's how it works:

### Message Encryption and Storage:

- **Inbound Message Handling**: All incoming messages received via the POST method will be encrypted.
- **Secure Storage**: The encrypted messages are then securely stored in both our backend database and AWS S3 storage.
- **Message Decryption**: The GET method is used to decrypt stored messages, employing the ASP-derived key.
- **Retrieval and Decryption**: Encrypted messages stored in the database can be decrypted using the GET method.
- This decryption process utilizes a key derived from our Application Specific Processor (ASP), specifically the Versioned Chip Endorsement Key (VCEK).

  
### Secure Configuration Management:
- **.env.aes File Handling**: 
- The application also decrypts the encrypted .env.aes file (located in the backend store) when it's loaded into the application.
- In-Memory Processing: This decryption occurs in-memory (DRAM), using the same ASP-derived key.
- The entire operation of the app is governed by the unique key generated by the Versioned Chip Endorsement Key, ensuring high-level security and integrity of data handling processes.
### Working image
![Example Image](https://github.com/compute-labs/HSM-test/blob/a78d90fff4fad127f048661fe32c488f8be92f26/PoC.png)

```
sudo ./startup.sh
curl -X POST http://127.0.0.1/user/transaction \
    -F 'name=Danied' \
    -F 'email=Lucas@example.com' \
    -F 'amount=5000' \
    -F 'currency=USD' \
    -F 'description=Test transaction3'


curl -X GET http://localhost/user/transaction
curl -X GET http://127.0.0.1/user/transaction/dec
```
## Use case  Illustration
![Security Log Example](https://github.com/compute-labs/HSM-test/blob/master/Bots%26ScriptAttacks.png)
- Here on our AWS-hosted application in image is frequently targeted by bots and automated scripts searching for the .env file. However, due to our robust encryption, any sensitive information remains secure against unauthorized access. 
- To ensures the protection of sensitive credentials and data by employing 256-bit CBC (Cipher Block Chaining) encryption.
- ![Encrypted .env file ](https://github.com/compute-labs/HSM-test/blob/master/Encrypted.png)
- This security measure is particularly crucial in the event of a web server compromise or if the AWS security services are breached.
- If your data is deleted from AWS S3, neither AWS, any other storage service, nor an attacker with database access can read your sensitive data. This is because decrypting it without the encryption key would take thousands+  years 
