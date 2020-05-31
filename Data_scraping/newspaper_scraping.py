# This code scraps through the advertisement picture from a newspaper and extracts a text separately ad by ad.

# Imports the Google Cloud client library
import os
import statistics

from google.cloud import vision
import io

import cv2
import numpy as np
from PIL import Image, ImageDraw

import pandas as pd


def get_document_words(path):
    """
    With the help of Google Vision OCR, it recognizes the blocks/paragraphs/words with x,y coordinates.
    As the paragraph detection doesn't work properly for newspapers, the words are extracted in a big list.
    Later they are organized into paragraphs by detecting the lines in the newspaper.
    """
    document_words = []
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    document_words.append(word)
    return document_words


def get_image_with_no_words(path, words):
    """
    The mission is to create a clean version of the document with the words removed.
    This way the lines can be easily identified and not confuse segments like "----" or dense words as a line.
    Using Pillow library, the bounding box of the word is drawn as a filled white rectangle, then saved as temp.png
    """
    image = Image.open(path)
    draw = ImageDraw.Draw(image)
    for word in words:
        bound = word.bounding_box
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], 'white', 'white')
    temp_file = "temp.png"
    image.save(temp_file)
    return temp_file


def get_open_cv_lines(path):
    """
    Detect the lines in a document using OpenCV. Use the get_image_with_no_words function before to get sharper results.
    """
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    all_lines = cv2.HoughLinesP(edges, 1, np.pi / 10, 100, minLineLength=50, maxLineGap=0)
    valid_lines_y = [0]
    for line in all_lines:
        for x1, y1, x2, y2 in line:
            if (x2 - x1) != 0 and abs((y2 - y1) / (x2 - x1)) < 0.3:
                line_y = int(statistics.mean([y1, y2]))
                valid_lines_y.append(line_y)
                # cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # cv2.putText(img, "{} - {}".format(x1, y1), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0))

    # cv2.imwrite('img/debug_lines.png', img)
    valid_lines_y.append(img.shape[0])
    return valid_lines_y


def group_lines_y(all_lines_y):
    """
    As some lines are detected multiple times, we need to group them to be able to work with a lines y coordinate
    """
    all_lines_y.sort()
    average_lines_y = []
    one_line_group = [all_lines_y[0]]
    for line_y in all_lines_y[1:]:
        if line_y - 10 > max(one_line_group):
            one_line_group_avg = int(statistics.mean(one_line_group))
            average_lines_y.append(one_line_group_avg)
            one_line_group = []
        one_line_group.append(line_y)

    if one_line_group:
        one_line_group_avg = int(statistics.mean(one_line_group))
        average_lines_y.append(one_line_group_avg)
    return average_lines_y


def get_lines(path, words):
    """
    Simplified version of getting the lines with 1 call
    """
    image_with_no_words = get_image_with_no_words(path, words)
    all_lines_y = get_open_cv_lines(image_with_no_words)
    os.remove(image_with_no_words)
    return group_lines_y(all_lines_y)


def get_paragraphs_divided_by_lines(words, lines_y):
    """
    Group words into sections that are in between 2 lines
    """
    all_paragraphs = []
    one_paragraph_words = []
    words_index = 0
    for i in range(0, len(lines_y) - 1):
        top_line = lines_y[i]
        bottom_line = lines_y[i + 1]
        while words_index < len(words):
            word = words[words_index]
            word_middle_y = int(statistics.mean([word.bounding_box.vertices[0].y, word.bounding_box.vertices[1].y, word.bounding_box.vertices[2].y, word.bounding_box.vertices[3].y]))
            if top_line <= word_middle_y <= bottom_line:
                one_paragraph_words.append(word)
                words_index += 1
            else:
                all_paragraphs.append(one_paragraph_words)
                one_paragraph_words = []
                break
    if one_paragraph_words:
        all_paragraphs.append(one_paragraph_words)
    return all_paragraphs


def convert_words_to_string(paragraph_words):
    """
    Convert the resulting list of words aka a paragraph into a string
    """
    word_texts = []
    for paragraph_word in paragraph_words:
        word_texts.append(''.join([
            symbol.text for symbol in paragraph_word.symbols
        ]))
    return ' '.join(word_texts)


def get_words_lists(all_paragraphs):
    """
    Convert the resulting list of paragraphs into list of lists of string representations of the words
    """
    all_words_lists = []
    one_words_list = []
    for one_paragraph in all_paragraphs:
        for word in one_paragraph:
            one_words_list.append(''.join([
                symbol.text for symbol in word.symbols
            ]))
        all_words_lists.append(one_words_list)
        one_words_list = []
    return all_words_lists


if __name__ == '__main__':
    image_path = "norvegian_houses.png"
    doc_words = get_document_words(image_path)
    grouped_lines_y = get_lines(image_path, doc_words)
    paragraphs_by_lines = get_paragraphs_divided_by_lines(doc_words, grouped_lines_y)

    for p in paragraphs_by_lines:
        print(convert_words_to_string(p))
        print("--------------------------------\n")
    words_lists = get_words_lists(paragraphs_by_lines)
    df = pd.DataFrame.from_records(words_lists)
    df.to_excel("houses.xlsx")
    print(df)
