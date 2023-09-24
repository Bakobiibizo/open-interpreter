import subprocess
import argparse
import os
from alive_progress import alive_it

filenames = [
    "install/environment.sh",
    "install/cuda-wsl.sh",
    "install/cuda-torch.sh",
    "install/is_file.sh",
]
cwd = os.getcwd()

for filename in filenames:
    print(filename)
    output = subprocess.run(["chmod", "+x", cwd + "/" + filename], check=True)
    if output.returncode != 0:
        raise RuntimeError(f"Failed to chmod {filename}")

subprocesses ={
    "no_cuda": [
            ["sudo", "bash", "install/environment.sh"],
            ["python", "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel", "-q"], 
            ["sudo", "apt", "install", "build-essential", "-y", "-q"], 
            ["pip", "install", "gradio", "-q"],
            ["pip", "install", "elevenlabs", "-q"], 
            ["pip", "install", "git+https://github.com/openai/whisper.git", "-q", "--no-deps"], 
            ["pip", "install", "git+https://github.com/KillianLucas/open-interpreter.git", "-q"],
            ["pip", "install", "-r", "requirements-whisper.txt", "-q", "--no-deps"]
        ],
    "cuda-wsl": [
            ["sudo", "bash", "install/cuda-wsl.sh"]
        ],
    "cuda-torch":[
            ["sudo", "bash", "install/cuda-torch.sh"]
        ],
}

def install_packages(to_install):
    subp = subprocesses[to_install]
    
    bar = alive_it(subp)

    print("Installing", to_install)
    print("Please wait...")
    
    for item in bar:
        bar.text(f"\nrunning {item}")
        subprocess.run(item, check=True)

def main(packages):
    install_packages("no_cuda")
    if packages == "no_cuda":
        return
    install_packages(packages)
    return
    

def parseargs():
    options = [x for x in subprocesses.keys()]
    parser = argparse.ArgumentParser()
    parser.add_argument("--install", choices=options, help="select what set of subprocess to run for instillation")
    return parser.parse_args()

if __name__ == "__main__":
    options = [x for x in subprocesses.keys()]
    args = parseargs()
    choice = args.install
    if not choice:
        for i, option in enumerate(options):
            print(f"{i+1}: {option}")

        choice = input("Select what accleration you want to install instillation: ")
        choice = options[int(choice)-1]
    main(choice)