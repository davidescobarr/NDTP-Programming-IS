#!/bin/bash -x

# Define paths to your other bash scripts
SCRIPT1="./scripts/build_problem_solver.sh"
SCRIPT2="./scripts/build_kb.sh"
SCRIPT3="./scripts/build_sc_web.sh"

chmod +x "$SCRIPT1"

chmod +x "$SCRIPT2"

chmod +x "$SCRIPT3"

cd "../Рабочий стол"
source .venv/bin/activate
cd "../nika"

bash "$SCRIPT1"
bash "$SCRIPT2"
bash "$SCRIPT3"

echo "All modules are built."
