import os
import json
import subprocess


def main():
    # s3_bucket_name = "hket-terraform-private-registry"
    # repository_name = os.environ.get("GORELEASER_METADATA").get("project_name")
    # repo_short = repository_name.removeprefix("terraform-provider-")
    # release_version = os.environ.get("GORELEASER_METADATA").get("version")
    # gpg_keyid = os.environ.get("GPG_KEYID")
    # gpg_public_key = refactor_public_key(os.environ.get("GPG_PUBLICKEY"))
    # artifacts = os.environ.get("GORELEASER_ARTIFACTS")
    # versions_file_location = f"s3://{s3_bucket_name}/v1/providers/hashicorp/{repo_short}/versions"

    s3_bucket_name = "hket-custom-terraform-providers"
    repository_name = "terraform-provider-hket-ad"
    repo_short = repository_name.removeprefix("terraform-provider-")
    release_version = "0.5.3"
    gpg_keyid = os.environ.get("GPG_KEYID")
    gpg_public_key = refactor_public_key(os.environ.get("GPG_PUBLICKEY"))
    versions_file_location = f"s3://{s3_bucket_name}/v1/providers/hashicorp/{repo_short}/versions"

    configure_download_file(s3_bucket_name,repository_name,release_version,repo_short,gpg_public_key,gpg_keyid)
    publish_version(s3_bucket_name,release_version,repo_short,versions_file_location)

def refactor_public_key(public_key):
    refactored_key = public_key.replace("\n","\\n")
    return refactored_key

def read_file(filename):
    with open(filename,'r') as file:
        json_body = json.load(file)
        return json_body

def write_file(filename,content):
    with open(filename,'w') as file:
        json.dump(content,file) 

def configure_download_file(s3_bucket_name,repository_name,release_version,repo_short,gpg_public_key,gpg_keyid):   
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
                "shasum": get_shasum(f"{repository_name}_{release_version}_{os_}_{arch}.zip"),
                "shasums_signature_url": f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo_short}/release/{repository_name}_{release_version}_SHA256SUMS.zip",
                "shasums_url": f"https://hket-terraform-private-registry.hket.ai/v1/providers/hashicorp/{repo_short}/release/{repository_name}_{release_version}_SHA256SUMS",
                "signing_keys": {
                    "gpg_public_keys": [
                        {
                        "ascii_armor": gpg_public_key,
                        "key_id": gpg_keyid,
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
                
            s3_key = f"s3://{s3_bucket_name}/v1/providers/hashicorp/{repo_short}/{release_version}/download/{os_}/{arch}"
            push_to_s3(arch,s3_key)    

def new_version_item(release_version):
    extend_dict = {"platforms":[],"protocols": ["5.0"],"version": release_version}

    for os_ in ["darwin","freebsd","linux","windows"]:
        archs = ["arm64","amd64","386","arm"] if os_ not in "darwin" else ["arm64","amd64"]
        for arch in archs:
            extend_dict["platforms"].append({"arch":arch,"os":os_})

    return extend_dict  

def publish_version(s3_bucket_name,release_version,repo_short,versions_file_location):
    print("Checking 'versions' file in provider path...")
    file_exist = subprocess.run(["aws","s3api","head-object","--bucket",s3_bucket_name,"--key","v1/providers/hashicorp/"+repo_short+"/versions"],stdout=subprocess.PIPE, text=True).stdout
    if file_exist:
        print(f"Getting versions file from s3 in {s3_bucket_name}/v1/providers/hashicorp/{repo_short}/versions. ")
        get_versions_from_s3 = subprocess.run(["aws","s3","cp","s3://"+s3_bucket_name+"/v1/providers/hashicorp/"+repo_short+"/versions","."],stdout=subprocess.PIPE, text=True).stdout
        print(get_versions_from_s3)

        body = read_file("versions")
        for item in body.get("versions"):
            if release_version in item['version']:
                print("same version exist")
                return

        body['versions'].append(new_version_item(release_version))
        versions_content = body

    else:
        versions_content = {"versions":[new_version_item(release_version)]}

    write_file("versions",versions_content)
    push_to_s3("versions",versions_file_location)    


def push_to_s3(filename,s3_key):
    output = subprocess.run(["aws","s3","cp",filename,s3_key],stdout=subprocess.PIPE, text=True).stdout
    print(output)   


def get_shasum(filename):
    print(filename)
    with open('artifacts','r') as file:
        body = json.load(file)
        for item in body:
            if item.get('name') == filename:
                return item['extra']['Checksum'].removeprefix("sha256:")

        print("Couldn't find shasum of file:" + filename)
        return None

if __name__ == "__main__":
    main()
