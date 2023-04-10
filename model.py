from pathlib import Path
import modal

import os


LOCAL_DBT_PROJECT = Path(__file__).parent / "src"
REMOTE_DBT_PROJECT = "/root/src"
CACHE_PATH = '/root/cache'


src_mount = modal.Mount.from_local_dir(
    LOCAL_DBT_PROJECT, remote_path=REMOTE_DBT_PROJECT
)

volume = modal.SharedVolume().persist(f'model_name-storage')
google_secrets = modal.Secret.from_name("google-storage-demos")


stub = modal.Stub('model_name', mounts=[src_mount], secrets=[google_secrets])
# image = modal.Image.debian_slim(python_version="3.10")
image = modal.Image.from_gcp_artifact_registry('us-central1-docker.pkg.dev/demos-375017/demo-images/test:latest', 
                                               secret=google_secrets)
stub.image = image


@stub.function(gpu="A10G",
                shared_volumes={CACHE_PATH: volume},
                secret=modal.Secret.from_name("google-storage-demos"))
def inference_modal(a, b):
    print(a+b)


@stub.local_entrypoint()
def main():
    inference_modal.call(1, 2)


