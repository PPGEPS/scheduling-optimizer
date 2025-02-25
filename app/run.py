import subprocess
from pathlib import Path

def main():
    current_dir = Path(__file__).parent

    print("Executando optimization.py...")
    subprocess.run(["python", str(current_dir / "optimization.py")])

    print("Executando decision.py...")
    subprocess.run(["python", str(current_dir / "decision.py")])

if __name__ == "__main__":
    main()
