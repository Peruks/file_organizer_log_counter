import os
import shutil

# ----------- CONFIG -----------
# Change this path when needed
TARGET_FOLDER = "sample_folder"

# File type mapping
FILE_TYPES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".doc", ".docx", ".txt"],
    "CSVs": [".csv"],
    "Logs": [".log"]
}
# -------------------------------

def create_subfolders(base_path):
    """Create subfolders if they don't exist."""
    for folder_name in FILE_TYPES.keys():
        folder_path = os.path.join(base_path, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

    # Folder for anything that doesn't match above types
    others_path = os.path.join(base_path, "Others")
    if not os.path.exists(others_path):
        os.mkdir(others_path)


def get_destination_folder(filename):
    """Return destination folder name based on file extension."""
    ext = os.path.splitext(filename)[1].lower()

    for folder_name, ext_list in FILE_TYPES.items():
        if ext in ext_list:
            return folder_name
    return "Others"


def organize_files(base_path):
    """Move files into subfolders based on file type."""
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)

        # Skip directories (we only want files)
        if os.path.isdir(item_path):
            continue

        dest_folder = get_destination_folder(item)
        dest_folder_path = os.path.join(base_path, dest_folder)

        shutil.move(item_path, os.path.join(dest_folder_path, item))


def count_log_errors(base_path):
    """Count lines containing 'ERROR' in .log and .txt files."""
    error_count = 0
    log_files_checked = 0

    # We will look inside base folder and Logs folder
    paths_to_check = [base_path, os.path.join(base_path, "Logs")]

    for path in paths_to_check:
        if not os.path.exists(path):
            continue

        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if os.path.isfile(item_path) and item_path.endswith((".log", ".txt")):
                log_files_checked += 1
                with open(item_path, "r", errors="ignore") as f:
                    for line in f:
                        if "ERROR" in line:
                            error_count += 1

    return log_files_checked, error_count


def main():
    base_path = os.path.abspath(TARGET_FOLDER)

    if not os.path.exists(base_path):
        print(f"Folder '{TARGET_FOLDER}' not found. Please check the path.")
        return

    print(f"Working on folder: {base_path}")
    print("-" * 50)

    # Step 1: create subfolders
    create_subfolders(base_path)

    # Step 2: organize files
    organize_files(base_path)
    print("✅ Files organized into subfolders.")

    # Step 3: count log errors
    log_files, errors = count_log_errors(base_path)
    print("✅ Log scan completed.")
    print("-" * 50)
    print(f"Log files checked : {log_files}")
    print(f"Total 'ERROR' lines: {errors}")


if __name__ == "__main__":
    main()
