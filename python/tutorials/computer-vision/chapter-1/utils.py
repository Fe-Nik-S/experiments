
import logging


def save_as(pil_im, output_file_name, extension="jpg"):
    output_file = '.'.join([output_file_name, extension])
    try:
        pil_im.save(output_file)
    except Exception as ex:
        logging.error("Error during convert image to '{}': {}".format(extension, ex))
