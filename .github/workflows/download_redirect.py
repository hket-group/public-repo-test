import os
import json
import subprocess

# repository_name = os.environ.get("REPOSITORY_NAME")
# repo_short = os.environ.get("REPOSITORY_NAME").removeprefix("terraform-provider-")
# release_version = os.environ.get("VERSION")
# fingerprint = os.environ.get("GPG_FINGERPRINT")

# s3_bucket_name = "hket-terraform-private-registry"

s3_bucket_name = "hket-custom-terraform-providers"
repository_name = "terraform-provider-hket-ad"
repo_short = "hket-ad"
release_version = "0.6.0"
fingerprint = "asdbbb"

# print("Get repo name:",repository_name)
# print("Get version:", release_version)
# print("Get fingerprint:", fingerprint)
# print("remove prefix",repository_name.removeprefix("terraform-provider-"))

def main():
    for os_ in ["darwin","freebsd","linux","windows"]:
        archs = ["arm64","amd64","386","arm"] if os_ not in "darwin" else ["arm64","amd64"]
        for arch in archs:
            release_dict = {
                "arch": arch,
                "download_url": f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo_short}/release/{repository_name}_{release_version}_{os_}_{arch}.zip",
                "filename": f"{repository_name}_{release_version}_{os_}_{arch}.zip",
                "os": os_,
                "protocols": [
                    "5.0"
                ],
                "shasum": fingerprint,
                "shasums_signature_url": f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo_short}/release/{repository_name}_{release_version}_SHA256SUMS.zip",
                "shasums_url": f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo_short}/release/{repository_name}_{release_version}_SHA256SUMS",
                "signing_keys": {
                    "gpg_public_keys": [
                        {
                        "ascii_armor": "-----BEGIN PGP PUBLIC KEY BLOCK-----\n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\nbxkzGYfMPQjjJ2g/VX93+W4=\n=r7A/\n-----END PGP PUBLIC KEY BLOCK-----",
                        "key_id": "F5DAB6023C43BF58",
                        "source": "",
                        "source_url": None,
                        "trust_signature": ""
                        }
                    ]
                }
            }
            
            print(f"Generating {os_}_{arch}...")
            with open(arch,'w+') as file:
                json.dump(release_dict,file)
                
            push_to_s3(arch,os_,arch)    


def push_to_s3(filename,os_,arch):
    s3_key = f"s3://{s3_bucket_name}/v1/providers/hashicorp/{repo_short}/{release_version}/download/{os_}/{arch}"
    output = subprocess.run(["aws","s3","cp",filename,s3_key],stdout=subprocess.PIPE, text=True)
    print(output.stdout)

    pass

def extend_versions(release_version):
    #check s3 have versions file
    # if have, cp the file and open it to update
    # if dont have, write new version file and upload
    with open("/Users/paulkuok/Desktop/public-repo-test/versions",'r+') as versions_file:
        body = json.load(versions_file)
        for item in body.get("versions"):
            if release_version in item['version']:
                print("same version exist")
                return

        extend_dict = {"platforms":[],"protocols": ["5.0"],"version": release_version}

        for os_ in ["darwin","freebsd","linux","windows"]:
            archs = ["arm64","amd64","386","arm"] if os_ not in "darwin" else ["arm64","amd64"]
            for arch in archs:
                extend_dict["platforms"].append({"arch":arch,"os":os_})

        body['versions'].append(extend_dict)
        print(body)

    with open ("/Users/paulkuok/Desktop/public-repo-test/versions",'w') as versions_file:
        json.dump(body,versions_file)

    s3_key = f"s3://{s3_bucket_name}/v1/providers/hashicorp/{repo_short}/versions"
    output = subprocess.run(["aws","s3","cp","versions",s3_key],stdout=subprocess.PIPE, text=True)
    print(output.stdout)    

    #s3://hket-custom-terraform-providers/v1/providers/hashicorp/hket-ad/versions
if __name__ == "__main__":
    pass
    # main()
    # extend_versions(release_version)

    # output = subprocess.run(["aws","s3","cp","s3://hket-custom-terraform-providers/v1/providers/hashicorp/hket-ad/version","."],stdout=subprocess.PIPE, text=True)
    # print(output.stdout)    

    # output = subprocess.run(["aws","s3api","head-object","--bucket","hket-custom-terraform-providers","--key","v1/providers/hashicorp/hket-ad/version"],stdout=subprocess.PIPE, text=True)
    # if "404" in output.stdout:
    #     print("not found")
    # print(output.stdout)