## Snapshots:

### Steps to take a snapshot:
#### Preparations:
- Add `"path.repo=/mnt/backup"` to environment of elastic nodes.
- Add `esbackup:/mnt/backup` to volumes.
- Define esbackup as a volume `esbackup: driver: local`.

#### Snapshot Config:
- URL: http://localhost:9200/_snapshot/my_fs_backup
- METHOD: PUT
- BODY: {"type": "fs", "settings": {"location": "backup1", "compress": true}}

#### Taking Snapshot:
- URL: http://localhost:9200/_snapshot/my_fs_backup/snapshot_2?wait_for_completion=true
- METHOD: PUT

#### Troubleshooting:
- If taking the snapshot fails, attach to the container, run `chown -R elasticsearch /mnt/backup`
- This will allow elasticsearch access to `/mnt/backup` and thus the backup will be saved there and thus it will 
reflect at the mapped esbackup folder present in var/docker/volumes

