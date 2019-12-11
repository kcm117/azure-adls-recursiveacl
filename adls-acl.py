import asyncio
import sys
import time

from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient,FileSystemClient

def set_permission(path,acl):
    # Directories and files need to be handled differently
    if path.is_directory:
        directory_client = filesystem.get_directory_client(directory=path.name)
        resp = directory_client.set_access_control(acl=acl)
        # print(f'\tApplied Directory ACL to {path.name}')
    else:
        file_client = filesystem.get_file_client(path.name)
        # Need to remove "Default" ACL segments from ACL string because that can't be applied to files
        resp = file_client.set_access_control(acl=acl[:acl.find('default')-1])
        # print(f'\tApplied File ACL to {path.name}')
    return resp

async def main(target_dir,filesystem):
    loop = asyncio.get_running_loop()

    # Get the target directory, subdirectories and permissions
    paths = filesystem.get_paths(path=target_dir)
    directory_client = filesystem.get_directory_client(directory=target_dir)
    acl = directory_client.get_access_control()
    target_acl_dir = acl['acl']

    tasks = [
        loop.run_in_executor(None,set_permission,*(path,target_acl_dir)) for path in paths
        ]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Please use the following syntax to call the script:')
        print('\tadls-acl.py <STORAGE_ACCT_NAME> <FILE_SYSTEM_NAME> <PATH>')
        print('Example:')
        print('\tadls-acl.py mystorageaccountname rawdata folder1/subfolder1/subfolder1-2')
        sys.exit()
    else:
        ACCOUNT_NAME, FILE_SYSTEM, TARGET_DIR = sys.argv[1:]
    
    # Clients
    credential = DefaultAzureCredential()
    service = DataLakeServiceClient(account_url=f'https://{ACCOUNT_NAME}.dfs.core.windows.net/', credential=credential)
    filesystem = service.get_file_system_client(file_system=FILE_SYSTEM)

    print('*'*20)
    print(f'Storage Account Name: {ACCOUNT_NAME}')
    print(f'File System Name: {FILE_SYSTEM}')
    print('*'*20)
    print(f'Running: Setting ACLs for all child paths (subdirectories and files) in {TARGET_DIR} to match parent.')
    total_start = time.time() # Start Timing
    asyncio.run(main(TARGET_DIR,filesystem))
    total_end = time.time() # End Timing
    print("Complete: Recursive ACL configuration took {} seconds.".format(str(round(total_end - total_start,2))))