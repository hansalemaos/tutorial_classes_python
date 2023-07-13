import urllib
from time import sleep
from textwrapre import wrapre
from a_selenium2df import get_df
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

def split_text(text):
    return wrapre(
        " ".join(text.splitlines()),
        blocksize=4000,
        regexsep=r"\.",
        raisewhenlonger=False,
        removenewlines_from_result=True,
    )


class GoogleTranslate:
    def __init__(self, langsrc, langdst, headless=True):
        self.langsrc = langsrc
        self.langdst = langdst
        self.headless = headless
        self.driver = None
        self.trabalho_feito = []

    def __enter__(self):
        return self.start_chrome()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit_chromedriver()


    def start_chrome(self):
        self.driver = uc.Chrome(headless=self.headless)
        return self

    def translate(self, text):
        splitted = split_text(text)
        results = []
        for s in splitted:
            googlelink = f"https://translate.google.com/?sl={self.langsrc}&tl={self.langdst}&text={urllib.parse.quote(s)}&op=translate"
            self.driver.get(googlelink)
            sleep(1)
            checkval = 0
            while checkval < 0.5:
                try:
                    while len(self.driver.find_elements(By.TAG_NAME, "textarea")) < 2:
                        sleep(1)
                        continue
                    df = get_df(
                        self.driver,
                        By,
                        WebDriverWait,
                        expected_conditions,
                        queryselector="textarea",
                        with_methods=True,
                    )
                    checkval = df.iloc[0].aa_textLength / df.iloc[1].aa_textLength > 0.5
                    results.append(df.aa_value.iloc[1])
                except Exception:
                    sleep(1)
                    continue
        self.trabalho_feito.append(results)
        return self
    def quit_chromedriver(self):
        self.driver.close()
        self.driver.quit()
        return self

class YandexTranslator(GoogleTranslate):
    def __init__(self, langsrc, langdst, headless=True):
        super().__init__(langsrc, langdst, headless)

    def __str__(self):
        return f'{self.langsrc} -> {self.langdst}'
    def __repr__(self):
        return self.__str__()

    def translate(self,text):
        splitted = split_text(text)
        results = []
        for s in splitted:
            yandexlink = f'''https://translate.yandex.com/?source_lang={self.langsrc}&target_lang={self.langdst}&text={urllib.parse.quote(s)}'''
            self.driver.get(yandexlink)
            sleep(1)
            checkval = 0
            while checkval < 0.5:
                try:
                    while len(self.driver.find_elements(By.TAG_NAME, "pre")) < 1:
                        sleep(1)
                    df = get_df(
                        self.driver,
                        By,
                        WebDriverWait,
                        expected_conditions,
                        queryselector="span",
                        with_methods=True,
                    )
                    df2 = df.loc[df.aa_outerHTML.str.contains('fullTextTranslation', na=False)]
                    translatedtext = df2.aa_innerText.iloc[0]
                    lentranslated = len(translatedtext)
                    checkval = lentranslated / len(s) > .5
                    results.append(translatedtext)
                except Exception:
                    sleep(1)
                    continue
        self.trabalho_feito.append(results)
        return self



textlist=[""""Text""",]
with YandexTranslator("de", "pt") as g_de_pt:
    for text in textlist:
        g_de_pt.translate(text)

print(g_de_pt.trabalho_feito)



# g_de_pt = (
#     GoogleTranslate("de", "pt")
#     .start_chrome()
#     .translate(text_de)
#     .translate(text_de1)
#     .translate(text_de2)
#     .quit_chromedriver()
# )

# g_de_pt.start_chrome()
# result_de_pt = g_de_pt.translate(text_de)
# text_en='''The New York Times (the Times or NYT) is a daily newspaper based in New York City with a worldwide readership reported in 2022 to comprise 740,000 paid print subscribers, and 8.6 million paid digital subscribers.'''
# g_en_pt = GoogleTranslate('en','pt').start_chrome()
# result_en_pt = g_de_pt.translate(text_en)
# print(result_en_pt)
# print(result_de_pt)
