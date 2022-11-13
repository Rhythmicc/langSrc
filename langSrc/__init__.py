#!/usr/bin/env python
# -*- coding: utf-8 -*-
name = "langSrc"
valid_lang = [
    "zh",  # 中文 | Chinese | 🇨🇳
    "en",  # 英文 | English | 🇬🇧
    "jp",  # 日文 | Japanese | 🇯🇵
    "kor",  # 韩文 | Korean | 🇰🇷
    "fra",  # 法文 | French | 🇫🇷
    "spa",  # 西班牙文 | Spanish | 🇪🇸
    "th",  # 泰文 | Thai | 🇹🇭
    "ara",  # 阿拉伯文 | Arabic | 🇸🇦
    "ru",  # 俄文 | Russian | 🇷🇺
    "pt",  # 葡萄牙文 | Portuguese | 🇵🇹
    "de",  # 德文 | German | 🇩🇪
    "it",  # 意大利文 | Italian | 🇮🇹
    "el",  # 希腊文 | Greek | 🇬🇷
    "nl",  # 荷兰文 | Dutch | 🇳🇱
    "bul",  # 保加利亚文 | Bulgarian | 🇧🇬
    "est",  # 爱沙尼亚文 | Estonian | 🇪🇪
    "dan",  # 丹麦文 | Danish | 🇩🇰
    "fin",  # 芬兰文 | Finnish | 🇫🇮
    "cs",  # 捷克文 | Czech | 🇨🇿
    "rom",  # 罗马尼亚文 | Romanian | 🇷🇴
    "slo",  # 斯洛文尼亚文 | Slovenian | 🇸🇮
    "swe",  # 瑞典文 | Swedish | 🇸🇪
    "hu",  # 匈牙利文 | Hungarian | 🇭🇺
    "vie",  # 越南文 | Vietnamese | 🇻🇳
]


class LanguageDetector:
    def __init__(self, lang, srcPath):
        """
        :param lang: 语言 | Language
        :param srcPath: 语言源文件路径 | Language source file path
        """
        if lang.lower() not in valid_lang:
            raise ValueError("Invalid or not support language")
        self.default_lang = lang
        self.srcPath = srcPath
        self.save_flag = 0
        self.load()
        self.save_flag = 1

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

    def register(self, name, word):
        """
        注册词条
        Register

        :param word: 词条, like:
        {
            "name": "language",
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
        return getattr(self, item)

    def __del__(self):
        if self.save_flag == 2:
            with open(self.srcPath, "w", encoding="utf-8") as f:
                import json

                json.dump(self._src, f, ensure_ascii=False, indent=4)
