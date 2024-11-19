# common Make commands for developing Python packages
run:
    uv run --directory crosszip python -c "import crosszip; print(crosszip.hello())"
