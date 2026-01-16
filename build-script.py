import os
import subprocess

def build_script(version="latest", build_env="prod"):
    services = ["catalog", "list-search", "upload-song", "reg-login", "play-song"]
    repo = "hafsa22/microsvc:"
    tag = version

    for service in services:
        try:
            build_command = ["docker", "build", "-t", f"{repo}{service}-{tag}","--build-arg", f"build_env={build_env}", f"./{service}-svc/."]
            print (build_command)
            print(f"Building {service} with tag {tag} and build_env {build_env}")
            subprocess.run(build_command, check=True)

            push_command = ["docker", "push", f"{repo}{service}-{tag}"]
            print(f"Pushing {service} with tag {tag}")
            subprocess.run(push_command, check=True)
        
        except subprocess.CalledProcessError as e:
            print(f"Error building or pushing {service} with tag {tag}")

if __name__ == "__main__":
    build_script()