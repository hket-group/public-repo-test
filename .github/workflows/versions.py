import os

full_repo = os.environ.get("REPOSITORY_NAME")
repo = os.environ.get("REPOSITORY_NAME")
version = os.environ.get("VERSION")

print("Get repo name:",repo)
print("Get version:", version)


# "s3://hket-terraform-private-registry/v1/providers/hashicorp/$REPOSITORY_NAME/$RELEASE_VERSION/release"
def main():
    for os_ in ["darwin","freebsd","linux","windows"]:
        archs = ["arm64","amd64","386","arm"] if os_ not in "darwin" else ["arm64","amd64"]
        for arch in archs:
            download_url = f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo}/release/{full_repo}_{version}_{os_}_{arch}.zip"
            filename = f"{full_repo}_{version}_{os_}_{arch}.zip"
            os = os_
            shasums_signature_url = f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo}/release/{full_repo}_{version}_SHA256SUMS.zip"
            shasums_url = f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo}/release/{full_repo}_{version}_SHA256SUMS"
            release_dict = {}
    pass

# if __name__ == "__main__":
#     main()