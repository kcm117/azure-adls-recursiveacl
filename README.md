# azure-adls-recursiveacl
This is a python script to recursively set ADLS Gen2 ACLs for all subdirectories and files belonging to a target directory.  This is a temporary solution until setting ACLs recursively on the server side is available via the SDK or Azure Storage Explorer GUI client.

# Requirements:
- Python 3.7
- ADLS Gen2 Preview SDK (https://pypi.org/project/azure-storage-file-datalake/)

## Python 3.7 Virtual Environment Creation and Configuration (Windows)
    ```
    python.exe -m venv .venv
    .venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install azure-identity==1.1.0
    pip install azure-storage-file-datalake --pre
    ```

# Usage

## Authentication & Permissions:
- You will need:
    - Your Azure Active Directory Tenant ID.
    - An Azure Active Directory Service Principal (With Client ID and Client Secret).
    - **Storage Blob Data Owner** RBAC permissions granted to the service principal for your ADLS Gen2 storage account.
    - Three environment variables configured (as noted [here](https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity#service-principal-with-secret)):

        | ENV VAR NAME | VALUE |
        | ---------- | ---------- |
        | AZURE_CLIENT_ID | id of an Azure Active Directory application
        | AZURE_TENANT_ID | id of the application's Azure Active Directory tenant
        | AZURE_CLIENT_SECRET | one of the application's client secrets

## Set Desired Permissions

You can set desired permissions for the top-level, target directory in the Azure Storage Explorer GUI client by following the directions [here](https://docs.microsoft.com/en-us/azure/storage/blobs/data-lake-storage-how-to-set-permissions-storage-explorer).  Once you set permissions in the GUI, the idea is that you point the script to the top-level directory to make all child path ACLs match the parent directory ACLs.

## Running the Script

```
##### Syntax #####
python adls-acl.py <STORAGE_ACCT_NAME> <FILE_SYSTEM_NAME> <PATH>

# Subdirectory Example:
python adls-acl.py mystorageaccountname rawdata folder1/subfolder1/subfolder1-2

# Root directory in file system example:
python adls-acl.py mystorageaccountname rawdata folder1
```


# Possible Future Enhancements:
- Performance optimizations
- Add parameters for AAD friendly names or GUIDs to remove the need for Storage Explorer.

## References:
- SDK Announcement
    - https://azure.microsoft.com/en-us/blog/extended-filesystem-programming-capabilities-in-azure-data-lake-storage/
- SDK Preview Documentation (Python)
    - https://azuresdkdocs.blob.core.windows.net/$web/python/azure-storage-file-datalake/12.0.0b5/azure.storage.filedatalake.html
- Authentication (This script uses Default)
    - https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity#credentials
