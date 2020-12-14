
import logging
import os


def save_as(pil_im, output_file_name, extension="jpg"):
    output_file = '.'.join([output_file_name, extension])
    try:
        pil_im.save(output_file)
    except Exception as ex:
        logging.error("Error during convert image to '{}': {}".format(extension, ex))


def get_files_by_extension(dir_path, extension="jpg"):
    if not os.path.exists(dir_path):
        logging.error("Path to dir '{}' not found".format(dir_path))
    all_files = os.listdir(dir_path)
    matched_files = filter(lambda file_name: file_name.endswith('.{}'.format(extension)), all_files)
    return [os.path.abspath(os.path.join(dir_path, file_name)) for file_name in matched_files]

