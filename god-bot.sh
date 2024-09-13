
mkdir -p temp

TARGET=input/kjvc.txt
if [ ! -f "$TARGET" ]; then
    echo "$TARGET does not exists."
    echo "Cleaning input"
    python3 scripts/kjv-clean.py
fi

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt


python3 src/markov-chain.py

rm -rf temp

deactivate
