#!/usr/bin/env python
# -*- coding: utf-8 -*-
name = "langSrc"


class LanguageDetector:
    def __init__(self, lang, srcPath, auto_translate=None):
        """
        :param lang: 语言 | Language
        :param srcPath: 语言源文件路径 | Language source file path
        :param auto_translate: 自动翻译函数 | Auto translate function: func(text, lang) -> str
        """
        self.default_lang = lang.lower()
        self.srcPath = srcPath
        self.save_flag = 0
        self.load()
        self.save_flag = 1
        self.translate = auto_translate

    def load(self):
        """
        加载语言包
        Load language package
        """
        import os

        if not os.path.exists(self.srcPath):
            self._src = {}
        else:
            with open(self.srcPath, "r", encoding="utf-8") as f:
                import json

                self._src = json.load(f)

            for name, word in self._src.items():
                self.register(name, word)

    def register(self, name: str, word: dict):
        """
        注册词条
        Register

        :param name: 词条名 | Entry name
        :param word: 词条, like:
        {
            "zh": "语言",
            "en": "Language",
            "jp": "言語",
            "kor": "언어",
            "fra": "Langue",
            "spa": "Idioma",
            "th": "ภาษา",
            "ara": "لغة",
            "ru": "язык",
            "pt": "Língua",
            "de": "Sprache",
            "it": "Lingua",
            "el": "Γλώσσα",
            "nl": "Taal",
            "bul": "Език",
            "est": "Keel",
            "dan": "Sprog",
            "fin": "Kieli",
            "cs": "Jazyk",
            "rom": "Limbă",
            "slo": "Jezik",
            "swe": "Språk",
            "hu": "Nyelv",
            "vie": "Ngôn ngữ"
        }
        """
        if not hasattr(self, name):
            setattr(self, name, word.get(self.default_lang, None))
            if self.save_flag > 0:
                self._src[name] = word
                self.save_flag = 2
        else:
            raise ValueError("The word has been registered")

    def __getitem__(self, item):
        res = getattr(self, item, None)
        if self.auto_translate and res is None:
            res = self.auto_translate(
                self._src[item][list(self._src[item].keys())[0]], self.default_lang
            )
            setattr(self, item, res)
            self._src[item][self.default_lang] = res
            self.save_flag = 2
        return res

    def __del__(self):
        if self.save_flag == 2:
            with open(self.srcPath, "w", encoding="utf-8") as f:
                import json

                json.dump(self._src, f, ensure_ascii=False, indent=4)
