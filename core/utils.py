import os
import re
import shutil
import tkinter as tk


def split_txt(input_file, output_path, logger) -> None:
    """
    This function will split txt novel into numerical order txt.
    :param input_file: path to input file.
    :param output_path: path to output file.
    :return: None
    """
    logger.insert(tk.INSERT, "[ info ] Start to split TXT. \n")
    if not os.path.exists(os.path.join(output_path, "temp")):
        os.makedirs(os.path.join(output_path, "temp"))
    else:
        shutil.rmtree(os.path.join(output_path, "temp"))
        os.makedirs(os.path.join(output_path, "temp"))
    save_file_path = None
    save_file = None
    with open(input_file, encoding='utf-8') as f:
        while True:
            # Read one line from
            line = f.readline()
            if not line:
                save_file.close()
                break
            line = line.rstrip('\r\n')

            pattern = r'[第章回部节集卷] *[\d一二三四五六七八九十零〇百千两]+ *[第章回部节集卷] '
            chapter = re.search(pattern, line)
            if chapter is not None:
                logger.insert(tk.INSERT, "[ info ] 找到：%s" % str(chapter[0]) + "\n")
                chapter = re.search(r"[\d一二三四五六七八九十零〇百千两]+", chapter[0])
                # Find new Chapter
                if save_file is not None:
                    save_file.close()

                save_file_path = os.path.join(output_path, "temp")
                save_file_path = os.path.join(save_file_path, "%s.txt" % str(chapter[0]))
                save_file = open(save_file_path, mode='a', encoding='utf-8')
                save_file.write(line)
                save_file.write("\n")
            else:
                save_file.write(line)
                save_file.write("\n")


def join_txt(txt_store_path, final_txt_path, logger) -> None:
    """
    This function will join all txt together.
    :param txt_store_path: path to stored txt folder
    :return: None
    """
    logger.insert(tk.INSERT, "[ info ] 开始排序并合并 \n")
    if not os.path.exists(final_txt_path):
        os.makedirs(final_txt_path)

    txt_name = []

    # Get txt names
    for root, dirs, files in os.walk(txt_store_path, topdown=False):
        for name in files:
            txt_name.append(name.split(".")[0])
    txt_name = [int(i) for i in txt_name]
    txt_name.sort(reverse=False)
    txt_name = [str(i) for i in txt_name]

    logger.insert(tk.INSERT, "[ info ] 排序完成，共 %d 章！" % int(len(txt_name)) + "\n")

    txt_out = os.path.join(final_txt_path, "output.txt")

    with open(txt_out, mode='a', encoding="utf-8") as f:
        for each in txt_name:
            logger.insert(tk.INSERT, "[ info ] Start to join: %s" % each + ".txt" + "\n")
            txt_path = os.path.join(txt_store_path, each + ".txt")
            with open(txt_path, encoding='utf-8') as txt:
                while True:
                    # Read one line from
                    line = txt.readline()
                    if not line:
                        break
                    line = line.rstrip('\r\n')
                    f.write(line)
                    f.write("\n")