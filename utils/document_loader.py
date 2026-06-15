from pathlib import Path

def load_repository(repo_path: Path):
    
    documents = []

    for file_path in repo_path.rglob("*"):
        # Skip directories
        if not file_path.is_file():
            continue

        try:
            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:
                content = f.read()

            document = {
                "content": content,
                "metadata": {
                    "file_name": file_path.name,
                    "relative_path": str(
                        file_path.relative_to(repo_path)
                    ),
                    "extension": file_path.suffix.lower()
                }
            }

            documents.append(document)

        except Exception as e:
            print(f"Could not read {file_path}: {e}")

    return documents