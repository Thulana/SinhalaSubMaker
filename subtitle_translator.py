# -*- coding: utf-8 -*-
### The comments with 3 # represents the code for Google Cloud Translate API.
### Currently this code is using the library provided by "googletrans".
import io
from translate import Translator


# zh-CN - chinese simplified
# zh-TW - chinese traditional
LANGUAGE = 'si'
SRT_FILE = 'sub1.srt'




s = [LANGUAGE]
filename = SRT_FILE.split(".")[0]
translator= Translator(to_lang="si")


def translate_text(text, target):
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    ###translate_client = translate.Client()

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    ###result = translate_client.translate(text, target_language=target)

    ###return result['translatedText']

    result = translator.translate(text, target)
    return result


for lang in s:
    with io.open(filename + "_" + lang + ".srt", 'wb') as hi:
        with io.open(filename + ".srt", 'r') as file:
            contents = file.readlines()
            contents[0] = "1\n"
            for i in range(len(contents)):
                if contents[i][0].isdigit():
                    hi.write(contents[i].encode())
                else:
                    receive = translate_text(contents[i], lang)
                    hi.write((receive + "\n").encode())
