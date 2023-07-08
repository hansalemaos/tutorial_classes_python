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


text_de = """The New York Times (NYT) ist eine einflussreiche überregionale US-amerikanische Tageszeitung, die in New York City im Verlag der New York Times Company erscheint."""
text_de1 = """Die New York Times Company ist im Aktienindex S&P 500 gelistet. Sie publiziert insgesamt über 30 Druckmedien. Ende 2016 lag die Druckauflage der New York Times wochentags bei 571.500, am Wochenende bei 1.085.700 Exemplaren. 2019 war die"""
text_de2 = """Die New York Times wurde als The New-York Daily Times 1851 von Henry J. Raymond und George Jones gegründet;"""
g_de_pt = (
    GoogleTranslate("de", "pt")
    .start_chrome()
    .translate(text_de)
    .translate(text_de1)
    .translate(text_de2)
    .quit_chromedriver()
)
print(g_de_pt.trabalho_feito)

# g_de_pt.start_chrome()
# result_de_pt = g_de_pt.translate(text_de)
# text_en='''The New York Times (the Times or NYT) is a daily newspaper based in New York City with a worldwide readership reported in 2022 to comprise 740,000 paid print subscribers, and 8.6 million paid digital subscribers.'''
# g_en_pt = GoogleTranslate('en','pt').start_chrome()
# result_en_pt = g_de_pt.translate(text_en)
# print(result_en_pt)
# print(result_de_pt)
