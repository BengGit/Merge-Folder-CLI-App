import os
import shutil


def main():
    counts()
    input_prompt = "--the input folder:\n="
    output_prompt = "--the output folder:\n="
    overwrite = check_overwrite_status()
    print("Please Input the directory address for")
    input_path = prompt_directories(input_prompt)
    output_path = prompt_directories(output_prompt, True)
    move_directory(input_path, output_path, overwrite)
    print(f"\nMerging Completed!\n\n")
    completion_stats()

def counts():
    global folder_count
    global moved_count
    global skipped_count
    global replaced_count
    folder_count = 0
    moved_count = 0
    skipped_count = 0
    replaced_count = 0

def completion_stats():
    total_files_moved = moved_count + replaced_count
    total_count = total_files_moved + folder_count
    print(f"Folders moved: {folder_count}")
    print(f"Files:")
    print(f"    Moved:    {moved_count}")
    print(f"    Replaced: {replaced_count}")
    print(f"    Skipped:  {skipped_count}")
    print(f"    Total:    {total_files_moved}")
    print(f"Total entries affected: {total_count}")


def move_files(entry, output_path, overwrite):
    output_file_path = os.path.join(output_path, entry.name)
    if os.path.exists(output_file_path):
        if overwrite:
            os.unlink(output_file_path)
            shutil.move(entry.path, output_path)
            print(f"Replaced: {entry.name}")
            global replaced_count
            replaced_count = replaced_count + 1
            return
        if not overwrite:
            print(f"Skipped:  {entry.name}")
            global skipped_count
            skipped_count = skipped_count + 1
            return # exits without moving
    else:
        shutil.move(entry.path, output_path)
        print(f"Moved:    {entry.name}")
        global moved_count
        moved_count = moved_count + 1

def move_directory(input_path, output_path, overwrite):
    directory = os.scandir(input_path)
    for entry in directory :
        if entry.is_dir():
            input_dir = input_path + "\\" + entry.name
            output_dir = output_path + "\\" + entry.name
            check_dir(output_dir, True)
            move_directory(input_dir, output_dir, overwrite)
            delete_dir(input_dir)
        if entry.is_file():
            move_files(entry, output_path, overwrite)
        else:
            print(f"Directory {input_path} empty.")
    directory.close()

def delete_dir(input_dir):
    try: 
        os.rmdir(input_dir) 
    except OSError as error:
        return

def check_dir(directory_path,output = False):
        if os.path.exists(directory_path):
            return True
        if output:
            os.mkdir(directory_path)
            print(f"Directory {directory_path} created")
            global folder_count
            folder_count = folder_count + 1
            return True
        else:
            print(f"The directory '{directory_path}' does not exist.")

def prompt_directories(prompt, output = False):
    exists = False
    while(exists == False):
        directory_path = input(prompt)
        exists = check_dir(directory_path,output)
    return directory_path

def check_overwrite_status():
    while(True):
        response = input("Do you wish to overwrite files with the name names? y/n\n")
        if response[0].lower() == chr(121): # y or Y
            return True
        if response[0].lower() == chr(110): # n or N
            return False
        else:
            print(f"Error: Invalid Answer")

if __name__ == '__main__':
    main()
    input("\n.\n.\n.\npress any key to exit...")
