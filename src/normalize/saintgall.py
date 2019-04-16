"""Normalize Saint Gall dataset."""

from glob import glob
import argparse
import json
import os
import shutil


def norm_partitions(origin, target, args):
    """Normalize and create 'partitions' folder."""

    origin_dir = os.path.join(origin, "sets")
    target_dir = os.path.join(target, args["PARTITIONS_DIR"])

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    def complete_partition_file(set_file, new_set_file):

        with open(set_file) as file:
            with open(new_set_file, "w+") as new_file:
                content = [x.strip() for x in file.readlines()]
                lines = os.path.join(origin, "data", "line_images_normalized")

                for item in content:
                    glob_filter = os.path.join(lines, f"{item}*")
                    paths = [x for x in glob(glob_filter, recursive=True)]

                    for path in paths:
                        basename = os.path.basename(path).split(".")[0]
                        new_file.write(f"{basename.strip()}\n")

                new_file.close()

    set_file = os.path.join(origin_dir, "train.txt")
    new_set_file = os.path.join(target_dir, args["TRAIN_FILE"])
    complete_partition_file(set_file, new_set_file)

    set_file = os.path.join(origin_dir, "valid.txt")
    new_set_file = os.path.join(target_dir, args["VALIDATION_FILE"])
    complete_partition_file(set_file, new_set_file)

    set_file = os.path.join(origin_dir, "test.txt")
    new_set_file = os.path.join(target_dir, args["TEST_FILE"])
    complete_partition_file(set_file, new_set_file)


def norm_gt(origin, target, args):
    """Normalize and create 'gt' folder (Ground Truth)."""

    origin_dir = os.path.join(origin, "ground_truth")
    target_dir = os.path.join(target, args["GT_DIR"])

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    set_file = os.path.join(origin_dir, "transcription.txt")

    with open(set_file) as file:
        content = [x.strip() for x in file.readlines()]

        for line in content:
            if (not line or line[0] == "#"):
                continue

            splited = line.strip().split(' ')
            assert len(splited) >= 3

            file_name = splited[0]
            file_text = splited[1].replace("-", "").replace("|", " ")

            new_set_file = os.path.join(target_dir, f"{file_name}.txt")

            with open(new_set_file, "w+") as new_file:
                new_file.write(file_text.strip())
                new_file.close()


def norm_lines(origin, target, args):
    """Normalize and create 'lines' folder."""

    origin_dir = os.path.join(origin, "data")
    target_dir = os.path.join(target, args["DATA_DIR"])

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)

    glob_filter = os.path.join(origin_dir, "line_images_normalized", "*.*")
    files = [x for x in glob(glob_filter, recursive=True)]

    for file in files:
        shutil.copy(file, target_dir)


def main():
    """Get the input parameter and call normalization methods."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True)
    args = parser.parse_args()

    src = args.data_dir
    src_backup = f"{src}_backup"

    if not os.path.exists(src_backup):
        os.rename(src, src_backup)

    dirname = os.path.dirname(__file__)
    config = os.path.join(dirname, "..", "config.json")

    with open(config, "r") as file:
        env = json.load(file)

    norm_partitions(src_backup, src, env)
    norm_gt(src_backup, src, env)
    norm_lines(src_backup, src, env)


if __name__ == '__main__':
    main()