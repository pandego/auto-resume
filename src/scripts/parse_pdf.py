import argparse
import os
from typing import List

import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def pdf_to_images(input_pdf, output_folder):
    # Convert PDF to images (one image per page)
    images = convert_from_path(input_pdf)

    image_paths: List[str] = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, 'PNG')
        image_paths.append(image_path)

    return image_paths


def ocr_on_images(image_paths, output_txt):
    text = ''

    for image_path in image_paths:
        # Perform OCR on each image
        text += pytesseract.image_to_string(Image.open(image_path)) + "\n"

    # Write the extracted text to a file
    with open(output_txt, 'w', encoding='utf-8') as output_file:
        output_file.write(text)


def parse_args():
    parser = argparse.ArgumentParser(description="Convert PDF to images and extract text using OCR.")

    parser.add_argument(
        'input_pdf',
        help="Path to the input PDF file"
    )
    parser.add_argument(
        '--output_txt',
        help="Path to the output text file (default: input path with .txt extension)"
    )
    parser.add_argument(
        '--output_folder',
        help="Folder to save the intermediate images for OCR processing."
    )

    args = parser.parse_args()

    # If no output text file is specified, change the input file extension from .pdf to .txt
    if not args.output_txt:
        args.output_txt = os.path.splitext(args.input_pdf)[0] + '.txt'

    if not args.output_folder:
        args.output_folder = os.path.split(args.input_pdf)[0] + '/tmp_ocr/' + \
                             os.path.split(args.input_pdf)[1].split('.')[0]

    return args


if __name__ == "__main__":
    args = parse_args()

    os.makedirs(args.output_folder, exist_ok=True)

    # Convert PDF to images
    image_paths = pdf_to_images(args.input_pdf, args.output_folder)

    # Perform OCR on the images and save the text
    ocr_on_images(image_paths, args.output_txt)

    print(f"Text extracted and saved to {args.output_txt}")
